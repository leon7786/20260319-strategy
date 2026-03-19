#!/usr/bin/env python3
from strategy_nasdaq_monthly_refine_runner import run_strategy

STRATEGY_ID = 'refine_m13_13_vw2_tv0.15_max4.5_min2.0_b0.0_cr-0.09_cd1_bond2x_pos'

if __name__ == '__main__':
    result = run_strategy(
        strategy_id=STRATEGY_ID,
        mom_fast=13,
        mom_slow=13,
        vol_window=2,
        target_vol=0.15,
        max_lev=4.5,
        min_lev=2.0,
        bonus=0.0,
        crash_filter=-0.09,
        crash_cooldown=1,
    )
    print(result['summary'])
