from gymnasium.envs.registration import register

register(
    id="AuctionEnv-v0",
    entry_point="auction_sim.gym_env.auction_env:AuctionEnv",
)
