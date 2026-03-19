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


def run_strategy(strategy_id: str, lookback: int, base_target_vol: float, attack_target_vol: float, attack_max_lev: float, min_lev: float, crash_filter: float, attack_mom_threshold: float, attack_vol_cap: float, attack_hold_months: int = 0, carry_mode: str = 'full') -> dict[str, Any]:
    dates, closes = load_monthly()
    mrets = returns_from_closes(closes)
    vals = [INITIAL_CAPITAL]
    cooldown_left = 0
    attack_timer = 0
    decisions = []
    equities = [{'date': dates[0].isoformat(), 'close': f'{closes[0]:.6f}', 'portfolio': f'{INITIAL_CAPITAL:.6f}'}]

    for i in range(1, len(closes)):
        j = i - 1
        mom = closes[j] / closes[j - lookback] - 1 if j >= lookback else None
        sig = mom is not None and mom > 0
        if mrets[j] <= crash_filter:
            sig = False
            cooldown_left = max(cooldown_left, 1)
            attack_timer = 0
        elif cooldown_left > 0:
            sig = False
            cooldown_left -= 1

        rv = realized_vol(mrets, j, 2)
        attack_trigger = mom is not None and mom >= attack_mom_threshold and rv is not None and rv <= attack_vol_cap and mrets[j] > 0
        if attack_trigger:
            attack_timer = attack_hold_months

        target_vol = base_target_vol
        max_lev = 4.5
        attack_state = 'base'
        if attack_trigger:
            target_vol = attack_target_vol
            max_lev = attack_max_lev
            attack_state = 'trigger'
        elif attack_timer > 0:
            attack_state = f'carry_{carry_mode}'
            if carry_mode == 'full':
                target_vol = attack_target_vol
            else:
                target_vol = base_target_vol + (attack_target_vol - base_target_vol) / 2
            max_lev = attack_max_lev
            attack_timer -= 1

        lev = min_lev if rv is None else max(min(target_vol / rv, max_lev), min_lev)

        if sig:
            nav = vals[-1] * (1 + mrets[i] * lev - MONTHLY_COST_PER_LEV * lev)
            alloc = 'ixic'
        else:
            ann = BOND_ANNUAL.get(dates[i].year, 0.05)
            oret = (((1 + ann) ** (1 / 12) - 1) * 2.0 - BOND_SIDE_MONTHLY_FEE) if ann > 0 else 0.0
            nav = vals[-1] * (1 + oret)
            alloc = 'bond2x_pos' if ann > 0 else 'cash'
        nav = max(nav, 1.0)
        vals.append(nav)

        decisions.append({
            'decision_date': dates[j].isoformat(),
            'apply_month': dates[i].isoformat(),
            'close': f'{closes[j]:.6f}',
            'momentum': '' if mom is None else f'{mom:.6f}',
            'prev_month_return': f'{mrets[j]:.6f}',
            'realized_vol': '' if rv is None else f'{rv:.6f}',
            'target_vol': f'{target_vol:.6f}',
            'target_leverage': f'{lev:.6f}',
            'attack_state': attack_state,
            'signal': str(sig),
            'allocation': alloc,
        })
        equities.append({'date': dates[i].isoformat(), 'close': f'{closes[i]:.6f}', 'portfolio': f'{nav:.6f}'})

    years = (dates[-1] - dates[0]).days / 365.25
    final_value = vals[-1]
    total_return = final_value / INITIAL_CAPITAL - 1
    cagr = (final_value / INITIAL_CAPITAL) ** (1 / years) - 1
    rs = [vals[i] / vals[i - 1] - 1 for i in range(1, len(vals))]
    ann_vol = statistics.stdev(rs) * math.sqrt(12) if len(rs) >= 2 else 0.0
    sharpe = ((statistics.mean(rs) * 12) / ann_vol) if ann_vol > 0 else 0.0
    peak = vals[0]
    worst = 0.0
    for v in vals:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1)

    stem = strategy_id.replace('.', 'p').replace('-', 'neg')
    summary = {
        '策略': strategy_id,
        '最终价值': fmt_money(final_value),
        '总收益': fmt_pct(total_return),
        '年化CAGR': fmt_pct(cagr),
        '年化波动': fmt_pct(ann_vol),
        '最大回撤': fmt_pct(worst),
        '夏普': f'{sharpe:.2f}',
    }
    summary_path = OUTPUT_DIR / f'{stem}_summary.csv'
    equity_path = OUTPUT_DIR / f'{stem}_equity.csv'
    decisions_path = OUTPUT_DIR / f'{stem}_decisions.csv'

    with summary_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)
    with equity_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(equities[0].keys()))
        writer.writeheader()
        writer.writerows(equities)
    with decisions_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(decisions[0].keys()))
        writer.writeheader()
        writer.writerows(decisions)

    return {'summary': summary, 'summary_path': str(summary_path), 'equity_path': str(equity_path), 'decisions_path': str(decisions_path)}
