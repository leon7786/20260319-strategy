# Top4_39.83pct_Mix20_3x

## 策略介绍

这是一条基于 **NASDAQ Composite（^IXIC）** 的动态仓位策略，核心思路如下：

- **LA = 8.01 个月动量窗口**，用于判断中期趋势
- 使用 **binary regime** 决策：
  - score >= 0.1952 时，切到 **高杠杆 3.00x** 的纳斯达克
  - 否则切到 **低杠杆 0.16x** 的纳斯达克
- 环境 score 由四类因子加权构成：
  - 趋势：0.360
  - 短周期动量：0.298
  - 波动率：0.327
  - 回撤：0.016
- 出局腿采用真实债券历史序列：**VUSTX 权重 0.2，VFITX 权重 0.8，债券杠杆 3.0x**

## 关键参数

- `mom_cap = 0.159312`
- `short_w = 2`
- `short_cap = 0.178646`
- `vol_w = 2`
- `vol_lo = 0.012525`
- `vol_hi = 0.027313`
- `dd_w = 9`
- `dd_floor = -0.180789`

## 回测指标

| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| Top4_39.83pct_Mix20_3x | $316,632,957 | 3166229.6% | 39.83% | -69.1% | 0.97 |

## 文件说明

- `strategy_04_top4_mix20_3x.py`：该策略的可执行 Python 文件
- `common.py`：公共下载 / 因子 / 回测逻辑
- `summary.json`：策略摘要结果

## 运行方式

```bash
cd "/root/.openclaw/workspace-leader/20260319-strategy/repositories/Openclaw_A3/04_top4_39_83pct_mix20_3x"
python3 strategy_04_top4_mix20_3x.py
```
