"""
Quick demo: Run a single episode with a simple bidding strategy
and display the results.

Usage:
    cd auction-sim
    source .venv/bin/activate
    python3 scripts/demo_gym_env.py
"""

import numpy as np
from auction_sim.config import SimConfig
from auction_sim.gym_env.auction_env import AuctionEnv


CONFIG = {
    "world": {
        "start_ts": 1704067200,
        "horizon_hours": 24,
        "opportunities": 10000,
        "batch_size": 10000,
        "slots": 3,
        "slot_multipliers": [1.0, 0.7, 0.5],
        "mechanism": "gsp",
        "embedding_dim": 16,
        "base_ctr": 0.02,
        "base_cvr": 0.02,
        "diurnal_amplitude": 0.2,
        "noise_std": 0.1,
        "regulation": {
            "min_quality": 0.0,
            "min_bid": 0.0,
            "reserve_cpc": 0.05,
        },
    },
    "sellers": [
        {  # Agent — we control this one
            "id": "agent",
            "brand": "MyBrand",
            "daily_budget": 500.0,
            "value_per_conversion": 50.0,
            "cogs_ratio": 0.3,
            "base_bid_shading": 0.8,
            "policy": "auto",
            "seed": 1,
        },
        {  # Competitor 1
            "id": "comp_1",
            "brand": "Rival_A",
            "daily_budget": 400.0,
            "value_per_conversion": 40.0,
            "cogs_ratio": 0.4,
            "base_bid_shading": 0.8,
            "policy": "rudimentary",
            "seed": 2,
        },
        {  # Competitor 2
            "id": "comp_2",
            "brand": "Rival_B",
            "daily_budget": 600.0,
            "value_per_conversion": 60.0,
            "cogs_ratio": 0.5,
            "base_bid_shading": 0.8,
            "policy": "auto",
            "seed": 3,
        },
    ],
}


def simple_bidding_strategy(obs: np.ndarray, value_per_conv: float = 50.0) -> np.ndarray:
    """
    A simple heuristic bidding strategy.
    Bids = value_per_conversion * predicted_CVR * budget_pacing_factor
    """
    embed_dim = 16
    budget_frac = obs[embed_dim + 1]   # remaining budget fraction
    pcvr = obs[embed_dim + 4]          # predicted CVR for this user

    # Base value: how much this impression is worth
    value = value_per_conv * pcvr

    # Pace: bid more aggressively when budget is high, less when low
    pacing = 0.5 + 0.5 * budget_frac   # ranges from 0.5 to 1.0

    bid = value * pacing
    return np.array([bid], dtype=np.float32)


def main():
    cfg = SimConfig.model_validate(CONFIG)
    env = AuctionEnv(cfg, agent_seller_index=0, seed=42)

    obs, info = env.reset()
    print("=" * 60)
    print("AuctionGym Demo — Single Episode")
    print("=" * 60)
    print(f"Opportunities:  {info['total_opportunities']}")
    print(f"Agent budget:   ₹{info['agent_budget']:.2f}")
    print(f"Obs dimension:  {obs.shape[0]}")
    print(f"Action space:   {env.action_space}")
    print("=" * 60)

    total_reward = 0.0
    steps = 0
    done = False
    milestones = [1000, 2500, 5000, 7500]

    while not done:
        action = simple_bidding_strategy(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        steps += 1
        done = terminated or truncated

        if steps in milestones:
            print(
                f"  Step {steps:>5} | "
                f"Spend ₹{info['agent_spend']:>8.2f} | "
                f"Wins {info['agent_wins']:>5} | "
                f"Clicks {info['agent_clicks']:>4} | "
                f"Conv {info['agent_conversions']:>3} | "
                f"ROAS {info['agent_roas']:>6.2f}"
            )

    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Steps:          {steps}")
    print(f"Total Reward:   ₹{total_reward:.2f}")
    print(f"Spend:          ₹{info['agent_spend']:.2f} / ₹{info['agent_budget']:.2f}")
    print(f"Wins:           {info['agent_wins']}")
    print(f"Clicks:         {info['agent_clicks']}")
    print(f"Conversions:    {info['agent_conversions']}")
    print(f"Revenue:        ₹{info['agent_revenue']:.2f}")
    print(f"ROAS:           {info['agent_roas']:.2f}")
    print(f"Win rate:       {info['agent_wins'] / steps * 100:.1f}%")
    if info['agent_clicks'] > 0:
        print(f"CPC:            ₹{info['agent_spend'] / info['agent_clicks']:.2f}")
    if info['agent_conversions'] > 0:
        print(f"CPA:            ₹{info['agent_spend'] / info['agent_conversions']:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
