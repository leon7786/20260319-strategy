import math
import pandas as pd
import yfinance as yf

START='1995-01-03'
END_EXCLUSIVE='2025-12-30'
INIT=10000.0

PARAMS={
  "la": 3.32,
  "trend_ma": 12,
  "rv_window": 12,
  "base_target_vol": 0.178,
  "winter_mult": 1.883,
  "summer_mult": 1.302,
  "min_lev": 0.32,
  "max_lev": 3.0,
  "risk_off_asset": "VUSTX",
  "risk_off_lev": 2.48,
  "risk_off_mom_window": 0,
  "use_trend_filter": false
}

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
    return (prices>prices.rolling(ma).mean()).fillna(False)

def momentum_positive(prices, window):
    if window<=0:
        return pd.Series(True,index=prices.index)
    return (prices>prices.shift(window)).fillna(False)

def seasonal_target_vol(index, base_target_vol, winter_mult, summer_mult):
    vals=[]
    for dt in index:
        vals.append(base_target_vol*winter_mult if dt.month in (11,12,1,2,3,4) else base_target_vol*summer_mult)
    return pd.Series(vals,index=index,dtype=float)

def backtest(ixic, risk_off, p):
    ixic_ret=ixic.pct_change().fillna(0.0)
    risk_off_ret=risk_off.pct_change().fillna(0.0)
    mom_sig=fractional_momentum_signal(ixic,p['la'])
    trend_sig=rolling_ma_filter(ixic,p['trend_ma']) if p['use_trend_filter'] else pd.Series(True,index=ixic.index)
    in_sig=(mom_sig & trend_sig).fillna(False)
    off_sig=momentum_positive(risk_off,p['risk_off_mom_window'])
    rvol=ixic_ret.rolling(p['rv_window']).std().clip(lower=0.02).fillna(0.02)
    tv=seasonal_target_vol(ixic.index,p['base_target_vol'],p['winter_mult'],p['summer_mult'])
    lev=(tv/rvol).clip(lower=p['min_lev'], upper=p['max_lev'])
    vals=[INIT]; v=INIT
    for i in range(1,len(ixic)):
        if bool(in_sig.iloc[i-1]):
            l=float(lev.iloc[i-1])
            v=max(v*(1+float(ixic_ret.iloc[i])*l-0.0015*l),1.0)
        else:
            if bool(off_sig.iloc[i-1]):
                rl=float(p['risk_off_lev'])
                v=max(v*(1+float(risk_off_ret.iloc[i])*rl-0.0005*rl),1.0)
        vals.append(v)
    return pd.Series(vals,index=ixic.index)

def main():
    ixic=download_monthly('^IXIC')
    risk_off=download_monthly(PARAMS['risk_off_asset'])
    aligned=align_series({'IXIC':ixic,'RISK_OFF':risk_off})
    pf=backtest(aligned['IXIC'], aligned['RISK_OFF'], PARAMS)
    years=(pf.index[-1]-pf.index[0]).days/365.25
    final=pf.iloc[-1]; total=final/INIT-1; cagr=(final/INIT)**(1/years)-1
    dd=pf/pf.cummax()-1; r=pf.pct_change().dropna(); ann_vol=r.std()*(12**0.5) if len(r) else 0
    sharpe=(r.mean()*12)/(r.std()*(12**0.5)) if len(r) and r.std()>0 else 0
    print('策略: Top8 WalkForward Best OOS')
    print(f'最终价值: ${final:,.2f}')
    print(f'总收益: {total*100:.2f}%')
    print(f'年化CAGR: {cagr*100:.2f}%')
    print(f'年化波动: {ann_vol*100:.2f}%')
    print(f'最大回撤: {dd.min()*100:.2f}%')
    print(f'夏普: {sharpe:.2f}')

if __name__=='__main__':
    main()
