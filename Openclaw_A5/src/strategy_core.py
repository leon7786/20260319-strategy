from config import PARAMS, RISK_RULES, PRIMARY_RISK_ASSET
from data_feed import download_monthly_close, align_series
from signal_engine import build_signals
from allocation_engine import build_allocation
from risk_engine import validate_decision


def generate_latest_decision() -> dict:
    risk_asset = PRIMARY_RISK_ASSET
    risk_off_asset = PARAMS['risk_off_asset']

    risk_prices = download_monthly_close(risk_asset)
    risk_off_prices = download_monthly_close(risk_off_asset)
    aligned = align_series({'risk': risk_prices, 'risk_off': risk_off_prices})

    signals = build_signals(aligned['risk'], aligned['risk_off'], PARAMS)
    alloc = build_allocation(aligned['risk'], signals, PARAMS)

    latest_dt = alloc.index[-1]
    latest = {
        'date': str(latest_dt.date()),
        'risk_asset': risk_asset,
        'risk_off_asset': risk_off_asset,
        'target_asset': str(alloc.loc[latest_dt, 'target_asset']),
        'target_leverage': float(alloc.loc[latest_dt, 'target_leverage']),
        'rv': float(alloc.loc[latest_dt, 'rv']),
        'target_vol': float(alloc.loc[latest_dt, 'target_vol']),
        'risk_on': bool(signals.loc[latest_dt, 'risk_on']),
        'risk_off_ok': bool(signals.loc[latest_dt, 'risk_off_ok']),
        'mode': 'DRY_RUN',
        'params': PARAMS,
    }
    return validate_decision(latest, RISK_RULES)
