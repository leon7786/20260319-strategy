import csv
import json
from pathlib import Path

from config import LOG_DIR
from execution_engine import build_orders
from portfolio_state import load_state, save_state
from strategy_core import generate_latest_decision


def append_signal_log(decision: dict, orders: list[dict]) -> None:
    path = LOG_DIR / 'signal_history.csv'
    exists = path.exists()
    with path.open('a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'target_asset', 'target_leverage', 'approved', 'risk_on', 'risk_off_ok', 'orders'])
        if not exists:
            writer.writeheader()
        writer.writerow({
            'date': decision['date'],
            'target_asset': decision['target_asset'],
            'target_leverage': decision['target_leverage'],
            'approved': decision['approved'],
            'risk_on': decision['risk_on'],
            'risk_off_ok': decision['risk_off_ok'],
            'orders': json.dumps(orders, ensure_ascii=False),
        })


def main():
    current_state = load_state()
    decision = generate_latest_decision()
    orders = build_orders(current_state, decision)
    append_signal_log(decision, orders)

    next_state = {
        'target_asset': decision['target_asset'],
        'target_leverage': decision['target_leverage'],
        'last_signal_date': decision['date'],
        'last_rebalance_date': decision['date'] if orders and orders[0]['action'] not in ('HOLD', 'NO_TRADE') else current_state.get('last_rebalance_date'),
    }
    save_state(next_state)

    output = {
        'decision': decision,
        'orders': orders,
        'previous_state': current_state,
        'next_state': next_state,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
