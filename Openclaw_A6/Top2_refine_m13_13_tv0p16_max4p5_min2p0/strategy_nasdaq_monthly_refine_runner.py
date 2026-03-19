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


def realized_vol(mrets: list[float], i: int, window: int) -> float | None:
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


def run_strategy(
    strategy_id: str,
    mom_fast: int,
    mom_slow: int,
    vol_window: int,
    target_vol: float,
    max_lev: float,
    min_lev: float,
    bonus: float,
    crash_filter: float,
    crash_cooldown: int,
) -> dict[str, Any]:
    dates, closes = load_monthly()
    mrets = returns_from_closes(closes)

    portfolio = [INITIAL_CAPITAL]
    equity_rows: list[dict[str, Any]] = []
    decision_rows: list[dict[str, Any]] = []
    cooldown_left = 0

    equity_rows.append({
        'date': dates[0].isoformat(),
        'close': f'{closes[0]:.6f}',
        'portfolio': f'{INITIAL_CAPITAL:.6f}',
        'monthly_return': '',
        'signal_prev_month': '',
        'leverage_prev_month': '',
        'out_mode': '',
    })

    for i in range(1, len(closes)):
        j = i - 1
        fast = closes[j] / closes[j - mom_fast] - 1 if j >= mom_fast else None
        slow = closes[j] / closes[j - mom_slow] - 1 if j >= mom_slow else None
        sig = fast is not None and slow is not None and fast > 0 and slow > 0
        cooldown_before = cooldown_left
        crash_triggered = mrets[j] <= crash_filter
        if crash_triggered:
            sig = False
            cooldown_left = max(cooldown_left, crash_cooldown)
        elif cooldown_left > 0:
            sig = False
            cooldown_left -= 1

        rv = realized_vol(mrets, j, vol_window)
        base_lev = min_lev if rv is None else max(min(target_vol / rv, max_lev), min_lev)
        mom_score = max(((fast or 0.0) + (slow or 0.0)) / 2, 0.0)
        lev = max(min(base_lev * (1 + bonus * mom_score), max_lev), min_lev)

        ann = BOND_ANNUAL.get(dates[i].year, 0.05)
        out_mode = 'bond2x_pos' if ann > 0 else 'cash'
        oret = (((1 + ann) ** (1 / 12) - 1) * 2.0 - BOND_SIDE_MONTHLY_FEE) if ann > 0 else 0.0

        if sig:
            nav = portfolio[-1] * (1 + mrets[i] * lev - MONTHLY_COST_PER_LEV * lev)
            applied_out_mode = 'ixic'
        else:
            nav = portfolio[-1] * (1 + oret)
            applied_out_mode = out_mode
        nav = max(nav, 1.0)
        portfolio.append(nav)

        decision_rows.append({
            'decision_date': dates[j].isoformat(),
            'apply_month': dates[i].isoformat(),
            'close': f'{closes[j]:.6f}',
            'mom_fast': '' if fast is None else f'{fast:.6f}',
            'mom_slow': '' if slow is None else f'{slow:.6f}',
            'prev_month_return': f'{mrets[j]:.6f}',
            'realized_vol': '' if rv is None else f'{rv:.6f}',
            'base_leverage': f'{base_lev:.6f}',
            'target_leverage': f'{lev:.6f}',
            'crash_triggered': str(crash_triggered),
            'cooldown_before': cooldown_before,
            'cooldown_after': cooldown_left,
            'signal': str(sig),
            'allocation': applied_out_mode,
        })

        equity_rows.append({
            'date': dates[i].isoformat(),
            'close': f'{closes[i]:.6f}',
            'portfolio': f'{nav:.6f}',
            'monthly_return': f'{(nav / portfolio[-2] - 1):.6f}',
            'signal_prev_month': str(sig),
            'leverage_prev_month': f'{lev:.6f}',
            'out_mode': applied_out_mode,
        })

    years = (dates[-1] - dates[0]).days / 365.25
    final_value = portfolio[-1]
    total_return = final_value / INITIAL_CAPITAL - 1
    cagr = (final_value / INITIAL_CAPITAL) ** (1 / years) - 1
    rs = [portfolio[i] / portfolio[i - 1] - 1 for i in range(1, len(portfolio))]
    ann_vol = statistics.stdev(rs) * math.sqrt(12) if len(rs) >= 2 else 0.0
    sharpe = ((statistics.mean(rs) * 12) / ann_vol) if ann_vol > 0 else 0.0
    peak = portfolio[0]
    worst = 0.0
    for v in portfolio:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1)

    summary = {
        '策略': strategy_id,
        '最终价值': fmt_money(final_value),
        '总收益': fmt_pct(total_return),
        '年化CAGR': fmt_pct(cagr),
        '年化波动': fmt_pct(ann_vol),
        '最大回撤': fmt_pct(worst),
        '夏普': f'{sharpe:.2f}',
        '参数_mom_fast': mom_fast,
        '参数_mom_slow': mom_slow,
        '参数_vol_window': vol_window,
        '参数_target_vol': target_vol,
        '参数_max_lev': max_lev,
        '参数_min_lev': min_lev,
        '参数_bonus': bonus,
        '参数_crash_filter': crash_filter,
        '参数_crash_cooldown': crash_cooldown,
    }

    stem = strategy_id.replace('.', 'p').replace('-', 'neg')
    summary_path = OUTPUT_DIR / f'{stem}_summary.csv'
    equity_path = OUTPUT_DIR / f'{stem}_equity.csv'
    decisions_path = OUTPUT_DIR / f'{stem}_decisions.csv'
    report_path = OUTPUT_DIR / f'{stem}_report.md'

    with summary_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    with equity_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(equity_rows[0].keys()))
        writer.writeheader()
        writer.writerows(equity_rows)

    with decisions_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(decision_rows[0].keys()))
        writer.writeheader()
        writer.writerows(decision_rows)

    lines = [
        f'# {strategy_id}',
        '',
        f'- 回测区间: {dates[0]} ~ {dates[-1]}',
        f'- 初始资金: {fmt_money(INITIAL_CAPITAL)}',
        '- 数据: 本地 IXIC 日线聚合为月末收盘',
        '- 执行: 月末信号，次月收益生效',
        '- 出场侧: 正债券年使用 2x bond，否则 cash',
        '',
        '## 绩效',
        '| 策略 | 最终价值 | 总收益 | 年化CAGR | 年化波动 | 最大回撤 | 夏普 |',
        '|---|---:|---:|---:|---:|---:|---:|',
        f"| {summary['策略']} | {summary['最终价值']} | {summary['总收益']} | {summary['年化CAGR']} | {summary['年化波动']} | {summary['最大回撤']} | {summary['夏普']} |",
        '',
        '## 参数',
        f'- mom_fast: {mom_fast}',
        f'- mom_slow: {mom_slow}',
        f'- vol_window: {vol_window}',
        f'- target_vol: {target_vol}',
        f'- max_lev: {max_lev}',
        f'- min_lev: {min_lev}',
        f'- bonus: {bonus}',
        f'- crash_filter: {crash_filter}',
        f'- crash_cooldown: {crash_cooldown}',
        '',
        '## 输出文件',
        f'- {summary_path.name}',
        f'- {equity_path.name}',
        f'- {decisions_path.name}',
    ]
    report_path.write_text('\n'.join(lines), encoding='utf-8')

    return {
        'summary_path': str(summary_path),
        'equity_path': str(equity_path),
        'decisions_path': str(decisions_path),
        'report_path': str(report_path),
        'summary': summary,
    }
