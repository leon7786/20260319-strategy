import pandas as pd
import numpy as np
from pathlib import Path

INIT_CASH = 10_000.0
START = pd.Timestamp("1995-01-03")
END = pd.Timestamp("2025-12-29")
TRADING_DAYS_PER_MONTH = 21
TRADING_DAYS_PER_YEAR = 252


def _resolve_data_paths():
    import os
    repo_root = Path(__file__).resolve().parents[1]
    candidate_dirs = []
    env_dir = os.getenv("STRATEGY_DATA_DIR")
    if env_dir:
        candidate_dirs.append(Path(env_dir))
    candidate_dirs.append(repo_root / "data")
    candidate_dirs.append(Path("/root/projects/20260318IXIC/data"))

    for d in candidate_dirs:
        ix = d / "IXIC_daily_yf.csv"
        bd = d / "VUSTX_daily_yf.csv"
        if ix.exists() and bd.exists():
            return ix, bd

    raise FileNotFoundError(
        "找不到 IXIC_daily_yf.csv / VUSTX_daily_yf.csv。"
        "可设置 STRATEGY_DATA_DIR 或把数据放到 repo/data/"
    )


def load_daily_data(start=START, end=END):
    ixic_path, bond_path = _resolve_data_paths()

    ixic = (
        pd.read_csv(ixic_path, parse_dates=["Date"])
        .set_index("Date")
        .sort_index()["Close"]
        .rename("IXIC")
    )
    bond = (
        pd.read_csv(bond_path, parse_dates=["Date"])
        .set_index("Date")
        .sort_index()["Close"]
        .rename("BOND")
    )

    df = pd.concat([ixic, bond], axis=1).dropna()
    df = df[(df.index >= start) & (df.index <= end)]
    return df


def _metrics(nav: pd.Series):
    years = (nav.index[-1] - nav.index[0]).days / 365.25
    cagr = (nav.iloc[-1] / nav.iloc[0]) ** (1 / years) - 1
    max_dd = ((nav / nav.cummax()) - 1).min()
    daily_ret = nav.pct_change().dropna()
    sharpe = np.sqrt(TRADING_DAYS_PER_YEAR) * daily_ret.mean() / (daily_ret.std() + 1e-9)
    total_return = nav.iloc[-1] / nav.iloc[0] - 1
    return {
        "final_value": nav.iloc[-1],
        "total_return": total_return,
        "cagr": cagr,
        "max_dd": max_dd,
        "sharpe": sharpe,
    }


def run_advanced_backtest(params: dict, start=START, end=END):
    """
    Advanced Daily Backtest (anti-lookahead)
    规则核心：
    - t-1 日信号 -> t 日执行
    - close 信号 + close 近似执行
    - 动态杠杆 + drawdown 降杠杆 + panic filter
    """
    df = load_daily_data(start=start, end=end)
    ix = df["IXIC"]
    bond = df["BOND"]

    rix = ix.pct_change().fillna(0.0)
    rb = bond.pct_change().fillna(0.0)

    ma = ix.rolling(params["ma_w"]).mean()
    mom = ix / ix.shift(params["mom_w"]) - 1
    vol = rix.rolling(params["vol_w"]).std()
    rolling_high = ix.rolling(params["dd_w"]).max()

    bond_mom = bond / bond.shift(params["blook"]) - 1
    panic_mom = ix / ix.shift(params["panic_mom_w"]) - 1

    cost_daily = params["month_cost"] / TRADING_DAYS_PER_MONTH
    bond_cost_daily = (0.0006 * params["bmult"]) / TRADING_DAYS_PER_MONTH

    tv_str_daily = params["tv_str"] / np.sqrt(TRADING_DAYS_PER_MONTH)
    tv_wk_daily = params["tv_wk"] / np.sqrt(TRADING_DAYS_PER_MONTH)

    idx = df.index
    nav = np.full(len(df), np.nan)
    nav[0] = INIT_CASH

    value = INIT_CASH
    in_risk = False

    for i in range(1, len(df)):
        # season target volatility
        month = idx[i - 1].month
        target_vol = tv_str_daily if month in (11, 12, 1, 2, 3, 4) else tv_wk_daily

        # signal at t-1
        risk_on = False
        if pd.notna(ma.iloc[i - 1]) and pd.notna(mom.iloc[i - 1]):
            risk_on = (ix.iloc[i - 1] > ma.iloc[i - 1]) and (mom.iloc[i - 1] > params["mom_thr"])

        # panic filter
        if pd.notna(panic_mom.iloc[i - 1]) and panic_mom.iloc[i - 1] < params["panic_mom_thr"]:
            risk_on = False

        # dynamic leverage at t-1
        lev = params["min_lev"]
        if pd.notna(vol.iloc[i - 1]) and vol.iloc[i - 1] > 1e-12:
            lev = target_vol / vol.iloc[i - 1]
        lev = max(params["min_lev"], min(params["max_lev"], lev))

        # drawdown-based de-leveraging
        if pd.notna(rolling_high.iloc[i - 1]) and rolling_high.iloc[i - 1] > 0:
            idx_dd = ix.iloc[i - 1] / rolling_high.iloc[i - 1] - 1
            if idx_dd < params["dd_thr"]:
                lev = max(
                    params["min_lev"],
                    min(params["max_lev"], lev * params["dd_lev_cut"]),
                )

        turnover = 1.0 if risk_on != in_risk else 0.0
        in_risk = risk_on

        if risk_on:
            value *= (1 + rix.iloc[i] * lev - cost_daily * lev - params["slip"] * turnover)
        else:
            if pd.notna(bond_mom.iloc[i - 1]) and bond_mom.iloc[i - 1] > 0:
                value *= (1 + rb.iloc[i] * params["bmult"] - bond_cost_daily - params["slip"] * turnover)
            else:
                value *= (1 - params["slip"] * turnover)

        value = max(value, 1.0)
        nav[i] = value

    nav = pd.Series(nav, index=idx, name="NAV")
    m = _metrics(nav)
    return {
        "params": params,
        "final_value": m["final_value"],
        "total_return": m["total_return"],
        "cagr": m["cagr"],
        "max_dd": m["max_dd"],
        "sharpe": m["sharpe"],
        "nav": nav,
    }


def segment_metrics(nav: pd.Series, start_date: str):
    sub = nav[nav.index >= pd.Timestamp(start_date)]
    if len(sub) < 30:
        raise ValueError("segment too short")

    rebased = sub / sub.iloc[0] * INIT_CASH
    m = _metrics(rebased)
    return {
        "final_value": m["final_value"],
        "total_return": m["total_return"],
        "cagr": m["cagr"],
        "max_dd": m["max_dd"],
        "sharpe": m["sharpe"],
    }


def print_report(name: str, result: dict):
    print(f"\n=== {name} ===")
    print("params:", result["params"])
    print(f"Final Value : ${result['final_value']:,.0f}")
    print(f"Total Return: {result['total_return']*100:,.1f}%")
    print(f"CAGR       : {result['cagr']*100:.2f}%")
    print(f"Max DD     : {result['max_dd']*100:.2f}%")
    print(f"Sharpe     : {result['sharpe']:.2f}")
