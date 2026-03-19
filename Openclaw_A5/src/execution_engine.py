def build_orders(current_state: dict, approved_decision: dict) -> list[dict]:
    orders = []
    current_asset = current_state.get('target_asset', 'CASH')
    current_lev = float(current_state.get('target_leverage', 0.0))
    target_asset = approved_decision['target_asset']
    target_lev = float(approved_decision['target_leverage'])

    if not approved_decision['approved']:
        return [{
            'action': 'NO_TRADE',
            'reason': approved_decision['risk_reasons'],
        }]

    if current_asset == target_asset and abs(current_lev - target_lev) < 1e-9:
        return [{
            'action': 'HOLD',
            'reason': 'no rebalance required',
        }]

    if current_asset != 'CASH':
        orders.append({'action': 'EXIT', 'asset': current_asset, 'leverage': current_lev})

    if target_asset != 'CASH':
        orders.append({'action': 'ENTER', 'asset': target_asset, 'leverage': target_lev})
    else:
        orders.append({'action': 'MOVE_TO_CASH'})

    return orders
