# BTP Project: Ad Auction Simulation Platform — Complete Status Document

**Date**: March 11, 2026
**Student**: Ayush
**Semester**: 6th (BTP)

---

## 1. WHAT IS THIS PROJECT

This is a **multi-slot online advertising auction simulator** built in Python. It models a complete ad marketplace where:

- **Users** arrive (300,000 per simulated day) with interest profiles (embedding vectors)
- **Sellers (advertisers)** compete by bidding to show their ads
- A **Platform** runs auctions (GSP/VCG/First-Price) to allocate ad slots to winning sellers
- **Clicks and conversions** are simulated probabilistically based on user-ad relevance
- Sellers pay the platform for clicks, and the simulation tracks spend, revenue, ROAS, etc.

The project has **two separate codebases** (platform side + seller side) that need to communicate through a clean interface. A **Gymnasium (AuctionGym)** environment has been integrated on the platform side to formalize this interface.

---

## 2. WORKSPACE STRUCTURE

```
/home/ayush/Desktop/sem6/BTP/
├── auction-sim/           ← PLATFORM SIDE (Ayush's work)
│   ├── src/auction_sim/
│   │   ├── config.py
│   │   ├── cli.py
│   │   ├── analysis.py
│   │   ├── auction/
│   │   │   ├── mechanisms.py
│   │   │   └── regulation.py
│   │   ├── market/
│   │   │   ├── sellers.py
│   │   │   └── users.py
│   │   ├── simulation/
│   │   │   ├── engine.py
│   │   │   └── tasks.py
│   │   ├── gym_env/           ← NEWLY ADDED (AuctionGym)
│   │   │   ├── __init__.py
│   │   │   └── auction_env.py
│   │   └── utils/
│   │       └── features.py
│   ├── tests/
│   │   ├── test_gym_env.py    ← NEWLY ADDED
│   │   └── test_imports.py
│   ├── scripts/
│   │   └── demo_gym_env.py    ← NEWLY ADDED
│   ├── configs/
│   │   └── example.json
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── .venv/                 ← Python 3.12 venv with all deps
│
├── seller/resint/             ← SELLER SIDE (Navishaa's work)
│   ├── src/auction_sim/
│   │   ├── config.py          (same schema as platform)
│   │   ├── cli.py
│   │   ├── auction/
│   │   │   ├── mechanisms.py  (same as platform)
│   │   │   └── regulation.py  (same as platform)
│   │   ├── market/
│   │   │   ├── sellers.py     ← DIFFERENT: has Campaign, 5 policies, observe_and_adapt()
│   │   │   └── users.py       (same as platform)
│   │   ├── simulation/
│   │   │   ├── engine.py      ← DIFFERENT: calls observe_and_adapt(), logs history
│   │   │   └── tasks.py       (modified for 3-tuple return)
│   │   └── utils/
│   │       └── features.py    (same as platform)
│   ├── configs/
│   │   └── example.json       ← 5 sellers with 5 different policies
│   ├── visualize_results.py
│   └── runs/                  ← Contains actual run outputs (sellers.csv, metrics.csv, history.csv)
│
├── resint/                    ← IGNORE (old dev fork, not relevant)
└── 9febclone/                 ← IGNORE (old backup, not relevant)
```

---

## 3. PLATFORM SIDE — DETAILED COMPONENT BREAKDOWN

All code lives in `auction-sim/src/auction_sim/`.

### 3.1 `config.py` — Configuration Schema

Pydantic models that define the entire simulation world:

```python
class RegulationConfig:
    min_quality: float = 0.0       # Min quality score to participate
    min_bid: float = 0.0           # Min bid amount
    reserve_cpc: float = 0.0       # Floor price per click

class SellerConfig:
    id: str                        # "A", "B", etc.
    brand: str                     # "alpha", "beta"
    daily_budget: float            # e.g., 20000.0 (₹)
    value_per_conversion: float    # e.g., 50.0 (₹)
    cogs_ratio: float              # Cost of goods ratio (0.5 = 50%)
    base_bid_shading: float        # Bid multiplier (0.8 = bid 80% of value)
    policy: str                    # "rudimentary" or "auto"
    seed: int

class WorldConfig:
    start_ts: int                  # Unix timestamp for day start
    horizon_hours: int             # 24 (one day)
    opportunities: int             # 300,000 user visits
    batch_size: int                # 100,000 per block
    slots: int                     # 3 ad slots per page
    slot_multipliers: [1.0, 0.7, 0.5]  # Position bias (slot 1 best)
    mechanism: str                 # "gsp" | "first_price" | "vcg"
    embedding_dim: int             # 16 (user/ad vector size)
    base_ctr: float                # 0.02 (2% base click-through rate)
    base_cvr: float                # 0.02 (2% base conversion rate)
    diurnal_amplitude: float       # 0.2 (time-of-day traffic variation)
    noise_std: float               # 0.1

class SimConfig:
    world: WorldConfig
    sellers: List[SellerConfig]
```

### 3.2 `market/users.py` — User Generation

```python
class UserGenerator:
    def batch(self, n, t0, horizon_hours):
        # Returns:
        #   u: (n, embed_dim) — user embedding vectors (unit normalized)
        #   ts: (n,) — random timestamps across the day
        #   diurnal: (n,) — traffic multiplier based on time-of-day (sinusoidal)
```

- Each user is a 16-dimensional unit vector representing their interests
- Time-of-day pattern: `1.0 + amplitude * sin(2π * hour / 24)` — more traffic at peak hours

### 3.3 `market/sellers.py` — Seller Agents (Platform Version)

```python
@dataclass
class Seller:
    id, brand, daily_budget, value_per_conversion, cogs_ratio
    base_bid_shading, policy, seed, d, ad_vec
    spend=0, clicks=0, conv=0, revenue=0

class RudimentaryPolicy:
    def bid(self, p_ctr, p_cvr):
        return base_bid_shading * value_per_conversion * p_cvr

class PacingController:
    def update(self, elapsed_frac, spent):
        # Adjusts pacing multiplier based on: am I spending too fast or too slow?
        # target = budget * elapsed_frac (how much SHOULD have been spent by now)
        # gap = target - actual_spent
        # multiplier goes up if underspending, down if overspending

class AutoBidPolicy:
    def bid(self, p_ctr, p_cvr, elapsed_frac, spent):
        value = value_per_conversion * p_cvr
        multiplier = pacer.update(elapsed_frac, spent)
        return value * multiplier
```

### 3.4 `auction/mechanisms.py` — Auction Logic

```python
def allocate(bids, qs, k):
    # Rank by bid × quality_score, pick top-k → winners get k slots

def prices_gsp(bids, qs, idx):
    # GSP: each winner pays (next_bidder_score / own_quality)
    # → you pay just enough to beat the bidder below you

def prices_first_price(bids, idx):
    # You pay exactly what you bid

def prices_vcg(bids, qs, slot_m):
    # VCG: you pay the externality you impose on others
```

### 3.5 `auction/regulation.py` — Quality Screening

```python
class Regulator:
    def screen(self, bids, qs):
        # Zeros out bids from sellers who fail:
        #   quality_score < min_quality  OR  bid < min_bid
```

### 3.6 `utils/features.py` — Math Helpers

```python
def unit_embeddings(rng, n, d):    # Random unit vectors
def sigmoid(x):                     # 1 / (1 + exp(-x))
```

### 3.7 `simulation/engine.py` — Core Simulation Loop

The heart of the platform. For each of N opportunities (users):

```
1. Generate user embedding + timestamp + diurnal multiplier
2. Compute CTR/CVR for every (user, seller) pair:
     relevance = dot(user_embed, seller_ad_embed)
     CTR = sigmoid(relevance) × base_ctr × diurnal_multiplier
     CVR = sigmoid(relevance/2) × base_cvr
3. Each seller places a bid (via their policy)
4. Regulator screens out low-quality/low-bid sellers
5. Auction mechanism allocates slots & computes prices
6. Apply position bias: actual_ctr = ctr × slot_multiplier[position]
7. Simulate click (random < actual_ctr)
8. If clicked → simulate conversion (random < cvr)
9. Winner pays: price × clicked (pay-per-click)
10. Update seller spend/clicks/conversions/revenue
```

Returns: `(sellers_df, metrics_df)` — aggregated stats

### 3.8 `simulation/tasks.py` — Distributed Execution

```python
@celery_app.task
def run_block(cfg_json, seed, offset):
    # Runs simulate_block() as a Celery task
    # Multiple blocks can run in parallel via Redis

def run_distributed(cfg, run_id):
    # Splits opportunities into blocks, distributes via Celery
    # Aggregates results, saves to runs/{run_id}/
```

### 3.9 `cli.py` — Entry Point

```bash
auction-sim run --config configs/example.json            # Local mode
auction-sim run --config configs/example.json --distributed  # Celery mode
```

Outputs: `runs/{run_id}/sellers.parquet`, `runs/{run_id}/metrics.parquet`

---

## 4. AUCTIONGYM — THE NEWLY INTEGRATED GYMNASIUM ENVIRONMENT

**Location**: `auction-sim/src/auction_sim/gym_env/auction_env.py`
**Status**: ✅ COMPLETE AND TESTED

### 4.1 What It Does

Wraps the platform's auction logic into a **Gymnasium `gym.Env`** so that a single seller can interact with the auction step-by-step instead of running the whole simulation at once.

### 4.2 How It Maps to Existing Code

| Gym Concept | Platform Code It Uses |
|---|---|
| `reset()` | `UserGenerator.batch()`, `make_sellers()`, pre-computes CTR/CVR matrices |
| `step(bid)` | One iteration of `engine.py`'s inner loop — collects bids, runs `allocate()` + `prices_gsp/fp/vcg()`, simulates clicks/conversions |
| Background sellers | `RudimentaryPolicy` and `AutoBidPolicy` from `sellers.py` — compete automatically |
| Regulation | `Regulator.screen()` from `regulation.py` |
| User generation | `UserGenerator` from `users.py` + `features.py` for embeddings/sigmoid |

### 4.3 Interface Specification

```python
env = AuctionEnv(cfg=SimConfig, agent_seller_index=0, seed=42)

# OBSERVATION SPACE — Box(embed_dim + 6,)
# [0..15]  : user embedding (16 floats)
# [16]     : elapsed_frac — fraction of day elapsed [0, 1]
# [17]     : budget_frac — remaining budget as fraction [0, 1]
# [18]     : diurnal — traffic multiplier at this time of day
# [19]     : quality — agent's CTR-based quality score for this user
# [20]     : pcvr — predicted conversion rate for this user
# [21]     : n_competitors — number of background sellers with remaining budget

# ACTION SPACE — Box(1,) in [0, max_bid]
# A single float: the bid amount in ₹

# REWARD
# Won + clicked + converted: value_per_conversion - price_paid  (positive)
# Won + clicked + no conversion: -price_paid                    (negative)
# Won + no click: 0
# Lost auction: 0

# TERMINATION
# Budget exhausted OR all opportunities used up

obs, info = env.reset()
obs, reward, terminated, truncated, info = env.step(np.array([bid_amount]))
```

### 4.4 Info Dict Contents

```python
info = {
    "step": int,                    # Current step number
    "total_opportunities": int,     # Total users in episode
    "agent_spend": float,           # Cumulative spend
    "agent_budget": float,          # Daily budget
    "agent_remaining_budget": float,
    "agent_clicks": int,
    "agent_conversions": int,
    "agent_revenue": float,
    "agent_wins": int,
    "agent_roas": float,            # Revenue / Spend
    "auction": {                    # Per-step auction result
        "won": bool,
        "slot": int,                # -1 if lost
        "clicked": bool,
        "converted": bool,
        "price_paid": float,
        "reward": float,
    }
}
```

### 4.5 Registered as Gymnasium Environment

```python
import gymnasium as gym
import auction_sim.gym_env  # triggers registration

env = gym.make("AuctionEnv-v0", cfg=sim_config, seed=42)
```

### 4.6 Tests (8 tests, all passing ✅)

File: `tests/test_gym_env.py`

1. **test_env_creation** — spaces have correct shapes
2. **test_reset** — returns valid obs + info
3. **test_single_step** — step works, returns correct types
4. **test_full_episode** — runs all opportunities to completion
5. **test_zero_bid** — bidding 0 → never wins
6. **test_high_bid** — bidding very high → wins frequently
7. **test_gym_registry** — `gym.make("AuctionEnv-v0")` works
8. **test_reproducibility** — same seed → identical results

### 4.7 Demo Script

File: `scripts/demo_gym_env.py` — runs a full 10,000-step episode with a simple heuristic strategy and prints progress milestones + final results.

---

## 5. SELLER SIDE — NAVISHAA'S WORK (Separate Repo)

**Location**: `seller/resint/src/auction_sim/`
**Status**: ✅ COMPLETE (standalone)

### 5.1 Key Differences from Platform sellers.py

Navishaa's `sellers.py` has a fundamentally different, richer seller model:

#### Campaign Abstraction (new)
```python
@dataclass
class Campaign:
    name: str
    daily_budget: float
    base_bid: float
    spent: float = 0.0
    def remaining_budget(self): return max(0, daily_budget - spent)
```

#### Seller Class (redesigned)
- Has `campaigns` list (initialized in `__post_init__`)
- `bid()` returns `(bid_amount, campaign)` tuple — checks campaign budget first
- `observe_and_adapt(click, conv, price, elapsed_frac)` — **adapts bid_shading after every auction**
- `get_log_snapshot(elapsed_frac)` — captures state for time-series logging
- `charge(price, campaign)` — compatibility stub

#### Five Bidding Personas

| Policy | Strategy | Adaptation Rule |
|---|---|---|
| `aggressive` | Spend 5% ahead of clock | Micro-increase shading (×1.0001) when behind target |
| `roi_driven` | Target ROAS = 4.0 | Decrease when ROAS < 4.0, increase when above |
| `conservative` | Stay exactly on schedule | Decrease if overspending, barely increase otherwise |
| `risk_averse` | Penalize non-converting clicks | Decrease on paid click without conversion, increase on conversion |
| `exploratory` | Random walk discovery | Apply random noise (0.9998–1.0002) each step |

All shading clamped to [0.01, 5.0].

#### Engine Modifications
Navishaa's `engine.py`:
- Calls `seller.observe_and_adapt()` for ALL sellers after every auction (winners get real data, losers get zeros)
- Logs history snapshots every 1,000 steps
- Returns 3-tuple: `(sellers_df, metrics_df, history_df)` instead of 2-tuple
- `aggregate()` handles the 3-tuple and recalculates ROAS correctly

#### Config
Uses 5 sellers with ₹200 daily budget each, 2 slots, GSP mechanism, 300K opportunities.

#### Results (latest run)
| Seller | Policy | Spend | ROAS | Revenue |
|---|---|---|---|---|
| seller_1 | aggressive | ₹215.72 | 1.39 | ₹300 |
| seller_2 | roi_driven | ₹153.98 | **4.87** | ₹750 |
| seller_3 | conservative | ₹200.02 | **4.75** | ₹950 |
| seller_4 | risk_averse | ₹200.09 | 2.50 | ₹500 |
| seller_5 | exploratory | ₹200.18 | 4.25 | ₹850 |

---

## 6. THE GAP — WHAT'S NOT CONNECTED YET

Right now the two sides are **completely independent**:

```
PLATFORM (auction-sim/)              SELLER (seller/resint/)
┌───────────────────────┐            ┌───────────────────────┐
│ engine.py              │           │ engine.py              │
│ mechanisms.py          │           │ mechanisms.py          │
│ sellers.py (simple)    │           │ sellers.py (rich)      │
│ AuctionGym (new)       │           │ 5 personas             │
│                        │     ???   │ observe_and_adapt()    │
│ obs → bid → reward     │◄────────►│ Campaign objects       │
│                        │           │ history logging        │
└───────────────────────┘            └───────────────────────┘
       No connection between them yet
```

The platform's `sellers.py` has basic `RudimentaryPolicy` and `AutoBidPolicy`.
The seller's `sellers.py` has rich `Campaign`, 5 adaptive policies, `observe_and_adapt()`.

**They share the same config schema** (`SellerConfig`, `WorldConfig`) and the **same auction mechanics** (`mechanisms.py`, `regulation.py`), but the seller-side code is not integrated into the platform.

---

## 7. NEXT TASK — SELLER CAMPAIGN MANAGEMENT

### 7.1 The Problem

Currently a "seller" is just a flat config:
```json
{
    "id": "A",
    "daily_budget": 20000,
    "value_per_conversion": 50,
    "base_bid_shading": 0.8,
    "policy": "auto"
}
```

In a real ad platform, sellers register **campaigns** with the platform. A campaign is a structured agreement:

- **What** the seller is advertising (ad creative, product, targeting)
- **Who** to show it to (targeting criteria — segments, keywords, demographics)
- **How much** to spend (daily budget, lifetime budget, bid caps)
- **What goal** to optimize for (CPC, CPA, ROAS target)
- **When** to run (start/end dates, dayparting schedules)
- **How** to bid (manual bidding, auto-bidding, bid strategies)

### 7.2 What Needs To Be Built

A **Campaign Management layer** that sits between the platform and seller:

```
┌─────────────────────────────────────────────────────────────────┐
│                     CAMPAIGN MANAGER (NEW)                       │
│                                                                  │
│  Seller registers campaign ──► CampaignConfig validated          │
│  Platform loads campaigns  ──► Feeds into AuctionEnv             │
│  During auction:                                                 │
│    Campaign provides bid strategy + targeting + budget rules     │
│  After auction:                                                  │
│    Campaign receives outcome feedback                            │
│    Campaign updates internal state (Navishaa's observe_and_adapt)│
│                                                                  │
│  This bridges:                                                   │
│    Platform's AuctionEnv ←→ Seller's Campaign/Policy logic       │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Specifically

1. **`CampaignConfig` model** — Pydantic schema for campaigns (extends current `SellerConfig` with targeting, scheduling, goal types, bid strategy config)
2. **`CampaignManager`** — manages multiple campaigns per seller, validates them, tracks state
3. **Integration with `AuctionEnv`** — campaigns as background sellers, or campaigns as the agent itself
4. **Integration with seller-side policies** — Navishaa's 5 personas should be pluggable as campaign bid strategies
5. **Campaign lifecycle** — start, pause, budget exhaustion, end

### 7.4 Theory/Reading Material Needed

The student (Ayush) has reading material for campaign management theory that will inform the design. This needs to be discussed before implementation.

---

## 8. DEPENDENCY SETUP

### Virtual Environment
```bash
cd /home/ayush/Desktop/sem6/BTP/auction-sim
source .venv/bin/activate    # Python 3.12
```

### Installed Packages
```
numpy, pandas, scipy, pydantic, click, pyarrow, gymnasium (1.2.3)
+ auction-sim installed in editable mode (pip install -e .)
```

### Running Tests
```bash
cd auction-sim && source .venv/bin/activate
python3 tests/test_gym_env.py         # 8 tests, all pass
```

### Running Demo
```bash
python3 scripts/demo_gym_env.py       # Full episode with simple strategy
```

### Running Original Simulation
```bash
auction-sim run --config configs/example.json   # Batch mode (no gym)
```

---

## 9. FILE-BY-FILE REFERENCE

### Platform Side (auction-sim/)

| File | Lines | What It Does |
|---|---|---|
| `src/auction_sim/config.py` | ~50 | Pydantic config: WorldConfig, SellerConfig, SimConfig |
| `src/auction_sim/market/users.py` | ~25 | UserGenerator: random embeddings + timestamps + diurnal pattern |
| `src/auction_sim/market/sellers.py` | ~80 | Seller dataclass, RudimentaryPolicy, AutoBidPolicy, PacingController, make_sellers() |
| `src/auction_sim/auction/mechanisms.py` | ~50 | allocate(), prices_gsp(), prices_first_price(), prices_vcg() |
| `src/auction_sim/auction/regulation.py` | ~12 | Regulator.screen() — quality/bid floor enforcement |
| `src/auction_sim/utils/features.py` | ~12 | unit_embeddings(), sigmoid() |
| `src/auction_sim/simulation/engine.py` | ~120 | simulate_block() — core loop, aggregate() |
| `src/auction_sim/simulation/tasks.py` | ~45 | Celery task wrapper, run_distributed() |
| `src/auction_sim/cli.py` | ~45 | Click CLI: `auction-sim run` |
| `src/auction_sim/analysis.py` | ~25 | compare() — t-test between two runs |
| `src/auction_sim/gym_env/__init__.py` | ~6 | Registers AuctionEnv-v0 with Gymnasium |
| `src/auction_sim/gym_env/auction_env.py` | ~410 | **AuctionEnv** — Gym environment wrapping the platform |
| `tests/test_gym_env.py` | ~180 | 8 tests for AuctionEnv |
| `scripts/demo_gym_env.py` | ~120 | Demo: full episode with heuristic bidding |
| `configs/example.json` | ~50 | Default config: 3 sellers, 300K opps, GSP |

### Seller Side (seller/resint/)

| File | Lines | What It Does |
|---|---|---|
| `src/auction_sim/market/sellers.py` | ~150 | **Campaign + Seller (rich)** — 5 policies, observe_and_adapt(), history logging |
| `src/auction_sim/simulation/engine.py` | ~157 | Modified engine — calls observe_and_adapt(), logs history, returns 3-tuple |
| `src/auction_sim/simulation/tasks.py` | Modified | Handles 3-tuple, saves history.csv |
| `configs/example.json` | ~80 | 5 sellers (aggressive, roi_driven, conservative, risk_averse, exploratory), ₹200 budget each |
| `visualize_results.py` | ~40 | Plots bid shading over time per policy |

---

## 10. SUMMARY OF WHAT'S DONE VS WHAT'S NEXT

| Component | Status | Location |
|---|---|---|
| Core auction engine | ✅ Done | `auction-sim/src/auction_sim/simulation/engine.py` |
| Auction mechanisms (GSP/VCG/FP) | ✅ Done | `auction-sim/src/auction_sim/auction/mechanisms.py` |
| Platform regulation | ✅ Done | `auction-sim/src/auction_sim/auction/regulation.py` |
| User generation | ✅ Done | `auction-sim/src/auction_sim/market/users.py` |
| Basic seller policies | ✅ Done | `auction-sim/src/auction_sim/market/sellers.py` |
| Config schema | ✅ Done | `auction-sim/src/auction_sim/config.py` |
| CLI + distributed execution | ✅ Done | `auction-sim/src/auction_sim/cli.py` + `tasks.py` |
| **AuctionGym (Gymnasium env)** | ✅ Done | `auction-sim/src/auction_sim/gym_env/auction_env.py` |
| AuctionGym tests | ✅ Done | `auction-sim/tests/test_gym_env.py` |
| Rich seller policies (5 personas) | ✅ Done (Navishaa) | `seller/resint/src/auction_sim/market/sellers.py` |
| Seller history/visualization | ✅ Done (Navishaa) | `seller/resint/visualize_results.py` |
| **Campaign Management** | ❌ NEXT TASK | Needs theory discussion → then implementation |
| **Platform ↔ Seller Integration** | ❌ NEXT TASK | Bridge AuctionGym with Navishaa's seller code |
| CTR/CVR ML Pipeline | ❌ Future | After campaign data flows |
| RL Agent Training | ❌ Future | After campaign integration |
