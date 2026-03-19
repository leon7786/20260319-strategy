from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
STATE_DIR = PROJECT_DIR / 'state'
LOG_DIR = PROJECT_DIR / 'logs'
STATE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

START = '1995-01-03'
END_EXCLUSIVE = '2025-12-30'
INIT_CAPITAL = 10000.0

PRIMARY_RISK_ASSET = '^IXIC'
DEFAULT_RISK_OFF_ASSET = 'VUSTX'
ALTERNATE_RISK_OFF_ASSET = 'VFITX'

# 当前默认先采用更稳健的 walk-forward 平衡版思路
PARAMS = {
    'la': 3.23,
    'trend_ma': 9,
    'rv_window': 2,
    'base_target_vol': 0.182,
    'winter_mult': 1.251,
    'summer_mult': 1.289,
    'min_lev': 0.09,
    'max_lev': 3.0,
    'risk_off_asset': 'VUSTX',
    'risk_off_lev': 2.35,
    'risk_off_mom_window': 6,
    'use_trend_filter': True,
}

RISK_RULES = {
    'max_allowed_leverage': 3.0,
    'max_rebalance_per_day': 1,
    'vol_hard_stop': 0.18,
    'allow_trade_when_data_missing': False,
}
