# AuctionSim-Py (RL Ready)

A multi-slot ad auction environment built in Python.

This project is designed to train **Reinforcement Learning (RL) agents** to bid optimally against highly dynamic, theory-backed background competitors in a simulated ad exchange.

## Features
- **Gymnasium Environment:** Includes `AuctionEnv-v0` for dropping straight into standard RL libraries (PPO, DQN, SAC).
- **Campaign Management:** Background sellers run decoupled campaigns using dynamic mathematical Strategies (Aggressive, ROI-Driven, Conservative, Risk-Averse, Exploratory).
- **Algorithmic Marketing Theory:** Built to simulate real market dynamics where competitors actively adapt their bid shading multipliers via real-time feedback (spend, clicks, conversions) as the day progresses.
- **Fast Simulated Users:** Generates millions of simulated user embeddings with distinct CTR/CVR responses.

## Quick Start (RL Agent Training)

The core focus of this repository is training an RL agent. To get started with the Gymnasium environment, just install the local package:

```bash
# 1. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install the package
pip install -e .
pip install gymnasium
```

You can then test the environment in your Python scripts:

```python
import gymnasium as gym
import auction_sim.gym_env # Registers the environment
from auction_sim.config import SimConfig

# Load your configuration
with open("configs/example.json") as f:
    cfg = SimConfig.model_validate_json(f.read())

# Create the training environment
env = gym.make("AuctionEnv-v0", cfg=cfg, agent_seller_index=0)
obs, info = env.reset()

# Standard RL training loop...
action = env.action_space.sample()
obs, reward, terminated, truncated, info = env.step(action)
```

---

## Legacy/Batch Simulation Mode (Optional: Celery & Redis)

Before the Gymnasium environment was added, this platform was built as a static, large-scale parallel simulator. If you just want to generate millions of rows of Parquet/CSV market data (without Training an RL agent), you can use the distributed `cli.py` tool.

This massive scale generation requires **Redis** and **Celery**.

### 1) Install and start Redis
If you want to use the distributed data generator, you need Redis running. The fastest way is Docker:
```bash
docker compose up -d redis
```
*(Or install natively via `apt`/`brew` depending on your OS)*

### 2) Start a Celery worker
Celery allows the platform to simulate different chunks of users (batches) simultaneously across multiple CPU cores.
```bash
celery -A auction_sim.simulation.tasks worker --loglevel INFO
```

### 3) Run a distributed simulation
```bash
python -m auction_sim.cli run --config configs/example.json --distributed
```

### 4) Inspect outputs
Outputs are saved as aggregated metrics:
```
runs/<timestamp>/sellers.parquet
runs/<timestamp>/metrics.parquet
```

**Note:** You do **not** need to run Redis or Celery to train your RL agent using `AuctionEnv`. They are purely for large-scale data generation!

