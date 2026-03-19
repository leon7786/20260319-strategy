import pandas as pd
import numpy as np
from pathlib import Path

INIT_CASH = 10_000.0
START = pd.Timestamp("1995-01-03")
END = pd.Timestamp("2025-12-29")
TRADING_DAYS_PER_MONTH = 21
TRADING_DAYS_PER_YEAR = 252


def _resolve_data_paths():
    """定位数据文件路径。"""
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


def load_daily_data():
    """加载 IXIC + VUSTX 日线，并对齐。"""
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
    df = df[(df.index >= START) & (df.index <= END)]
    return df["IXIC"], df["BOND"]


def _months_to_trading_days(months: float) -> int:
    return max(2, int(round(months * TRADING_DAYS_PER_MONTH)))


def run_backtest(params: dict):
    """
    params 字段（保留“月”语义，在内部转换为日度窗口）：
      tw, rvw, tvs, tvw, minl, maxl, bmult, blook, cost, slip

    - tw: 趋势窗口（月）
    - rvw: 波动率窗口（月）
    - blook: 债券动量窗口（月）
    - tvs/tvw: 月度目标波动率（内部换算为日度）
    - cost: 月度杠杆成本（内部按日分摊）
    - slip: 换仓滑点（每次状态切换生效）
    """
    ixic, bond = load_daily_data()
    ixic_ret = ixic.pct_change()
    bond_ret = bond.pct_change()

    tw_month = params["tw"]
    rvw_month = params["rvw"]
    blook_month = params["blook"]

    tw_days = _months_to_trading_days(tw_month)
    rvw_days = _months_to_trading_days(rvw_month)
    blook_days = _months_to_trading_days(blook_month)

    tvs_month = params["tvs"]
    tvw_month = params["tvw"]
    minl = params["minl"]
    maxl = params["maxl"]
    bmult = params["bmult"]
    cost_month = params["cost"]
    slip = params["slip"]

    # 月目标波动率 -> 日目标波动率
    tvs_daily = tvs_month / np.sqrt(TRADING_DAYS_PER_MONTH)
    tvw_daily = tvw_month / np.sqrt(TRADING_DAYS_PER_MONTH)

    # 月杠杆成本 -> 日杠杆成本
    cost_daily = cost_month / TRADING_DAYS_PER_MONTH

    # 1) 趋势开关（按日）
    signal_risk_on = ixic > ixic.rolling(tw_days).mean()

    # 2) 动态杠杆（0.1x ~ 3.0x）
    vol_floor_daily = 0.01 / np.sqrt(TRADING_DAYS_PER_MONTH)
    realized_vol = ixic_ret.rolling(rvw_days).std().clip(lower=vol_floor_daily)

    target_vol = pd.Series(tvw_daily, index=ixic.index)
    target_vol[ixic.index.month.isin([11, 12, 1, 2, 3, 4])] = tvs_daily
    leverage = (target_vol / realized_vol).clip(lower=minl, upper=maxl)

    # 3) 风险外资产（债券动量过滤，按日）
    bond_mom = ((1 + bond_ret).rolling(blook_days).apply(np.prod, raw=True) - 1).shift(1)
    bond_cost_daily = (0.0006 * bmult) / TRADING_DAYS_PER_MONTH
    out_ret = pd.Series(
        np.where(bond_mom > 0, bond_ret * bmult - bond_cost_daily, 0.0),
        index=ixic.index,
    ).fillna(0.0)

    # 4) 回测引擎（严格用 t-1 信号决策 t）
    nav = np.full(len(ixic), np.nan)
    nav[0] = INIT_CASH
    value = INIT_CASH
    in_risk = False

    for i in range(1, len(ixic)):
        risk_on = bool(signal_risk_on.iloc[i - 1])
        lev = float(leverage.iloc[i - 1]) if not np.isnan(leverage.iloc[i - 1]) else minl
        lev = max(minl, min(maxl, lev))

        turnover = 1.0 if risk_on != in_risk else 0.0
        in_risk = risk_on

        r_ix = float(ixic_ret.iloc[i]) if not np.isnan(ixic_ret.iloc[i]) else 0.0
        r_out = float(out_ret.iloc[i]) if not np.isnan(out_ret.iloc[i]) else 0.0

        if risk_on:
            value *= (1 + r_ix * lev - cost_daily * lev - slip * turnover)
        else:
            value *= (1 + r_out - slip * turnover)

        value = max(value, 1.0)
        nav[i] = value

    nav = pd.Series(nav, index=ixic.index, name="NAV")

    years = (nav.index[-1] - nav.index[0]).days / 365.25
    cagr = (nav.iloc[-1] / nav.iloc[0]) ** (1 / years) - 1
    max_dd = ((nav / nav.cummax()) - 1).min()
    daily_ret = nav.pct_change().dropna()
    sharpe = np.sqrt(TRADING_DAYS_PER_YEAR) * daily_ret.mean() / (daily_ret.std() + 1e-9)
    total_return = nav.iloc[-1] / nav.iloc[0] - 1

    return {
        "params": params,
        "window_days": {
            "trend": tw_days,
            "vol": rvw_days,
            "bond_mom": blook_days,
        },
        "final_value": nav.iloc[-1],
        "total_return": total_return,
        "cagr": cagr,
        "max_dd": max_dd,
        "sharpe": sharpe,
        "nav": nav,
    }


def print_report(name: str, result: dict):
    print(f"\n=== {name} ===")
    print("params:", result["params"])
    print("window_days:", result.get("window_days", {}))
    print(f"Final Value : ${result['final_value']:,.0f}")
    print(f"Total Return: {result['total_return']*100:,.1f}%")
    print(f"CAGR       : {result['cagr']*100:.2f}%")
    print(f"Max DD     : {result['max_dd']*100:.2f}%")
    print(f"Sharpe     : {result['sharpe']:.2f}")
