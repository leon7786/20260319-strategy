import math
import pandas as pd
import yfinance as yf

START='1995-01-03'
END_EXCLUSIVE='2025-12-30'
INIT=10000.0
LA=1.32
BASE_LEV=1.465
BOND_LEV=3.0
TARGET_VOL=0.10

BOND_ANNUAL={1995:0.31,1996:-0.01,1997:0.15,1998:0.14,1999:-0.09,2000:0.22,2001:0.04,2002:0.17,2003:0.02,2004:0.09,2005:0.07,2006:0.01,2007:0.10,2008:0.26,2009:-0.14,2010:0.10,2011:0.34,2012:0.03,2013:-0.14,2014:0.25,2015:-0.02,2016:0.01,2017:0.09,2018:-0.02,2019:0.15,2020:0.18,2021:-0.05,2022:-0.31,2023:-0.03,2024:-0.05,2025:0.03}

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
    bond_monthly=pd.Series(index=prices.index,dtype=float)
    for date in prices.index:
        ann=BOND_ANNUAL.get(date.year,0.05)
        bond_monthly.loc[date]=(1+ann)**(1/12)-1
    bond_monthly=bond_monthly.fillna(0.0)
    values=[INIT]; v=INIT
    for i in range(1,len(prices)):
        if signal.iloc[i-1]:
            lev=min(max(BASE_LEV*(TARGET_VOL/rvol.iloc[i-1]),0.1),3.0)
            v=max(v*(1+mr.iloc[i]*lev-0.0015*lev),1.0)
        else:
            v=max(v*(1+bond_monthly.iloc[i]*BOND_LEV-0.0005*BOND_LEV),1.0)
        values.append(v)
    pf=pd.Series(values,index=prices.index)
    years=(pf.index[-1]-pf.index[0]).days/365.25
    final=pf.iloc[-1]; total=final/INIT-1; cagr=(final/INIT)**(1/years)-1
    dd=pf/pf.cummax()-1; r=pf.pct_change().dropna(); sharpe=(r.mean()*12)/(r.std()*(12**0.5)) if r.std()>0 else 0
    print('策略: Top2 Local Dynamic Bond')
    print(f'最终价值: ${final:,.2f}')
    print(f'总收益: {total*100:.2f}%')
    print(f'年化CAGR: {cagr*100:.2f}%')
    print(f'最大回撤: {dd.min()*100:.2f}%')
    print(f'夏普: {sharpe:.2f}')

if __name__=='__main__':
    main()
