#!/usr/bin/env python3
"""Top 5 动态杠杆策略公共模块。"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
import json
import re

import numpy as np
import pandas as pd
import yfinance as yf

START_DATE = "1995-01-03"
END_DATE_EXCLUSIVE = "2025-12-30"  # 为了包含 2025-12-29
INITIAL_CAPITAL = 10_000.0
NASDAQ_COST_PER_LEV = 0.0015
BOND_COST_PER_LEV = 0.0005

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent.parent / "output" / "top5_dynamic_strategies"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class StrategyConfig:
    """单个策略配置。"""

    name: str
    la: float
    thr: float
    lev_low: float
    lev_high: float
    w_trend: float
    w_short: float
    w_vol: float
    w_dd: float
    mom_cap: float
    short_w: int
    short_cap: float
    vol_w: int
    vol_lo: float
    vol_hi: float
    dd_w: int
    dd_floor: float
    bond_alpha: float
    bond_mult: float


@lru_cache(maxsize=None)
def monthly_last_close(symbol: str) -> pd.Series:
    """下载日线并聚合成每个月最后一个交易日收盘价。"""
    df = yf.download(
        symbol,
        start=START_DATE,
        end=END_DATE_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    close = df["Close"].dropna()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    month_end_index: list[pd.Timestamp] = []
    month_end_values: list[float] = []
    for _, group in close.groupby(close.index.to_period("M")):
        month_end_index.append(group.index[-1])
        month_end_values.append(float(group.iloc[-1]))

    return pd.Series(month_end_values, index=pd.DatetimeIndex(month_end_index), name=symbol)


@lru_cache(maxsize=1)
def load_aligned_universe() -> tuple[pd.Series, pd.Series, pd.Series]:
    """载入并对齐 NASDAQ / 长债 / 中债 月末序列。"""
    ixic = monthly_last_close("^IXIC")
    vustx = monthly_last_close("VUSTX").reindex(ixic.index, method="ffill")
    vfitx = monthly_last_close("VFITX").reindex(ixic.index, method="ffill")
    return ixic, vustx, vfitx


@lru_cache(maxsize=None)
def fractional_reference(la: float) -> pd.Series:
    """按 LA（月）计算带小数的参考价格。"""
    ixic, _, _ = load_aligned_universe()
    prices = ixic.astype(float)

    low = max(int(np.floor(la)), 1)
    high = max(int(np.ceil(la)), 1)
    frac = la - np.floor(la)

    ref = pd.Series(np.nan, index=prices.index, dtype=float)
    if low == high:
        ref.iloc[low:] = prices.iloc[:-low].to_numpy()
    else:
        ref.iloc[high:] = (
            prices.iloc[high - low : len(prices) - low].to_numpy() * (1 - frac)
            + prices.iloc[: len(prices) - high].to_numpy() * frac
        )

    return ref


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_").lower()


def build_strategy_frame(config: StrategyConfig) -> pd.DataFrame:
    """生成策略所需的所有月度因子与决策列。"""
    ixic, vustx, vfitx = load_aligned_universe()
    df = pd.DataFrame(
        {
            "ixic": ixic,
            "vustx": vustx,
            "vfitx": vfitx,
        }
    )

    df["ixic_ret"] = df["ixic"].pct_change().fillna(0.0)
    df["vustx_ret"] = df["vustx"].pct_change().fillna(0.0)
    df["vfitx_ret"] = df["vfitx"].pct_change().fillna(0.0)

    df["ref_price"] = fractional_reference(config.la)
    df["signal_in"] = df["ixic"] > df["ref_price"]
    df["trend_raw"] = df["ixic"] / df["ref_price"] - 1.0
    df["trend_score"] = (df["trend_raw"] / config.mom_cap).clip(lower=0.0, upper=1.0)

    df["short_raw"] = df["ixic"] / df["ixic"].shift(config.short_w) - 1.0
    df["short_score"] = (df["short_raw"] / config.short_cap).clip(lower=0.0, upper=1.0)

    df["vol_raw"] = df["ixic_ret"].rolling(config.vol_w).std()
    df["vol_score"] = (
        1.0 - (df["vol_raw"] - config.vol_lo) / max(config.vol_hi - config.vol_lo, 1e-9)
    ).clip(lower=0.0, upper=1.0)

    df["drawdown_raw"] = df["ixic"] / df["ixic"].rolling(config.dd_w).max() - 1.0
    df["drawdown_score"] = (
        (df["drawdown_raw"] - config.dd_floor) / (0.0 - config.dd_floor)
    ).clip(lower=0.0, upper=1.0)

    df["score"] = (
        config.w_trend * df["trend_score"]
        + config.w_short * df["short_score"]
        + config.w_vol * df["vol_score"]
        + config.w_dd * df["drawdown_score"]
    ).clip(lower=0.0, upper=1.0)

    df["leverage"] = np.where(df["score"] >= config.thr, config.lev_high, config.lev_low)
    df["leverage"] = df["leverage"].round(2).clip(lower=0.10, upper=3.00)

    # bond_alpha = VUSTX 权重；1 - bond_alpha = VFITX 权重
    df["bond_ret_base"] = config.bond_alpha * df["vustx_ret"] + (1.0 - config.bond_alpha) * df["vfitx_ret"]
    df["bond_ret_used"] = df["bond_ret_base"] * config.bond_mult - BOND_COST_PER_LEV * config.bond_mult

    return df


def backtest_strategy(config: StrategyConfig) -> tuple[pd.DataFrame, dict]:
    """按给定配置执行月频回测。"""
    df = build_strategy_frame(config)
    nav_list: list[float] = [INITIAL_CAPITAL]
    action_list: list[str] = ["INIT"]
    monthly_portfolio_ret: list[float] = [0.0]

    value = INITIAL_CAPITAL
    prev_in = False

    for i in range(1, len(df)):
        prev_signal_in = bool(df["signal_in"].iloc[i - 1]) if pd.notna(df["signal_in"].iloc[i - 1]) else False
        prev_lev = float(df["leverage"].iloc[i - 1]) if pd.notna(df["leverage"].iloc[i - 1]) else config.lev_low

        if prev_signal_in:
            period_ret = float(df["ixic_ret"].iloc[i]) * prev_lev - NASDAQ_COST_PER_LEV * prev_lev
        else:
            period_ret = float(df["bond_ret_used"].iloc[i])

        value = max(value * (1.0 + period_ret), 1.0)
        nav_list.append(value)
        monthly_portfolio_ret.append(period_ret)

        current_in = prev_signal_in
        if current_in and not prev_in:
            action_list.append("ENTER_NASDAQ")
        elif (not current_in) and prev_in:
            action_list.append("EXIT_TO_BOND")
        else:
            action_list.append("HOLD")
        prev_in = current_in

    df["portfolio_ret"] = monthly_portfolio_ret
    df["nav"] = nav_list
    df["action"] = action_list

    years = (df.index[-1] - df.index[0]).days / 365.25
    final_value = float(df["nav"].iloc[-1])
    total_return = final_value / INITIAL_CAPITAL - 1.0
    cagr = (final_value / INITIAL_CAPITAL) ** (1.0 / years) - 1.0 if years > 0 else np.nan

    drawdown = df["nav"] / df["nav"].cummax() - 1.0
    max_drawdown = float(drawdown.min())

    monthly_ret = df["portfolio_ret"].iloc[1:]
    sharpe = (monthly_ret.mean() * 12.0) / (monthly_ret.std() * np.sqrt(12.0)) if monthly_ret.std() > 0 else np.nan

    buy_hold_nav = INITIAL_CAPITAL * (1.0 + df["ixic_ret"]).cumprod()
    buy_hold_final = float(buy_hold_nav.iloc[-1])
    buy_hold_total = buy_hold_final / INITIAL_CAPITAL - 1.0
    buy_hold_cagr = (buy_hold_final / INITIAL_CAPITAL) ** (1.0 / years) - 1.0 if years > 0 else np.nan

    summary = {
        "strategy_name": config.name,
        "date_range": f"{df.index[0].date()} ~ {df.index[-1].date()}",
        "initial_capital": INITIAL_CAPITAL,
        "final_value": final_value,
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "buy_hold_final": buy_hold_final,
        "buy_hold_total": buy_hold_total,
        "buy_hold_cagr": buy_hold_cagr,
        "config": asdict(config),
    }

    return df, summary


def save_outputs(config: StrategyConfig, df: pd.DataFrame, summary: dict) -> Path:
    """保存 summary / nav / decisions 三类输出。"""
    slug = slugify(config.name)
    strategy_dir = OUTPUT_DIR / slug
    strategy_dir.mkdir(parents=True, exist_ok=True)

    summary_path = strategy_dir / "summary.json"
    nav_path = strategy_dir / "nav.csv"
    decisions_path = strategy_dir / "decisions.csv"

    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    df[["ixic", "vustx", "vfitx", "signal_in", "score", "leverage", "bond_ret_used", "portfolio_ret", "nav"]].to_csv(
        nav_path,
        encoding="utf-8-sig",
    )
    df[["ixic", "signal_in", "score", "leverage", "action"]].to_csv(
        decisions_path,
        encoding="utf-8-sig",
    )

    return strategy_dir


def print_summary(summary: dict) -> None:
    """终端打印摘要。"""
    print("=" * 72)
    print(summary["strategy_name"])
    print("=" * 72)
    print(f"区间: {summary['date_range']}")
    print(f"初始资金: ${summary['initial_capital']:,.0f}")
    print(f"最终价值: ${summary['final_value']:,.0f}")
    print(f"总收益: {summary['total_return'] * 100:.1f}%")
    print(f"年化 CAGR: {summary['cagr'] * 100:.2f}%")
    print(f"最大回撤: {summary['max_drawdown'] * 100:.1f}%")
    print(f"夏普: {summary['sharpe']:.2f}")
    print(f"买入持有总收益: {summary['buy_hold_total'] * 100:.1f}%")
    print(f"买入持有 CAGR: {summary['buy_hold_cagr'] * 100:.2f}%")


__all__ = [
    "StrategyConfig",
    "backtest_strategy",
    "print_summary",
    "save_outputs",
]
