"""
AuctionEnv — Gymnasium wrapper around the auction-sim platform.

Exposes the auction simulation as a step-by-step environment.
One step = one user arrives, the agent (a single seller) places a bid,
the auction resolves against background competitors, and the outcome
(win/loss, click, conversion, cost) is returned.

Observation:
    0..embed_dim-1   : user embedding vector
    embed_dim        : elapsed fraction of the day [0, 1]
    embed_dim+1      : remaining budget fraction [0, 1]
    embed_dim+2      : diurnal traffic multiplier
    embed_dim+3      : agent's quality score for this user (CTR-based)
    embed_dim+4      : predicted CVR for this user
    embed_dim+5      : number of competing bids (active background sellers)

Action (continuous):
    A single float in [0, max_bid] representing the bid amount.

Reward:
    If won a slot and user clicked:
        If converted: value_per_conversion - price_paid
        Else:         -price_paid
    If won but no click:  0
    If lost auction:      0

Episode ends when:
    - All opportunities are exhausted (day is over), OR
    - Agent's budget is fully spent.
"""

from __future__ import annotations

from typing import Any, Optional

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from auction_sim.auction.mechanisms import allocate, prices_first_price, prices_gsp, prices_vcg
from auction_sim.auction.regulation import Regulator
from auction_sim.config import SimConfig
from auction_sim.market.sellers import Seller, make_sellers
from auction_sim.market.users import UserGenerator
from auction_sim.utils.features import sigmoid


class AuctionEnv(gym.Env):

    """
    Gymnasium environment for a single-agent ad auction.

    The agent controls ONE seller.  Background sellers use their configured
    policies (campaign strategies) and compete in every auction.

    Parameters
    ----------
    cfg : SimConfig
        Full simulation configuration.
    agent_seller_index : int
        Which seller in cfg.sellers the agent controls (default 0).
    seed : int | None
        Random seed.
    """

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        cfg: SimConfig,
        agent_seller_index: int = 0,
        seed: int | None = None,
        render_mode: str | None = None,
    ):
        super().__init__()
        self.cfg = cfg
        self.w = cfg.world
        self.agent_idx = agent_seller_index
        self.render_mode = render_mode

        # --- Dimensions ---
        self.embed_dim = self.w.embedding_dim
        # obs = user_embed(d) + elapsed(1) + budget_frac(1) + diurnal(1) + quality(1) + pcvr(1) + n_competitors(1)
        obs_dim = self.embed_dim + 6

        # --- Spaces ---
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32
        )
        # Agent bids a non-negative amount.  Upper bound is generous.
        # We calculate max_bid based on the first campaign or just an arbitrary high value
        # if the agent has no campaigns default to 1.0 * 5.0
        val_per_conv = cfg.sellers[agent_seller_index].value_per_conversion
        max_bid = val_per_conv * 5.0 if val_per_conv > 0 else 50.0
        self.action_space = spaces.Box(
            low=np.float32(0.0), high=np.float32(max_bid), shape=(1,), dtype=np.float32
        )

        # --- Internal state (populated on reset) ---
        self._rng: np.random.Generator | None = None
        self._seed = seed
        self._sellers: list[Seller] = []
        self._agent: Seller | None = None
        self._regulator: Regulator | None = None

        # Pre-computed user data for the episode
        self._user_embeds: np.ndarray | None = None
        self._timestamps: np.ndarray | None = None
        self._diurnal: np.ndarray | None = None
        self._CTR: np.ndarray | None = None
        self._CVR: np.ndarray | None = None

        self._step_idx = 0
        self._n_opportunities = 0

        # Cumulative episode stats
        self._agent_spend = 0.0
        self._agent_clicks = 0
        self._agent_conversions = 0
        self._agent_revenue = 0.0
        self._agent_wins = 0

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def reset(
        self,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict]:
        super().reset(seed=seed)

        s = seed if seed is not None else self._seed
        self._rng = np.random.default_rng(s)

        w = self.w

        # --- Create sellers ---
        self._sellers = make_sellers(self.cfg, w.embedding_dim, self._rng.integers(0, 2**31))
        self._agent = self._sellers[self.agent_idx]

        # --- Regulator ---
        self._regulator = Regulator(
            w.regulation.min_quality, w.regulation.min_bid, w.regulation.reserve_cpc
        )

        # --- Generate ALL users for the episode upfront (vectorized) ---
        ug = UserGenerator(
            w.embedding_dim, w.base_ctr, w.base_cvr, w.diurnal_amplitude, w.noise_std,
            int(self._rng.integers(0, 2**31)),
        )
        self._n_opportunities = w.opportunities
        self._user_embeds, self._timestamps, self._diurnal = ug.batch(
            self._n_opportunities, w.start_ts, w.horizon_hours
        )

        # Pre-compute CTR / CVR matrices  (n_users × n_sellers)
        S = len(self._sellers)
        A = np.stack([s.ad_vec for s in self._sellers], axis=0)  # (S, d)
        Q = self._user_embeds @ A.T  # (n, S)
        Q = (Q - Q.mean()) / (Q.std() + 1e-6)
        self._CTR = sigmoid(Q) * w.base_ctr * self._diurnal.reshape(-1, 1)
        self._CVR = sigmoid(Q / 2) * w.base_cvr

        # --- Reset counters ---
        self._step_idx = 0
        self._agent_spend = 0.0
        self._agent_clicks = 0
        self._agent_conversions = 0
        self._agent_revenue = 0.0
        self._agent_wins = 0

        obs = self._make_obs()
        info = self._make_info(auction_result=None)
        return obs, info

    # ------------------------------------------------------------------
    # Step
    # ------------------------------------------------------------------
    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool, dict]:
        """
        Run one auction.

        Parameters
        ----------
        action : np.ndarray, shape (1,)
            The agent's bid for the current user.

        Returns
        -------
        obs, reward, terminated, truncated, info
        """
        assert self._agent is not None, "Call reset() before step()"

        t = self._step_idx
        w = self.w
        k = w.slots
        slot_m = np.array(w.slot_multipliers[:k])

        ctr_row = self._CTR[t]  # (S,)
        cvr_row = self._CVR[t]  # (S,)
        elapsed = float((self._timestamps[t] - w.start_ts) / (w.horizon_hours * 3600))

        S = len(self._sellers)

        # --- 1. Collect bids ---
        bids = np.zeros(S)
        active_campaigns = [None] * S
        
        for i, seller in enumerate(self._sellers):
            if i == self.agent_idx:
                # Agent's bid from the action
                agent_bid = float(np.clip(action, 0.0, None).flat[0])
                # Respect budget
                remaining = self._agent.daily_budget - self._agent_spend
                if remaining <= 0:
                    agent_bid = 0.0
                bids[i] = agent_bid
                
                # We can optionally hook up an active campaign for the agent if we want it to track stats too
                _, ac = self._agent.bid(ctr_row[i], cvr_row[i], elapsed)
                active_campaigns[i] = ac
            else:
                # Background seller bids via its policy
                bids[i], active_campaigns[i] = seller.bid(ctr_row[i], cvr_row[i], elapsed)

        # --- 2. Quality scores ---
        qs = ctr_row.copy()
        max_q = qs.max()
        if max_q > 0:
            qs = qs / max_q
        else:
            qs = qs + 1e-9

        # --- 3. Regulation ---
        bids, qs = self._regulator.screen(bids, qs)

        # --- 4. Run auction ---
        mech = w.mechanism
        if mech == "first_price":
            idx, _ = allocate(bids, qs, k)
            prices = prices_first_price(bids, idx)
        elif mech == "vcg":
            idx, prices = prices_vcg(bids, qs, slot_m)
        else:
            idx, _ = allocate(bids, qs, k)
            prices = prices_gsp(bids, qs, idx)

        prices = np.maximum(prices, w.regulation.reserve_cpc)

        # --- 5. Simulate clicks & conversions ---
        lm = slot_m[: len(idx)]
        ctr_show = ctr_row[idx] * lm
        clicked = self._rng.random(len(idx)) < ctr_show
        converted = (self._rng.random(len(idx)) < cvr_row[idx]) & clicked
        pay = prices * clicked

        # --- 6. Determine agent outcome & Update background sellers ---
        reward = 0.0
        agent_won = False
        agent_slot = -1
        agent_clicked = False
        agent_converted = False
        agent_price = 0.0

        winners_map = {pos: j for j, pos in enumerate(idx)}
        
        for i, seller in enumerate(self._sellers):
            if i == self.agent_idx:
                if i in winners_map:
                    j = winners_map[i]
                    agent_won = True
                    agent_slot = j
                    agent_clicked = bool(clicked[j])
                    agent_converted = bool(converted[j])
                    agent_price = float(pay[j])

                    self._agent_spend += agent_price
                    self._agent_wins += 1
                    if agent_clicked:
                        self._agent_clicks += 1
                    if agent_converted:
                        self._agent_conversions += 1
                        conv_value = self._agent.value_per_conversion
                        self._agent_revenue += conv_value
                        reward = conv_value - agent_price
                    elif agent_clicked:
                        reward = -agent_price
                        
                    # Also update the agent's internal stats 
                    # Note: We omit the `observe_and_adapt` step because the RL agent acts independently,
                    # but we keep internal campaign state aligned with the environment tracking just in case
                    seller.observe_and_adapt(active_campaigns[i], int(agent_clicked), int(agent_converted), agent_price, elapsed)
                else:
                    seller.observe_and_adapt(active_campaigns[i], 0, 0, 0.0, elapsed)
            else:
                # Background seller update
                if i in winners_map:
                    j = winners_map[i]
                    seller.observe_and_adapt(active_campaigns[i], int(clicked[j]), int(converted[j]), float(pay[j]), elapsed)
                else:
                    seller.observe_and_adapt(active_campaigns[i], 0, 0, 0.0, elapsed)


        # --- 8. Advance step ---
        self._step_idx += 1

        # --- 9. Check termination ---
        budget_exhausted = (self._agent.daily_budget - self._agent_spend) <= 0
        day_over = self._step_idx >= self._n_opportunities
        terminated = budget_exhausted or day_over
        truncated = False

        # --- 10. Build next observation ---
        if not terminated:
             obs = self._make_obs()
        else:
             # Terminal observation (zeros)
             obs = np.zeros(self.observation_space.shape, dtype=np.float32)

        info = self._make_info(
            auction_result={
                "won": agent_won,
                "slot": agent_slot,
                "clicked": agent_clicked,
                "converted": agent_converted,
                "price_paid": agent_price,
                "reward": reward,
            }
        )

        return obs, reward, terminated, truncated, info

    # ------------------------------------------------------------------
    # Observation builder
    # ------------------------------------------------------------------
    def _make_obs(self) -> np.ndarray:
        """Build the observation vector for the current step."""
        t = self._step_idx
        w = self.w

        user_embed = self._user_embeds[t].astype(np.float32)  # (d,)
        elapsed = float((self._timestamps[t] - w.start_ts) / (w.horizon_hours * 3600))
        budget_frac = float(
            (self._agent.daily_budget - self._agent_spend) / max(self._agent.daily_budget, 1e-9)
        )
        diurnal = float(self._diurnal[t])

        # Agent's quality / CTR / CVR for this user
        quality = float(self._CTR[t, self.agent_idx])
        pcvr = float(self._CVR[t, self.agent_idx])

        # Count active competitors (those with remaining budget)
        n_active = sum(
            1 for i, s in enumerate(self._sellers)
            if i != self.agent_idx and (s.daily_budget - s.spend) > 0
        )

        obs = np.concatenate([
            user_embed,
            np.array([elapsed, budget_frac, diurnal, quality, pcvr, n_active], dtype=np.float32),
        ])
        return obs

    # ------------------------------------------------------------------
    # Info builder
    # ------------------------------------------------------------------
    def _make_info(self, auction_result: dict | None = None) -> dict:
        info = {
            "step": self._step_idx,
            "total_opportunities": self._n_opportunities,
            "agent_spend": self._agent_spend,
            "agent_budget": self._agent.daily_budget,
            "agent_remaining_budget": self._agent.daily_budget - self._agent_spend,
            "agent_clicks": self._agent_clicks,
            "agent_conversions": self._agent_conversions,
            "agent_revenue": self._agent_revenue,
            "agent_wins": self._agent_wins,
            "agent_roas": (
                self._agent_revenue / self._agent_spend if self._agent_spend > 0 else 0.0
            ),
        }
        if auction_result is not None:
            info["auction"] = auction_result
        return info

    # ------------------------------------------------------------------
    # Render (optional, human-readable)
    # ------------------------------------------------------------------
    def render(self):
        if self.render_mode == "human":
            t = self._step_idx
            total = self._n_opportunities
            spend = self._agent_spend
            budget = self._agent.daily_budget
            print(
                f"Step {t}/{total} | "
                f"Spend: ₹{spend:.2f}/₹{budget:.2f} | "
                f"Wins: {self._agent_wins} | "
                f"Clicks: {self._agent_clicks} | "
                f"Conv: {self._agent_conversions} | "
                f"Revenue: ₹{self._agent_revenue:.2f}"
            )
