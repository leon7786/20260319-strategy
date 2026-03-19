import pandas as pd
import numpy as np
from pathlib import Path

INIT_CASH = 10_000.0
START = pd.Timestamp("1995-01-03")
END = pd.Timestamp("2025-12-29")


def load_monthly_data():
    """加载 IXIC + VUSTX 日线，并对齐后转月线。"""
    import os

    # common.py 位于 repo/Openclaw_A2/common.py，repo 根目录是 parents[1]
    repo_root = Path(__file__).resolve().parents[1]

    # 数据目录优先级：
    # 1) 环境变量 STRATEGY_DATA_DIR
    # 2) 当前仓库 data/
    # 3) 已有回测项目 /root/projects/20260318IXIC/data/
    candidate_dirs = []
    env_dir = os.getenv("STRATEGY_DATA_DIR")
    if env_dir:
        candidate_dirs.append(Path(env_dir))
    candidate_dirs.append(repo_root / "data")
    candidate_dirs.append(Path("/root/projects/20260318IXIC/data"))

    ixic_path = None
    bond_path = None
    for d in candidate_dirs:
        ix = d / "IXIC_daily_yf.csv"
        bd = d / "VUSTX_daily_yf.csv"
        if ix.exists() and bd.exists():
            ixic_path = ix
            bond_path = bd
            break

    if ixic_path is None or bond_path is None:
        raise FileNotFoundError(
            "找不到 IXIC_daily_yf.csv / VUSTX_daily_yf.csv。"
            "可设置 STRATEGY_DATA_DIR 或把数据放到 repo/data/"
        )

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
    monthly = df.resample("ME").last().dropna()
    return monthly["IXIC"], monthly["BOND"]


def run_backtest(params: dict):
    """
    params 字段：
      tw, rvw, tvs, tvw, minl, maxl, bmult, blook, cost, slip
    """
    ixic, bond = load_monthly_data()
    ixic_ret = ixic.pct_change()
    bond_ret = bond.pct_change()

    tw = params["tw"]
    rvw = params["rvw"]
    tvs = params["tvs"]
    tvw = params["tvw"]
    minl = params["minl"]
    maxl = params["maxl"]
    bmult = params["bmult"]
    blook = params["blook"]
    cost = params["cost"]
    slip = params["slip"]

    # 1) 趋势开关
    signal_risk_on = ixic > ixic.rolling(tw).mean()

    # 2) 动态杠杆（0.1x ~ 3.0x）
    realized_vol = ixic_ret.rolling(rvw).std().clip(lower=0.01)
    target_vol = pd.Series(tvw, index=ixic.index)
    target_vol[ixic.index.month.isin([11, 12, 1, 2, 3, 4])] = tvs
    leverage = (target_vol / realized_vol).clip(lower=minl, upper=maxl)

    # 3) 空仓期债券过滤（绝对动量）
    bond_mom = ((1 + bond_ret).rolling(blook).apply(np.prod, raw=True) - 1).shift(1)
    out_ret = pd.Series(
        np.where(bond_mom > 0, bond_ret * bmult - 0.0006 * bmult, 0.0),
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
            value *= (1 + r_ix * lev - cost * lev - slip * turnover)
        else:
            value *= (1 + r_out - slip * turnover)

        value = max(value, 1.0)
        nav[i] = value

    nav = pd.Series(nav, index=ixic.index, name="NAV")

    years = (nav.index[-1] - nav.index[0]).days / 365.25
    cagr = (nav.iloc[-1] / nav.iloc[0]) ** (1 / years) - 1
    max_dd = ((nav / nav.cummax()) - 1).min()
    monthly_ret = nav.pct_change().dropna()
    sharpe = np.sqrt(12) * monthly_ret.mean() / (monthly_ret.std() + 1e-9)
    total_return = nav.iloc[-1] / nav.iloc[0] - 1

    return {
        "params": params,
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
    print(f"Final Value : ${result['final_value']:,.0f}")
    print(f"Total Return: {result['total_return']*100:,.1f}%")
    print(f"CAGR       : {result['cagr']*100:.2f}%")
    print(f"Max DD     : {result['max_dd']*100:.2f}%")
    print(f"Sharpe     : {result['sharpe']:.2f}")
