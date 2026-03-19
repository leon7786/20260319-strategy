#!/usr/bin/env python3
from strategy_nasdaq_monthly_latest_runner import run_strategy

STRATEGY_ID = 'refine_attack_lb13_vw2_btv0.15_atv0.26_amax4.5_min2.0_cr-0.09_cd1_am0.12_av0.07'

if __name__ == '__main__':
    result = run_strategy(
        strategy_id=STRATEGY_ID,
        lookback=13,
        base_target_vol=0.15,
        attack_target_vol=0.26,
        attack_max_lev=4.5,
        min_lev=2.0,
        crash_filter=-0.09,
        attack_mom_threshold=0.12,
        attack_vol_cap=0.07,
        attack_hold_months=0,
        carry_mode='full',
    )
    print(result['summary'])
