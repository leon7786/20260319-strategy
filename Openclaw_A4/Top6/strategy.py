import math
import pandas as pd
import yfinance as yf

START='1995-01-03'
END_EXCLUSIVE='2025-12-30'
INIT=10000.0

BOND_ANNUAL={1995:0.31,1996:-0.01,1997:0.15,1998:0.14,1999:-0.09,2000:0.22,2001:0.04,2002:0.17,2003:0.02,2004:0.09,2005:0.07,2006:0.01,2007:0.10,2008:0.26,2009:-0.14,2010:0.10,2011:0.34,2012:0.03,2013:-0.14,2014:0.25,2015:-0.02,2016:0.01,2017:0.09,2018:-0.02,2019:0.15,2020:0.18,2021:-0.05,2022:-0.31,2023:-0.03,2024:-0.05,2025:0.03}

def download_monthly(ticker):
    raw=yf.download(ticker,start=START,end=END_EXCLUSIVE,interval='1d',auto_adjust=True,progress=False)
    close=raw['Close'].dropna()
    if isinstance(close,pd.DataFrame): close=close.iloc[:,0]
    return close.resample('ME').last().dropna().astype(float)

def align_series(series_map):
    df=pd.concat(series_map.values(),axis=1,join='inner')
    df.columns=list(series_map.keys())
    return df.dropna()

def fractional_momentum_signal(prices, la):
    vals=prices.values
    low=max(1,int(math.floor(la))); high=max(1,int(math.ceil(la)))
    sig=pd.Series(False,index=prices.index)
    if low==high:
        sig.iloc[low:]=vals[low:]>vals[:-low]
        return sig
    frac=la-low; start=high
    low_ref=vals[start-low:len(vals)-low]
    high_ref=vals[start-high:len(vals)-high]
    ref=(1-frac)*low_ref+frac*high_ref
    sig.iloc[start:]=vals[start:]>ref
    return sig

def rolling_ma_filter(prices, ma):
    if ma<=0:
        return pd.Series(True,index=prices.index)
    r=prices.rolling(ma).mean()
    return (prices>r).fillna(False)

def momentum_positive(prices, window):
    if window<=0:
        return pd.Series(True,index=prices.index)
    return (prices>prices.shift(window)).fillna(False)

def seasonal_target_vol(index, base_target_vol, winter_mult, summer_mult):
    vals=[]
    for dt in index:
        if dt.month in (11,12,1,2,3,4):
            vals.append(base_target_vol*winter_mult)
        else:
            vals.append(base_target_vol*summer_mult)
    return pd.Series(vals,index=index,dtype=float)

def backtest(ixic, risk_off, la, trend_ma, rv_window, base_target_vol, winter_mult, summer_mult, min_lev, max_lev, risk_off_lev, risk_off_mom_window, use_trend_filter):
    ixic_ret=ixic.pct_change().fillna(0.0)
    risk_off_ret=risk_off.pct_change().fillna(0.0)
    mom_sig=fractional_momentum_signal(ixic, la)
    trend_sig=rolling_ma_filter(ixic, trend_ma) if use_trend_filter else pd.Series(True,index=ixic.index)
    in_sig=(mom_sig & trend_sig).fillna(False)
    off_sig=momentum_positive(risk_off, risk_off_mom_window)
    rvol=ixic_ret.rolling(rv_window).std().clip(lower=0.02).fillna(0.02)
    tv=seasonal_target_vol(ixic.index, base_target_vol, winter_mult, summer_mult)
    lev=(tv/rvol).clip(lower=min_lev, upper=max_lev)
    vals=[INIT]
    v=INIT
    for i in range(1,len(ixic)):
        if bool(in_sig.iloc[i-1]):
            l=float(lev.iloc[i-1])
            v=max(v*(1+float(ixic_ret.iloc[i])*l-0.0015*l),1.0)
        else:
            if bool(off_sig.iloc[i-1]):
                rl=float(risk_off_lev)
                v=max(v*(1+float(risk_off_ret.iloc[i])*rl-0.0005*rl),1.0)
        vals.append(v)
    return pd.Series(vals,index=ixic.index)


def main():
    ixic=download_monthly('^IXIC')
    risk_off=download_monthly('VUSTX')
    aligned=align_series({'IXIC':ixic,'RISK_OFF':risk_off})
    ixic=aligned['IXIC']
    risk_off=aligned['RISK_OFF']
    pf=backtest(
        ixic=ixic,
        risk_off=risk_off,
        la=1.08,
        trend_ma=3,
        rv_window=3,
        base_target_vol=0.151,
        winter_mult=1.0,
        summer_mult=1.349,
        min_lev=0.05,
        max_lev=3.0,
        risk_off_lev=2.89,
        risk_off_mom_window=2,
        use_trend_filter=False
    )
    years=(pf.index[-1]-pf.index[0]).days/365.25
    final=pf.iloc[-1]
    total=final/INIT-1
    cagr=(final/INIT)**(1/years)-1
    dd=pf/pf.cummax()-1
    r=pf.pct_change().dropna()
    ann_vol=r.std()*(12**0.5) if len(r) else 0
    sharpe=(r.mean()*12)/(r.std()*(12**0.5)) if len(r) and r.std()>0 else 0
    print('策略: Top6')
    print(f'最终价值: ${final:,.2f}')
    print(f'总收益: {total*100:.2f}%')
    print(f'年化CAGR: {cagr*100:.2f}%')
    print(f'年化波动: {ann_vol*100:.2f}%')
    print(f'最大回撤: {dd.min()*100:.2f}%')
    print(f'夏普: {sharpe:.2f}')

if __name__=='__main__':
    main()
