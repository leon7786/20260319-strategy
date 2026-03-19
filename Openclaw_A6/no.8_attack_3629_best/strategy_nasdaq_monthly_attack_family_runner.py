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


def run_attack_family_strategy(strategy_id: str, lookback: int, base_target_vol: float, attack_target_vol: float, attack_max_lev: float, min_lev: float, crash_filter: float, cooldown_months: int, attack_mom_threshold: float, attack_vol_cap: float, require_prev_positive: bool = True, attack_hold_months: int = 0, carry_mode: str = 'full', vol_window: int = 2):
    dates, closes = load_monthly()
    mrets = returns_from_closes(closes)
    vals = [INITIAL_CAPITAL]
    cooldown_left = 0
    attack_timer = 0
    decisions = []

    for i in range(1, len(closes)):
        j = i - 1
        mom = closes[j] / closes[j - lookback] - 1 if j >= lookback else None
        sig = mom is not None and mom > 0
        if mrets[j] <= crash_filter:
            sig = False
            cooldown_left = max(cooldown_left, cooldown_months)
            attack_timer = 0
        elif cooldown_left > 0:
            sig = False
            cooldown_left -= 1
            attack_timer = 0

        rv = realized_vol(mrets, j, vol_window)
        attack_trigger = mom is not None and mom >= attack_mom_threshold and rv is not None and rv <= attack_vol_cap
        if require_prev_positive:
            attack_trigger = attack_trigger and mrets[j] > 0
        if attack_trigger:
            attack_timer = attack_hold_months

        target_vol = base_target_vol
        max_lev = 4.5
        state = 'base'
        if attack_trigger:
            target_vol = attack_target_vol
            max_lev = attack_max_lev
            state = 'trigger'
        elif attack_timer > 0:
            max_lev = attack_max_lev
            state = f'carry_{carry_mode}'
            if carry_mode == 'full':
                target_vol = attack_target_vol
            else:
                target_vol = base_target_vol + (attack_target_vol - base_target_vol) / 2
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
            'momentum': '' if mom is None else f'{mom:.6f}',
            'prev_month_return': f'{mrets[j]:.6f}',
            'realized_vol': '' if rv is None else f'{rv:.6f}',
            'attack_state': state,
            'target_vol': f'{target_vol:.6f}',
            'target_leverage': f'{lev:.6f}',
            'signal': str(sig),
            'allocation': alloc,
        })
    return write_outputs(strategy_id, vals, dates, closes, decisions)
