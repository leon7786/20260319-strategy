from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common import run_backtest, print_report

# Top1 · AlphaPulse
PARAMS = {'tw': 12, 'rvw': 3, 'tvs': 0.18, 'tvw': 0.12, 'minl': 0.1, 'maxl': 3.0, 'bmult': 2.0, 'blook': 9, 'cost': 0.0015, 'slip': 0.0005}

if __name__ == "__main__":
    result = run_backtest(PARAMS)
    print_report("Top1 · AlphaPulse", result)
