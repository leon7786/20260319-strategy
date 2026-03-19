import pandas as pd

from features import fractional_momentum_signal, rolling_ma_filter, momentum_positive


def build_signals(risk_prices: pd.Series, risk_off_prices: pd.Series, params: dict) -> pd.DataFrame:
    mom = fractional_momentum_signal(risk_prices, params['la'])
    trend = rolling_ma_filter(risk_prices, params['trend_ma']) if params['use_trend_filter'] else pd.Series(True, index=risk_prices.index)
    risk_on = (mom & trend).fillna(False)
    risk_off_ok = momentum_positive(risk_off_prices, params['risk_off_mom_window'])
    df = pd.DataFrame({
        'risk_on_raw': risk_on,
        'risk_off_ok_raw': risk_off_ok,
    }, index=risk_prices.index)
    # 强制无未来函数：t-1 决策 t
    df['risk_on'] = df['risk_on_raw'].shift(1).fillna(False)
    df['risk_off_ok'] = df['risk_off_ok_raw'].shift(1).fillna(False)
    return df
