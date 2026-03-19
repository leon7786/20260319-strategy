# Openclaw_A2 · Top5 Strategy Suite

> 无未来函数（t-1 决策 t）的 IXIC + VUSTX **日度**策略合集。

## 📊 与 Buy&Hold 对比（含最大回撤）

| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| **S5_Alpha_Strike (NEW)** | $49,703,552 | 496,935.5% | **31.61%** | **-48.45%** | 0.95 |
| S3_AggressiveEdge | $38,939,358 | 389,293.6% | 30.58% | -49.67% | 0.93 |
| **S1_BalancedBreakout** | $35,898,857 | 358,888.6% | 30.24% | -48.78% | 0.98 |
| S6_Balanced_Plus (NEW) | $24,246,270 | 242,362.7% | 28.60% | -47.87% | 0.93 |
| S2_LowDDMomentum | $26,663,412 | 266,534.1% | 28.99% | -43.72% | 0.97 |
| S4_Defensive_Armor (NEW) | $12,577,942 | 125,679.4% | 25.90% | -43.31% | 0.94 |
| Top5 · AlphaPulse (Bond6) | $2,206,836 | 21,968.4% | 19.02% | -68.78% | 0.64 |
| Top1 · AlphaPulse | $1,996,343 | 19,863.4% | 18.64% | -66.99% | 0.63 |
| Top2 · NovaBalance | $1,964,628 | 19,546.3% | 18.58% | -64.51% | 0.63 |
| Top3 · AlphaPulse (High Slip) | $1,835,948 | 18,259.5% | 18.32% | -67.34% | 0.62 |
| Top4 · NovaBalance (High Slip) | $1,806,828 | 17,968.3% | 18.26% | -64.89% | 0.62 |
| Buy&Hold (IXIC) | $315,694 | 3,056.9% | 11.79% | -77.93% | 0.58 |


## 📌 回测设定

- **回测区间**：1995-01-03 ~ 2025-12-29
- **样本标的**：IXIC（NASDAQ Composite）+ VUSTX（长期美债基金）
- **数据频率**：**日度（Daily）**
- **初始资金（成本）**：**$10,000**
- **执行规则**：全部策略使用 `t-1` 信号执行 `t` 日交易
- **窗口换算**：策略参数仍沿用“月语义”，内部自动换算为交易日（约 21 日/月）

## 📆 每年收益对比（%）

| 年份 | Buy&Hold | S1_BalancedBreakout | S2_LowDDMomentum |
|---:|---:|---:|---:|
| 1996 | 22.0% | 74.3% | 23.3% |
| 1997 | 22.6% | 82.6% | 46.1% |
| 1998 | 38.6% | 192.1% | 215.1% |
| 1999 | 84.3% | 89.1% | 86.8% |
| 2000 | -40.2% | 12.4% | -4.4% |
| 2001 | -14.9% | -6.9% | 4.8% |
| 2002 | -32.5% | 33.1% | 12.8% |
| 2003 | 44.7% | 73.3% | 75.3% |
| 2004 | 8.4% | 3.8% | 0.9% |
| 2005 | 2.5% | 15.2% | -8.5% |
| 2006 | 7.6% | 12.8% | 8.0% |
| 2007 | 9.5% | 4.9% | 6.5% |
| 2008 | -39.6% | 21.6% | 17.5% |
| 2009 | 39.0% | -0.2% | 11.5% |
| 2010 | 14.9% | 36.0% | -10.5% |
| 2011 | -3.2% | -22.9% | -30.0% |
| 2012 | 14.0% | 52.2% | 23.5% |
| 2013 | 34.2% | 29.7% | 68.3% |
| 2014 | 14.3% | 33.1% | 14.9% |
| 2015 | 5.9% | -18.5% | -32.5% |
| 2016 | 9.8% | -3.7% | -3.2% |
| 2017 | 27.2% | 45.2% | 80.8% |
| 2018 | -5.3% | -7.0% | -21.4% |
| 2019 | 34.6% | 74.1% | 39.3% |
| 2020 | 41.8% | 117.7% | 40.5% |
| 2021 | 23.2% | 17.9% | 51.5% |
| 2022 | -33.9% | -18.6% | -24.4% |
| 2023 | 44.5% | 28.3% | 29.0% |
| 2024 | 30.8% | 58.8% | 75.3% |
| 2025 | 21.5% | 29.1% | -7.2% |



## ✨ 策略目录（精简概要）

| 编号 | 文件夹 | 概要 |
|---|---|---|
| 01 | `01_AlphaPulse_Trend12_Vol18_12_Bond9_Slip05` | 高进攻主策略，收益最高 |
| 02 | `02_NovaBalance_Trend12_Vol16_12_Bond9_Slip05` | 平衡版本，Sharpe 更优 |
| 03 | `03_AlphaPulse_Trend12_Vol18_12_Bond9_Slip10` | Top1 高滑点压力测试 |
| 04 | `04_NovaBalance_Trend12_Vol16_12_Bond9_Slip10` | Top2 高滑点压力测试 |
| 05 | `05_AlphaPulse_Trend12_Vol18_12_Bond6_Slip05` | 债券动量窗口更短版本 |
| 09 | `09_S4_Defensive_Armor` | 新增防守型：回撤明显更低（-43.31%） |
| 10 | `10_S5_Alpha_Strike` | 新增进攻型：收益与回撤双维度优于 S1 |
| 11 | `11_S6_Balanced_Plus` | 新增均衡型：收益/回撤折中优化版本 |


## 🧬 S1 是如何诞生的？(Evolution of S1)

S1 (BalancedBreakout) 并非凭空发明的神奇指标，而是基于华尔街经典量化骨架，在**严苛的实盘沙盒**里“暴力寻优”出来的混血儿。

### 1. 经典骨架
- **CTA 趋势跟踪**：长周期均线过滤大熊市。
- **AQR 波动率平价**：波动率低时加杠杆，波动率飙升时自动降杠杆。
- **动量与季节性**：结合绝对动量与美股历史季节效应。
- **硬性风控**：从高点回撤超过阈值强制削减杠杆（冷血熔断器）。

### 2. 真实物理定律沙盒
很多开源的高分策略（如一些大模型生成的初始代码或带未来函数的代码）通病是“在无摩擦的温室里过拟合”。为了解决这个问题，S1 的寻优环境自带真实物理法则：
- **零未来函数**：强制 T-1 信号计算，T 日执行。
- **真实摩擦**：强制扣除万8滑点和杠杆管理费。
- **资金成本**：强制计算开杠杆融资借贷带来的真实利息损耗。

### 3. 大逃杀寻优
我们将成千上万种参数组合放入上述严酷的沙盒中跑了 4000 次以上的高强度模拟。绝大多数策略要么因为换手太频繁被滑点“吸血”致死，要么在 2000 年科网泡沫或 2008 年次贷危机中爆仓。
**S1（BalancedBreakout）** 是在这场大逃杀中跑出来的最优解：它聪明地找到了一个极佳的**平衡点**——换手率低（规避了滑点损耗），熔断机制足够深（避开了假摔但防住了真死）。在硬扛住了所有真实摩擦后，依然斩获了 **30.24% 的年化和 -48.78% 的回撤**。这也是为什么它是目前最具备实盘落地价值的版本。

## 📁 目录结构

```text
Openclaw_A2/
├── common.py
├── 01_AlphaPulse_Trend12_Vol18_12_Bond9_Slip05/
├── 02_NovaBalance_Trend12_Vol16_12_Bond9_Slip05/
├── 03_AlphaPulse_Trend12_Vol18_12_Bond9_Slip10/
├── 04_NovaBalance_Trend12_Vol16_12_Bond9_Slip10/
├── 05_AlphaPulse_Trend12_Vol18_12_Bond6_Slip05/
├── 06_BalancedBreakout_DailyClose_AntiLookahead/
├── 07_LowDDMomentum_DailyClose_AntiLookahead/
├── 08_AggressiveEdge_DailyClose_AntiLookahead/
├── 09_S4_Defensive_Armor/
├── 10_S5_Alpha_Strike/
└── 11_S6_Balanced_Plus/
```


## 🔬 终极自我审查 (Self-Audit with Pure Daily Shift)

很多开源策略把指标和交易写在同一天（T日信号T日吃收益）造成未来函数。为了彻底自证清白，本仓库提供的 `strategy.py` 以及下方的自查脚本，严格将所有技术指标（MA、Momentum、Vol、Drawdown）计算完毕后，统一执行 **`.shift(1)`**。也就是说，只有在 **T-1 日收盘后**能看到的数据，才会用来决定 **T 日**的杠杆和仓位。

你可以随时用以下最极简、无任何封装的 Pandas 脚本来交叉验证 S1 的真实收益（确保无未来函数、有摩擦成本）：

```python
import pandas as pd, numpy as np
import yfinance as yf

# 1. 下载最纯粹的日线数据
ix = yf.download('^IXIC', start='1995-01-03', end='2025-12-29', interval='1d', auto_adjust=True, progress=False)['Close'].dropna()
bd = yf.download('VUSTX', start='1995-01-03', end='2025-12-29', interval='1d', auto_adjust=True, progress=False)['Close'].dropna()
df = pd.concat([ix.rename('IXIC'), bd.rename('BOND')], axis=1).dropna()
rix, rb = df['IXIC'].pct_change().fillna(0), df['BOND'].pct_change().fillna(0)

# 2. S1 核心参数
p = {
    'ma_w': 273, 'mom_w': 40, 'mom_thr': -0.05, 'vol_w': 21, 
    'tv_str': 0.16, 'tv_wk': 0.14, 'min_lev': 0.1, 'max_lev': 2.8, 
    'blook': 84, 'bmult': 2.0, 'slip': 0.0008, 'month_cost': 0.0015, 
    'dd_w': 252, 'dd_thr': -0.30, 'dd_lev_cut': 0.7, 'panic_mom_w': 20, 'panic_mom_thr': 0.0
}

# 3. T 日指标计算
ma = df['IXIC'].rolling(p['ma_w']).mean()
mom = df['IXIC'] / df['IXIC'].shift(p['mom_w']) - 1
vol = rix.rolling(p['vol_w']).std()
rh = df['IXIC'].rolling(p['dd_w']).max()
bm = df['BOND'] / df['BOND'].shift(p['blook']) - 1
pm = df['IXIC'] / df['IXIC'].shift(p['panic_mom_w']) - 1

# 4. 核心：全部指标强行 Shift(1) 退后一天，杜绝未来函数
ma_prev, mom_prev, vol_prev = ma.shift(1), mom.shift(1), vol.shift(1)
rh_prev, bm_prev, pm_prev = rh.shift(1), bm.shift(1), pm.shift(1)
ix_prev = df['IXIC'].shift(1)

nav = np.full(len(df), np.nan); nav[0] = 10000.0; v = 10000.0; inr = False
cost = p['month_cost'] / 21; bcost = (0.0006 * p['bmult']) / 21
tvs, tvw = p['tv_str'] / np.sqrt(21), p['tv_wk'] / np.sqrt(21)

# 5. 日频滚动回测
for i in range(1, len(df)):
    tv = tvs if df.index[i-1].month in (11, 12, 1, 2, 3, 4) else tvw
    
    # 风险开关 (基于 T-1)
    risk = False
    if pd.notna(ma_prev.iloc[i]) and pd.notna(mom_prev.iloc[i]):
        risk = (ix_prev.iloc[i] > ma_prev.iloc[i]) and (mom_prev.iloc[i] > p['mom_thr'])
    if pd.notna(pm_prev.iloc[i]) and pm_prev.iloc[i] < p['panic_mom_thr']:
        risk = False
        
    # 动态杠杆与熔断 (基于 T-1)
    lev = p['min_lev']
    if pd.notna(vol_prev.iloc[i]) and vol_prev.iloc[i] > 1e-12:
        lev = tv / vol_prev.iloc[i]
    lev = max(p['min_lev'], min(p['max_lev'], lev))
    if pd.notna(rh_prev.iloc[i]) and rh_prev.iloc[i] > 0 and (ix_prev.iloc[i] / rh_prev.iloc[i] - 1) < p['dd_thr']:
        lev = max(p['min_lev'], min(p['max_lev'], lev * p['dd_lev_cut']))
        
    # 执行当天的真实涨跌 (T 日)
    turn = 1.0 if risk != inr else 0.0; inr = risk
    if risk:
        v *= (1 + rix.iloc[i] * lev - cost * lev - p['slip'] * turn)
    else:
        if pd.notna(bm_prev.iloc[i]) and bm_prev.iloc[i] > 0:
            v *= (1 + rb.iloc[i] * p['bmult'] - bcost - p['slip'] * turn)
        else:
            v *= (1 - p['slip'] * turn)
    nav[i] = max(v, 1.0)

nav_s = pd.Series(nav, index=df.index)
cagr = (nav_s.iloc[-1] / 10000.0) ** (1 / ((df.index[-1] - df.index[0]).days / 365.25)) - 1
dd = (nav_s / nav_s.cummax() - 1).min()
print(f"S1 Pure Daily Reality Check -> CAGR: {cagr*100:.2f}% | Max DD: {dd*100:.2f}%")
```

