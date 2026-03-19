from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from common_advanced import run_advanced_backtest, segment_metrics, print_report

PARAMS = {
    'ma_w': 294, 'mom_w': 20, 'mom_thr': 0.0, 'vol_w': 21,
    'tv_str': 0.22, 'tv_wk': 0.16, 'min_lev': 0.1, 'max_lev': 3.0,
    'blook': 84, 'bmult': 2.0, 'slip': 0.0008, 'month_cost': 0.0015,
    'dd_w': 252, 'dd_thr': -0.30, 'dd_lev_cut': 0.8,
    'panic_mom_w': 20, 'panic_mom_thr': 0.0
}

if __name__ == "__main__":
    result = run_advanced_backtest(PARAMS)
    print_report("S5_Alpha_Strike", result)

    oos = segment_metrics(result['nav'], '2015-01-01')
    print("\n[OOS 2015-2025]")
    print(f"Final Value : ${oos['final_value']:,.0f}")
    print(f"Total Return: {oos['total_return']*100:,.1f}%")
    print(f"CAGR       : {oos['cagr']*100:.2f}%")
    print(f"Max DD     : {oos['max_dd']*100:.2f}%")
    print(f"Sharpe     : {oos['sharpe']:.2f}")
