from dataclasses import dataclass, field
import numpy as np

@dataclass
class Campaign:
    id: str
    daily_budget: float
    base_bid_shading: float  # Dynamic over time
    policy: str
    spent: float = 0.0
    revenue: float = 0.0
    clicks: int = 0
    conv: int = 0

    def remaining_budget(self):
        return max(0.0, self.daily_budget - self.spent)

class Strategy:
    """Base strategy for campaign bid adaptation."""
    def adapt(self, campaign: Campaign, click: int, conv: int, price: float, elapsed_frac: float):
        pass

class AggressiveStrategy(Strategy):
    def adapt(self, campaign: Campaign, click: int, conv: int, price: float, elapsed_frac: float):
        if campaign.daily_budget > 0 and (campaign.spent / campaign.daily_budget) < (elapsed_frac + 0.05):
            campaign.base_bid_shading *= 1.0001

class ROIDrivenStrategy(Strategy):
    def adapt(self, campaign: Campaign, click: int, conv: int, price: float, elapsed_frac: float):
        current_roas = (campaign.revenue / campaign.spent) if campaign.spent > 1.0 else 4.0
        if current_roas < 4.0:
            campaign.base_bid_shading *= 0.9999
        else:
            campaign.base_bid_shading *= 1.00005

class ConservativeStrategy(Strategy):
    def adapt(self, campaign: Campaign, click: int, conv: int, price: float, elapsed_frac: float):
        if campaign.daily_budget > 0 and (campaign.spent / campaign.daily_budget) > elapsed_frac:
            campaign.base_bid_shading *= 0.9999
        else:
            campaign.base_bid_shading *= 1.00002

class RiskAverseStrategy(Strategy):
    def adapt(self, campaign: Campaign, click: int, conv: int, price: float, elapsed_frac: float):
        if price > 0 and conv == 0:
            campaign.base_bid_shading *= 0.9999
        elif conv > 0:
            campaign.base_bid_shading *= 1.0002

class ExploratoryStrategy(Strategy):
    def adapt(self, campaign: Campaign, click: int, conv: int, price: float, elapsed_frac: float):
        noise = np.random.uniform(0.9998, 1.0002)
        campaign.base_bid_shading *= noise

class StrategyFactory:
    @staticmethod
    def create(policy_name: str) -> Strategy:
        strategies = {
            "aggressive": AggressiveStrategy(),
            "roi_driven": ROIDrivenStrategy(),
            "conservative": ConservativeStrategy(),
            "risk_averse": RiskAverseStrategy(),
            "exploratory": ExploratoryStrategy(),
        }
        return strategies.get(policy_name, Strategy())

@dataclass
class Seller:
    id: str
    brand: str
    value_per_conversion: float
    cogs_ratio: float
    seed: int
    d: int
    ad_vec: np.ndarray
    campaigns: list[Campaign] = field(default_factory=list)
    spend: float = 0.0
    clicks: int = 0
    conv: int = 0
    revenue: float = 0.0
    
    _strategies: dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        self._strategies = {c.id: StrategyFactory.create(c.policy) for c in self.campaigns}

    @property
    def daily_budget(self) -> float:
        return sum(c.daily_budget for c in self.campaigns)

    def bid(self, p_ctr, p_cvr, elapsed_frac):
        active_campaign = None
        for c in self.campaigns:
            if c.remaining_budget() > 0:
                active_campaign = c
                break
                
        if not active_campaign:
            return 0.0, None

        v = self.value_per_conversion * p_cvr
        bid_value = active_campaign.base_bid_shading * v
        return bid_value, active_campaign

    def observe_and_adapt(self, active_campaign: Campaign, click: int, conv: int, price: float, elapsed_frac: float):
        if not active_campaign:
            return

        self.spend += price
        self.clicks += int(click)
        self.conv += int(conv)
        rev_gain = int(conv) * self.value_per_conversion
        self.revenue += rev_gain
        
        active_campaign.spent += price
        active_campaign.clicks += int(click)
        active_campaign.conv += int(conv)
        active_campaign.revenue += rev_gain
        
        strategy = self._strategies.get(active_campaign.id)
        if strategy:
            strategy.adapt(active_campaign, click, conv, price, elapsed_frac)
            
        active_campaign.base_bid_shading = np.clip(active_campaign.base_bid_shading, 0.01, 5.0)

def make_sellers(cfg, d, seed):
    r = np.random.default_rng(seed)
    out = []
    for sc in cfg.sellers:
        vec = r.normal(0, 1, size=d)
        vec /= np.linalg.norm(vec) + 1e-8
        
        campaigns = []
        for cc in sc.campaigns:
            campaigns.append(Campaign(
                id=cc.id,
                daily_budget=cc.daily_budget,
                base_bid_shading=cc.base_bid_shading,
                policy=cc.policy
            ))
            
        out.append(
            Seller(
                id=sc.id,
                brand=sc.brand,
                value_per_conversion=sc.value_per_conversion,
                cogs_ratio=sc.cogs_ratio,
                seed=sc.seed,
                d=d,
                ad_vec=vec,
                campaigns=campaigns
            )
        )
    return out
