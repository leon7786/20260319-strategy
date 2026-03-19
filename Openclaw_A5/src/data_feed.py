import pandas as pd
import yfinance as yf

from config import START, END_EXCLUSIVE


def download_daily_close(ticker: str) -> pd.Series:
    raw = yf.download(ticker, start=START, end=END_EXCLUSIVE, interval='1d', auto_adjust=True, progress=False)
    if raw.empty:
        raise ValueError(f'No data for {ticker}')
    close = raw['Close'].dropna()
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close.name = ticker
    return close.astype(float)


def download_monthly_close(ticker: str) -> pd.Series:
    return download_daily_close(ticker).resample('ME').last().dropna().astype(float)


def align_series(series_map: dict[str, pd.Series]) -> pd.DataFrame:
    df = pd.concat(series_map.values(), axis=1, join='inner')
    df.columns = list(series_map.keys())
    return df.dropna()
