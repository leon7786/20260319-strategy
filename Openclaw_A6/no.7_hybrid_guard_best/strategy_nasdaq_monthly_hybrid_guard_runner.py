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

BASE_LOOKBACK = 13
BASE_VOL_WINDOW = 2
BASE_TARGET_VOL = 0.15
BASE_MAX_LEV = 4.5
BASE_MIN_LEV = 2.0
BASE_CRASH_FILTER = -0.09
BASE_COOLDOWN = 1


def run_hybrid_guard_strategy(strategy_id: str, dd_guard: float, recovery_threshold: float, defense_target_vol: float, defense_max_lev: float, defense_min_lev: float, attack_extra_target_vol: float, attack_mom_threshold: float, attack_vol_cap: float):
    dates, closes = load_monthly()
    mrets = returns_from_closes(closes)
    vals = [INITIAL_CAPITAL]
    peak = INITIAL_CAPITAL
    cooldown_left = 0
    in_defense = False
    decisions = []

    for i in range(1, len(closes)):
        j = i - 1
        mom = closes[j] / closes[j - BASE_LOOKBACK] - 1 if j >= BASE_LOOKBACK else None
        sig = mom is not None and mom > 0
        if mrets[j] <= BASE_CRASH_FILTER:
            sig = False
            cooldown_left = max(cooldown_left, BASE_COOLDOWN)
        elif cooldown_left > 0:
            sig = False
            cooldown_left -= 1

        rv = realized_vol(mrets, j, BASE_VOL_WINDOW)
        current_dd = vals[-1] / peak - 1
        if current_dd <= dd_guard:
            in_defense = True
        elif current_dd >= recovery_threshold:
            in_defense = False

        if in_defense:
            target_vol = defense_target_vol
            max_lev = defense_max_lev
            min_lev = defense_min_lev
            regime = 'defense'
        else:
            target_vol = BASE_TARGET_VOL
            if mom is not None and mom >= attack_mom_threshold and rv is not None and rv <= attack_vol_cap:
                target_vol += attack_extra_target_vol
                regime = 'attack'
            else:
                regime = 'base'
            max_lev = BASE_MAX_LEV
            min_lev = BASE_MIN_LEV
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
