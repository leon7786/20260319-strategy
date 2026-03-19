#!/usr/bin/env python3
from __future__ import annotations

from strategy_nasdaq_monthly_shared import (
    BOND_ANNUAL,
    BOND_SIDE_MONTHLY_FEE,
    INITIAL_CAPITAL,
    MONTHLY_COST_PER_LEV,
    load_monthly,
    realized_vol,
    returns_from_closes,
    write_outputs,
)


def run_breakout_strategy(strategy_id: str, lookback: int, vol_window: int, normal_target_vol: float, attack_target_vol: float, defense_target_vol: float, max_lev: float, min_lev: float, crash_filter: float, cooldown_months: int, dd_guard: float, attack_mom_threshold: float, attack_vol_cap: float):
    dates, closes = load_monthly()
    mrets = returns_from_closes(closes)
    vals = [INITIAL_CAPITAL]
    peak = INITIAL_CAPITAL
    cooldown_left = 0
    decisions = []

    for i in range(1, len(closes)):
        j = i - 1
        mom = closes[j] / closes[j - lookback] - 1 if j >= lookback else None
        sig = mom is not None and mom > 0
        if mrets[j] <= crash_filter:
            sig = False
            cooldown_left = max(cooldown_left, cooldown_months)
        elif cooldown_left > 0:
            sig = False
            cooldown_left -= 1

        rv = realized_vol(mrets, j, vol_window)
        current_dd = vals[-1] / peak - 1
        if current_dd <= dd_guard:
            regime = 'defense'
            target_vol = defense_target_vol
        elif mom is not None and mom >= attack_mom_threshold and rv is not None and rv <= attack_vol_cap:
            regime = 'attack'
            target_vol = attack_target_vol
        else:
            regime = 'normal'
            target_vol = normal_target_vol
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
        peak = max(peak, nav)
        decisions.append({
            'decision_date': dates[j].isoformat(),
            'apply_month': dates[i].isoformat(),
            'momentum': '' if mom is None else f'{mom:.6f}',
            'realized_vol': '' if rv is None else f'{rv:.6f}',
            'current_drawdown': f'{current_dd:.6f}',
            'regime': regime,
            'target_vol': f'{target_vol:.6f}',
            'target_leverage': f'{lev:.6f}',
            'signal': str(sig),
            'allocation': alloc,
        })
    return write_outputs(strategy_id, vals, dates, closes, decisions)
