#!/usr/bin/env python3
from common import StrategyConfig, backtest_strategy, print_summary, save_outputs

CONFIG = StrategyConfig(
    name="Top2_39.95pct_Mix10_3x",
    la=8.01,
    thr=0.1952011747,
    lev_low=0.1643266466,
    lev_high=3.00,
    w_trend=0.3599906019,
    w_short=0.2977751372,
    w_vol=0.3265232357,
    w_dd=0.0157110253,
    mom_cap=0.1593122767,
    short_w=2,
    short_cap=0.1786462737,
    vol_w=2,
    vol_lo=0.0125245696,
    vol_hi=0.0273133989,
    dd_w=9,
    dd_floor=-0.1807888320,
    bond_alpha=0.1,
    bond_mult=3.0,
)

if __name__ == "__main__":
    df, summary = backtest_strategy(CONFIG)
    out_dir = save_outputs(CONFIG, df, summary)
    print_summary(summary)
    print(f"输出目录: {out_dir}")
