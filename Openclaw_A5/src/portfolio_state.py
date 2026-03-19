import json
from pathlib import Path

from config import STATE_DIR

STATE_FILE = STATE_DIR / 'current_position.json'


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {
            'target_asset': 'CASH',
            'target_leverage': 0.0,
            'last_signal_date': None,
            'last_rebalance_date': None,
        }
    return json.loads(STATE_FILE.read_text(encoding='utf-8'))


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
