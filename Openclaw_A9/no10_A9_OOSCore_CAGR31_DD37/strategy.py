from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common import run_a9_hybrid_backtest, print_report

STRATEGY_NAME = 'No10 · A9 OOSCore'
PARAMS = {'downside_window': 18, 'target_down_vol_strong': 0.325, 'target_down_vol_weak': 0.325, 'max_lev': 2.5, 'ema_fast': 60, 'ema_slow': 190, 'dd_window': 84, 'dd_soft': 0.14, 'dd_lev_cut': 0.35, 'panic_window': 20, 'panic_thr': 0.0, 'bond_lookback': 84, 'bond_lev': 0.5, 'rf_annual': 0.06, 'strong_months': [11, 12, 1, 2, 3, 4]}

if __name__ == "__main__":
    result = run_a9_hybrid_backtest(STRATEGY_NAME, PARAMS, Path(__file__).resolve().parent)
    print_report(STRATEGY_NAME, result)
