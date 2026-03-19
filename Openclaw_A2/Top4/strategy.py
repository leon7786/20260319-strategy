from common import run_backtest, print_report

# Top4 by CAGR
PARAMS = {
    "tw": 12,
    "rvw": 3,
    "tvs": 0.16,
    "tvw": 0.12,
    "minl": 0.1,
    "maxl": 3.0,
    "bmult": 2.0,
    "blook": 9,
    "cost": 0.0015,
    "slip": 0.0010,
}

if __name__ == "__main__":
    result = run_backtest(PARAMS)
    print_report("Top4", result)
