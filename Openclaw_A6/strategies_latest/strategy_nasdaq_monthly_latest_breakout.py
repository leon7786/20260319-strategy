#!/usr/bin/env python3
from strategy_nasdaq_monthly_latest_runner import run_strategy

STRATEGY_ID = 'breakout_lb13_vw2_ntv0.14_atv0.2_dtv0.08_max5.0_min1.5_cr-0.09_cd1_dd-0.15_am0.2_av0.06'

if __name__ == '__main__':
    result = run_strategy(
        strategy_id=STRATEGY_ID,
        lookback=13,
        base_target_vol=0.14,
        attack_target_vol=0.20,
        attack_max_lev=5.0,
        min_lev=1.5,
        crash_filter=-0.09,
        attack_mom_threshold=0.20,
        attack_vol_cap=0.06,
        attack_hold_months=0,
        carry_mode='full',
    )
    print(result['summary'])
