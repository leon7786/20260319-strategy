import math
import pandas as pd


def fractional_momentum_signal(prices: pd.Series, la: float) -> pd.Series:
    vals = prices.values
    low = max(1, int(math.floor(la)))
    high = max(1, int(math.ceil(la)))
    sig = pd.Series(False, index=prices.index)
    if low == high:
        sig.iloc[low:] = vals[low:] > vals[:-low]
        return sig
    frac = la - low
    start = high
    low_ref = vals[start - low: len(vals) - low]
    high_ref = vals[start - high: len(vals) - high]
    ref = (1 - frac) * low_ref + frac * high_ref
    sig.iloc[start:] = vals[start:] > ref
    return sig


def rolling_ma_filter(prices: pd.Series, ma: int) -> pd.Series:
    if ma <= 0:
        return pd.Series(True, index=prices.index)
    return (prices > prices.rolling(ma).mean()).fillna(False)


def momentum_positive(prices: pd.Series, window: int) -> pd.Series:
    if window <= 0:
        return pd.Series(True, index=prices.index)
    return (prices > prices.shift(window)).fillna(False)


def realized_vol(returns: pd.Series, window: int) -> pd.Series:
    return returns.rolling(window).std().clip(lower=0.02).fillna(0.02)


def seasonal_target_vol(index: pd.DatetimeIndex, base_target_vol: float, winter_mult: float, summer_mult: float) -> pd.Series:
    vals = []
    for dt in index:
        vals.append(base_target_vol * winter_mult if dt.month in (11, 12, 1, 2, 3, 4) else base_target_vol * summer_mult)
    return pd.Series(vals, index=index, dtype=float)
