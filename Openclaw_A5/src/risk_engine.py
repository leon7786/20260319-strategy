def validate_decision(decision: dict, rules: dict) -> dict:
    approved = True
    reasons = []

    lev = float(decision.get('target_leverage', 0.0))
    if lev > float(rules['max_allowed_leverage']):
        approved = False
        reasons.append('target leverage exceeds max_allowed_leverage')

    rv = float(decision.get('rv', 0.0))
    if rv > float(rules['vol_hard_stop']) and decision.get('target_asset') == 'RISK':
        approved = False
        reasons.append('realized volatility above vol_hard_stop for risk asset')

    if not reasons:
        reasons.append('risk checks passed')

    return {
        **decision,
        'approved': approved,
        'risk_reasons': reasons,
    }
