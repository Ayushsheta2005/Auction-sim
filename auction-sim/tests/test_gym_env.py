"""
Tests for AuctionEnv — verifies the Gym environment works correctly
with the existing auction-sim platform code.
"""

import json
import numpy as np
import gymnasium as gym

# Trigger registration
import auction_sim.gym_env  # noqa: F401

from auction_sim.config import SimConfig
from auction_sim.gym_env.auction_env import AuctionEnv


# ---------------------------------------------------------------------------
# Helper: minimal config
# ---------------------------------------------------------------------------
MINIMAL_CONFIG = {
    "world": {
        "start_ts": 1704067200,
        "horizon_hours": 24,
        "opportunities": 500,       # small for tests
        "batch_size": 500,
        "slots": 2,
        "slot_multipliers": [1.0, 0.7],
        "mechanism": "gsp",
        "embedding_dim": 8,         # small for tests
        "base_ctr": 0.05,
        "base_cvr": 0.03,
        "diurnal_amplitude": 0.2,
        "noise_std": 0.1,
        "regulation": {
            "min_quality": 0.0,
            "min_bid": 0.0,
            "reserve_cpc": 0.05,
        },
    },
    "sellers": [
        {
            "id": "agent",
            "brand": "AgentBrand",
            "value_per_conversion": 50.0,
            "cogs_ratio": 0.3,
            "seed": 1,
            "campaigns": [
                {
                    "id": "default",
                    "daily_budget": 100.0,
                    "base_bid_shading": 0.8,
                    "policy": "auto"
                }
            ]
        },
        {
            "id": "bg_1",
            "brand": "BG1",
            "value_per_conversion": 40.0,
            "cogs_ratio": 0.4,
            "seed": 2,
            "campaigns": [
                {
                    "id": "default",
                    "daily_budget": 100.0,
                    "base_bid_shading": 0.8,
                    "policy": "conservative"
                }
            ]
        },
        {
            "id": "bg_2",
            "brand": "BG2",
            "value_per_conversion": 60.0,
            "cogs_ratio": 0.5,
            "seed": 3,
            "campaigns": [
                {
                    "id": "default",
                    "daily_budget": 80.0,
                    "base_bid_shading": 0.8,
                    "policy": "roi_driven"
                }
            ]
        },
    ],
}


def _make_cfg() -> SimConfig:
    return SimConfig.model_validate(MINIMAL_CONFIG)


# ---------------------------------------------------------------------------
# Test 1: Environment creation and spaces
# ---------------------------------------------------------------------------
def test_env_creation():
    cfg = _make_cfg()
    env = AuctionEnv(cfg, agent_seller_index=0, seed=42)

    assert env.observation_space.shape == (8 + 6,)  # embed_dim + 6 extras
    assert env.action_space.shape == (1,)
    assert env.action_space.low[0] == 0.0
    print("✅ test_env_creation passed")


# ---------------------------------------------------------------------------
# Test 2: Reset returns valid observation
# ---------------------------------------------------------------------------
def test_reset():
    cfg = _make_cfg()
    env = AuctionEnv(cfg, seed=42)
    obs, info = env.reset()

    assert obs.shape == (14,)
    assert obs.dtype == np.float32
    assert "agent_spend" in info
    assert info["agent_spend"] == 0.0
    assert info["step"] == 0
    print("✅ test_reset passed")


# ---------------------------------------------------------------------------
# Test 3: Single step works
# ---------------------------------------------------------------------------
def test_single_step():
    cfg = _make_cfg()
    env = AuctionEnv(cfg, seed=42)
    obs, info = env.reset()

    action = np.array([1.0], dtype=np.float32)
    obs2, reward, terminated, truncated, info2 = env.step(action)

    assert obs2.shape == obs.shape
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert info2["step"] == 1
    print("✅ test_single_step passed")


# ---------------------------------------------------------------------------
# Test 4: Full episode runs to completion
# ---------------------------------------------------------------------------
def test_full_episode():
    cfg = _make_cfg()
    env = AuctionEnv(cfg, seed=42)
    obs, info = env.reset()

    total_reward = 0.0
    steps = 0
    done = False

    while not done:
        # Bid = value_per_conversion * predicted_cvr * 0.8 (like a rudimentary seller)
        pcvr = obs[8 + 4]  # the CVR component in observation
        bid = np.array([50.0 * pcvr * 0.8], dtype=np.float32)
        obs, reward, terminated, truncated, info = env.step(bid)
        total_reward += reward
        steps += 1
        done = terminated or truncated

    print(f"   Episode: {steps} steps, reward={total_reward:.2f}")
    print(f"   Spend: ₹{info['agent_spend']:.2f}/{info['agent_budget']:.2f}")
    print(f"   Wins: {info['agent_wins']}, Clicks: {info['agent_clicks']}, Conv: {info['agent_conversions']}")
    print(f"   Revenue: ₹{info['agent_revenue']:.2f}, ROAS: {info['agent_roas']:.2f}")
    assert steps > 0
    assert steps <= 500  # at most opportunities
    print("✅ test_full_episode passed")


# ---------------------------------------------------------------------------
# Test 5: Zero bid → never wins
# ---------------------------------------------------------------------------
def test_zero_bid():
    cfg = _make_cfg()
    env = AuctionEnv(cfg, seed=42)
    obs, _ = env.reset()

    for _ in range(50):
        obs, reward, done, _, info = env.step(np.array([0.0], dtype=np.float32))
        if done:
            break

    assert info["agent_wins"] == 0
    assert info["agent_spend"] == 0.0
    print("✅ test_zero_bid passed")


# ---------------------------------------------------------------------------
# Test 6: Very high bid → should win frequently
# ---------------------------------------------------------------------------
def test_high_bid():
    cfg = _make_cfg()
    env = AuctionEnv(cfg, seed=42)
    obs, _ = env.reset()

    for _ in range(100):
        obs, reward, done, _, info = env.step(np.array([200.0], dtype=np.float32))
        if done:
            break

    # With a huge bid the agent should win most auctions
    assert info["agent_wins"] > 50
    print(f"   High bid: won {info['agent_wins']}/100 auctions, spend=₹{info['agent_spend']:.2f}")
    print("✅ test_high_bid passed")


# ---------------------------------------------------------------------------
# Test 7: Gymnasium registry works
# ---------------------------------------------------------------------------
def test_gym_registry():
    cfg = _make_cfg()
    env = gym.make("AuctionEnv-v0", cfg=cfg, seed=42)
    obs, info = env.reset()
    assert obs.shape[0] > 0
    obs, r, d, t, i = env.step(env.action_space.sample())
    print("✅ test_gym_registry passed")


# ---------------------------------------------------------------------------
# Test 8: Reproducibility — same seed gives same results
# ---------------------------------------------------------------------------
def test_reproducibility():
    cfg = _make_cfg()

    def run_episode(seed):
        env = AuctionEnv(cfg, seed=seed)
        obs, _ = env.reset()
        total_r = 0.0
        for _ in range(100):
            obs, r, d, _, _ = env.step(np.array([1.5], dtype=np.float32))
            total_r += r
            if d:
                break
        return total_r

    r1 = run_episode(42)
    r2 = run_episode(42)
    assert r1 == r2, f"Not reproducible: {r1} != {r2}"
    print("✅ test_reproducibility passed")


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_env_creation()
    test_reset()
    test_single_step()
    test_full_episode()
    test_zero_bid()
    test_high_bid()
    test_gym_registry()
    test_reproducibility()
    print("\n🎉 All tests passed!")
