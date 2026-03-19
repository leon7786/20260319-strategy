import pandas as pd

from features import realized_vol, seasonal_target_vol


def build_allocation(risk_prices: pd.Series, signals: pd.DataFrame, params: dict) -> pd.DataFrame:
    risk_ret = risk_prices.pct_change().fillna(0.0)
    rv = realized_vol(risk_ret, params['rv_window'])
    target_vol = seasonal_target_vol(risk_prices.index, params['base_target_vol'], params['winter_mult'], params['summer_mult'])
    lev = (target_vol / rv).clip(lower=params['min_lev'], upper=params['max_lev'])

    target_asset = []
    target_leverage = []
    for dt in risk_prices.index:
        if bool(signals.loc[dt, 'risk_on']):
            target_asset.append('RISK')
            target_leverage.append(float(lev.loc[dt]))
        elif bool(signals.loc[dt, 'risk_off_ok']):
            target_asset.append('RISK_OFF')
            target_leverage.append(float(params['risk_off_lev']))
        else:
            target_asset.append('CASH')
            target_leverage.append(0.0)

    return pd.DataFrame({
        'target_asset': target_asset,
        'target_leverage': target_leverage,
        'rv': rv,
        'target_vol': target_vol,
    }, index=risk_prices.index)
