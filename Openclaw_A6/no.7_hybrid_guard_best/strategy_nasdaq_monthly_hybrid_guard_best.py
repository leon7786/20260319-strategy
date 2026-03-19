#!/usr/bin/env python3
from strategy_nasdaq_monthly_hybrid_guard_runner import run_hybrid_guard_strategy

STRATEGY_ID = 'hybrid_dd-0.18_rec-0.04_dtv0.08_dmax2.5_dmin1.0_ax0.02_am0.15_av0.06'

if __name__ == '__main__':
    result = run_hybrid_guard_strategy(
        strategy_id=STRATEGY_ID,
        dd_guard=-0.18,
        recovery_threshold=-0.04,
        defense_target_vol=0.08,
        defense_max_lev=2.5,
        defense_min_lev=1.0,
        attack_extra_target_vol=0.02,
        attack_mom_threshold=0.15,
        attack_vol_cap=0.06,
    )
    print(result['summary'])
