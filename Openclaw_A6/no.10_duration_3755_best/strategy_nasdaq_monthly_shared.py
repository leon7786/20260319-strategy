#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import statistics
from datetime import date, datetime
from pathlib import Path
from typing import Any

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / 'processed' / 'ixic_daily.csv'
OUTPUT_DIR = PROJECT_DIR / 'output'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = date(1995, 1, 3)
END_DATE = date(2025, 12, 29)
INITIAL_CAPITAL = 10_000.0
MONTHLY_COST_PER_LEV = 0.0015
BOND_SIDE_MONTHLY_FEE = 0.001

BOND_ANNUAL = {
    1995: 0.31, 1996: -0.01, 1997: 0.15, 1998: 0.14,
    1999: -0.09, 2000: 0.22, 2001: 0.04, 2002: 0.17,
    2003: 0.02, 2004: 0.09, 2005: 0.07, 2006: 0.01,
    2007: 0.10, 2008: 0.26, 2009: -0.14, 2010: 0.10,
    2011: 0.34, 2012: 0.03, 2013: -0.14, 2014: 0.25,
    2015: -0.02, 2016: 0.01, 2017: 0.09, 2018: -0.02,
    2019: 0.15, 2020: 0.18, 2021: -0.05, 2022: -0.31,
    2023: -0.03, 2024: -0.05, 2025: 0.03,
}


def load_monthly() -> tuple[list[date], list[float]]:
    rows = []
    with DATA_PATH.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = datetime.strptime(row['date'], '%Y-%m-%d').date()
            if START_DATE <= dt <= END_DATE:
                rows.append((dt, float(row['close'])))
    rows.sort()
    monthly = []
    cur = None
    last = None
    for dt, close in rows:
        key = (dt.year, dt.month)
        if key != cur:
            if last is not None:
                monthly.append(last)
            cur = key
        last = (dt, close)
    if last is not None:
        monthly.append(last)
    return [d for d, _ in monthly], [c for _, c in monthly]


def returns_from_closes(closes: list[float]) -> list[float]:
    return [0.0] + [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes))]


def realized_vol(mrets: list[float], i: int, window: int = 2) -> float | None:
    if i < window:
        return None
    sample = mrets[i - window + 1:i + 1]
    if len(sample) < 2:
        return None
    return max(statistics.stdev(sample), 0.025)


def fmt_money(x: float) -> str:
    return f'${x:,.2f}'


def fmt_pct(x: float) -> str:
    return f'{x * 100:.2f}%'


def calc_metrics(portfolio: list[float], dates: list[date]) -> dict[str, float]:
    final = portfolio[-1]
    total = final / portfolio[0] - 1
    years = (dates[-1] - dates[0]).days / 365.25
    cagr = (final / portfolio[0]) ** (1 / years) - 1
    rs = [portfolio[i] / portfolio[i - 1] - 1 for i in range(1, len(portfolio))]
    ann_vol = statistics.stdev(rs) * math.sqrt(12) if len(rs) >= 2 else 0.0
    sharpe = ((statistics.mean(rs) * 12) / ann_vol) if ann_vol > 0 else 0.0
    peak = portfolio[0]
    worst = 0.0
    for v in portfolio:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1)
    return {
        'final_value': final,
        'total_return': total,
        'cagr': cagr,
        'ann_vol': ann_vol,
        'max_drawdown': worst,
        'sharpe': sharpe,
    }


def sanitize(name: str) -> str:
    return name.replace('.', 'p').replace('-', 'neg')


def write_outputs(strategy_id: str, portfolio: list[float], dates: list[date], closes: list[float], decisions: list[dict[str, Any]]) -> dict[str, Any]:
    mm = calc_metrics(portfolio, dates)
    stem = sanitize(strategy_id)
    summary = {
        '策略': strategy_id,
        '最终价值': fmt_money(mm['final_value']),
        '总收益': fmt_pct(mm['total_return']),
        '年化CAGR': fmt_pct(mm['cagr']),
        '年化波动': fmt_pct(mm['ann_vol']),
        '最大回撤': fmt_pct(mm['max_drawdown']),
        '夏普': f"{mm['sharpe']:.2f}",
    }
    summary_path = OUTPUT_DIR / f'{stem}_summary.csv'
    equity_path = OUTPUT_DIR / f'{stem}_equity.csv'
    decisions_path = OUTPUT_DIR / f'{stem}_decisions.csv'
    report_path = OUTPUT_DIR / f'{stem}_report.md'

    with summary_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    equities = [{'date': dates[i].isoformat(), 'close': f'{closes[i]:.6f}', 'portfolio': f'{portfolio[i]:.6f}'} for i in range(len(portfolio))]
    with equity_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(equities[0].keys()))
        writer.writeheader()
        writer.writerows(equities)

    with decisions_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(decisions[0].keys()) if decisions else ['decision_date'])
        writer.writeheader()
        if decisions:
            writer.writerows(decisions)

    report_path.write_text(
        '\n'.join([
            f'# {strategy_id}',
            '',
            f'- 回测区间: {dates[0]} ~ {dates[-1]}',
            f'- 初始资金: {fmt_money(INITIAL_CAPITAL)}',
            '- 数据: 本地 IXIC 日线聚合为月末收盘',
            '- 执行: 月末信号，次月收益生效',
            '',
            '| 策略 | 最终价值 | 总收益 | 年化CAGR | 年化波动 | 最大回撤 | 夏普 |',
            '|---|---:|---:|---:|---:|---:|---:|',
            f"| {summary['策略']} | {summary['最终价值']} | {summary['总收益']} | {summary['年化CAGR']} | {summary['年化波动']} | {summary['最大回撤']} | {summary['夏普']} |",
        ]),
        encoding='utf-8',
    )
    return {'summary': summary, 'summary_path': str(summary_path), 'equity_path': str(equity_path), 'decisions_path': str(decisions_path), 'report_path': str(report_path)}
