import math
import pandas as pd
import yfinance as yf

START='1995-01-03'
END_EXCLUSIVE='2025-12-30'
INIT=10000.0
LA=1.50
BASE_LEV=1.45
TARGET_VOL=0.10

def signal_from_fractional_la(prices, la):
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

def main():
    raw=yf.download('^IXIC', start=START, end=END_EXCLUSIVE, interval='1d', auto_adjust=True, progress=False)
    prices=raw['Close'].dropna()
    if isinstance(prices,pd.DataFrame): prices=prices.iloc[:,0]
    prices=prices.resample('ME').last().dropna().astype(float)
    mr=prices.pct_change().fillna(0.0)
    rvol=mr.rolling(3).std().clip(lower=0.025).fillna(0.025)
    signal=signal_from_fractional_la(prices, LA)
    values=[INIT]; v=INIT
    for i in range(1,len(prices)):
        if signal.iloc[i-1]:
            lev=min(max(BASE_LEV*(TARGET_VOL/rvol.iloc[i-1]),0.1),3.0)
            v=max(v*(1+mr.iloc[i]*lev-0.0015*lev),1.0)
        values.append(v)
    pf=pd.Series(values,index=prices.index)
    years=(pf.index[-1]-pf.index[0]).days/365.25
    final=pf.iloc[-1]; total=final/INIT-1; cagr=(final/INIT)**(1/years)-1
    dd=pf/pf.cummax()-1; r=pf.pct_change().dropna(); sharpe=(r.mean()*12)/(r.std()*(12**0.5)) if r.std()>0 else 0
    print('策略: Top5 Dynamic Cash')
    print(f'最终价值: ${final:,.2f}')
    print(f'总收益: {total*100:.2f}%')
    print(f'年化CAGR: {cagr*100:.2f}%')
    print(f'最大回撤: {dd.min()*100:.2f}%')
    print(f'夏普: {sharpe:.2f}')

if __name__=='__main__':
    main()
