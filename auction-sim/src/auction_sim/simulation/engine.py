import numpy as np
import pandas as pd

from auction_sim.auction.mechanisms import allocate, prices_first_price, prices_gsp, prices_vcg
from auction_sim.auction.regulation import Regulator
from auction_sim.config import SimConfig
from auction_sim.market.sellers import make_sellers
from auction_sim.market.users import UserGenerator
from auction_sim.utils.features import sigmoid


def simulate_block(cfg: SimConfig, seed: int, start_offset: int):
    r = np.random.default_rng(seed)
    w = cfg.world
    ug = UserGenerator(
        w.embedding_dim, w.base_ctr, w.base_cvr, w.diurnal_amplitude, w.noise_std, seed
    )
    sellers = make_sellers(cfg, w.embedding_dim, seed + 1)
    k = w.slots
    slot_m = np.array(w.slot_multipliers[:k])
    ts0 = w.start_ts + start_offset
    n = w.batch_size
    u, ts, diurnal = ug.batch(n, ts0, w.horizon_hours)
    S = len(sellers)
    A = np.stack([s.ad_vec for s in sellers], axis=0)
    Q = u @ A.T
    Q = (Q - Q.mean()) / (Q.std() + 1e-6)
    CTR = sigmoid(Q) * w.base_ctr * diurnal.reshape(-1, 1)
    CVR = sigmoid(Q / 2) * w.base_cvr
    spent = np.zeros(S)
    clicks = np.zeros(S)
    conv = np.zeros(S)
    revenue = np.zeros(S)
    ux_acc = 0.0
    rev_acc = 0.0
    welfare_acc = 0.0
    mech = w.mechanism
    reg = Regulator(w.regulation.min_quality, w.regulation.min_bid, w.regulation.reserve_cpc)
    for t in range(n):
        ctr_row = CTR[t]
        cvr_row = CVR[t]
        bids = np.zeros(S)
        qs = (ctr_row / ctr_row.max()) if ctr_row.max() > 0 else ctr_row + 1e-9
        elapsed = (ts[t] - w.start_ts) / (w.horizon_hours * 3600)
        # 1. Bids Phase
        for i, s in enumerate(sellers):
            b, active_campaign = s.bid(ctr_row[i], cvr_row[i], elapsed)
            bids[i] = b

        bids, qs = reg.screen(bids, qs)
        if mech == "first_price":
            idx, _ = allocate(bids, qs, k)
            prices = prices_first_price(bids, idx)
        elif mech == "vcg":
            idx, prices = prices_vcg(bids, qs, slot_m)
        else:
            idx, _ = allocate(bids, qs, k)
            prices = prices_gsp(bids, qs, idx)
        prices = np.maximum(prices, w.regulation.reserve_cpc)

        # 2. Outcome Phase
        lm = slot_m[: len(idx)]
        ctr_show = ctr_row[idx] * lm
        click = r.random(len(idx)) < ctr_show
        conv_now = (r.random(len(idx)) < cvr_row[idx]) & click
        pay = prices * click

        # 3. Observe and Adapt Phase
        winners_map = {pos: j for j, pos in enumerate(idx)}
        for i, s in enumerate(sellers):
            # The campaign needs to know what campaign was active during this bid
            # Since bid() only gives us the campaign, we should strictly pass it back or use the seller's state. 
            # In our new implementation, observe_and_adapt takes (active_campaign, click, conv, price, elapsed_frac)
            # But here `engine.py` does not track *which* campaign bid.
            # However, since a seller only has ONE active campaign at a time, we can re-evaluate or use the basic logic.
            # The best way is to fetch active campaign from the seller directly if it's the winner
            _, active_campaign = s.bid(ctr_row[i], cvr_row[i], elapsed)
            
            if i in winners_map:
                j = winners_map[i]
                c_click = int(click[j])
                c_conv = int(conv_now[j])
                c_pay = pay[j]
                
                s.observe_and_adapt(active_campaign, c_click, c_conv, c_pay, elapsed)
                
                spent[i] += c_pay
                clicks[i] += c_click
                conv[i] += c_conv
                rev_now = c_conv * s.value_per_conversion
                revenue[i] += rev_now
                welfare_acc += rev_now
                rev_acc += c_pay
            else:
                s.observe_and_adapt(active_campaign, 0, 0, 0.0, elapsed)
                
        ux_acc += ctr_show.mean() if len(idx) > 0 else 0.0
    data = {
        "seller_id": [s.id for s in sellers],
        "cogs_ratio": [s.cogs_ratio for s in sellers],
        "spend": spent,
        "clicks": clicks,
        "conversions": conv,
        "revenue": revenue,
    }
    df_s = pd.DataFrame(data)
    if w.metrics.roas_mode == "profit_over_spend":
        df_s["roas"] = df_s.apply(
            lambda r: ((r["revenue"] - r["spend"]) / r["spend"]) if r["spend"] > 0 else 0.0, axis=1
        )
    else:
        df_s["roas"] = df_s.apply(
            lambda r: (r["revenue"] / r["spend"]) if r["spend"] > 0 else 0.0, axis=1
        )
    if w.metrics.rocs_mode == "profit_after_cogs_over_spend":
        df_s["rocs"] = df_s.apply(
            lambda r: (((r["revenue"] * (1.0 - r["cogs_ratio"])) - r["spend"]) / r["spend"])
            if r["spend"] > 0
            else 0.0,
            axis=1,
        )
    else:
        df_s["rocs"] = df_s.apply(
            lambda r: (((r["revenue"] * (1.0 - r["cogs_ratio"])) - r["spend"]) / r["spend"])
            if r["spend"] > 0
            else 0.0,
            axis=1,
        )
    df_s["surplus"] = df_s["revenue"] - df_s["spend"]
    metrics = {
        "opportunities": n,
        "platform_revenue": rev_acc,
        "social_welfare": welfare_acc,
        "user_experience": ux_acc / n if n > 0 else 0.0,
        "mechanism": mech,
        "slots": k,
        "reserve_cpc": w.regulation.reserve_cpc,
        "ts_start": int(ts0),
        "ts_end": int(ts0) + n,
    }
    return df_s, pd.DataFrame([metrics])


def aggregate(results):
    sellers = []
    metrics = []
    for s, m in results:
        sellers.append(s)
        metrics.append(m)
    sf = (
        pd.concat(sellers, ignore_index=True)
        .groupby("seller_id", as_index=False)
        .sum(numeric_only=True)
    )
    tmp = pd.concat(metrics, ignore_index=True).sum(numeric_only=True)
    agg = tmp.to_frame().T
    return sf, agg
