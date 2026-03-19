#!/usr/bin/env python3
from strategy_nasdaq_monthly_latest_runner import run_strategy

STRATEGY_ID = 'hybrid_dd-0.18_rec-0.04_dtv0.08_dmax2.5_dmin1.0_ax0.02_am0.15_av0.06'

if __name__ == '__main__':
    result = run_strategy(
        strategy_id=STRATEGY_ID,
        lookback=13,
        base_target_vol=0.15,
        attack_target_vol=0.17,
        attack_max_lev=4.5,
        min_lev=1.0,
        crash_filter=-0.09,
        attack_mom_threshold=0.15,
        attack_vol_cap=0.06,
        attack_hold_months=0,
        carry_mode='full',
    )
    print(result['summary'])
