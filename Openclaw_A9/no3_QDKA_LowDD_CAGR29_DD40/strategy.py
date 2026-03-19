from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common import run_qdka_backtest, print_report

STRATEGY_NAME = 'No3 · QDKA LowDD'
PARAMS = {'downside_window': 14, 'target_down_vol': 0.325, 'max_lev': 2.5, 'ema_fast': 50, 'ema_slow': 190, 'dd_window': 84, 'dd_cut': 0.14, 'rf_annual': 0.06}

if __name__ == "__main__":
    result = run_qdka_backtest(STRATEGY_NAME, PARAMS, Path(__file__).resolve().parent)
    print_report(STRATEGY_NAME, result)
