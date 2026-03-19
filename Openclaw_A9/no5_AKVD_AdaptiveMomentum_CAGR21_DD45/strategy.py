from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common import run_akvd_backtest, print_report

STRATEGY_NAME = 'No5 · AKVD AdaptiveMomentum'
PARAMS = {'ema_fast': 50, 'ema_slow': 200, 'mom_63_w': 0.2, 'mom_126_w': 0.3, 'mom_252_w': 0.5, 'target_vol': 0.4, 'max_leverage': 3.0, 'vol_window': 20}

if __name__ == "__main__":
    result = run_akvd_backtest(STRATEGY_NAME, Path(__file__).resolve().parent, PARAMS)
    print_report(STRATEGY_NAME, result)
