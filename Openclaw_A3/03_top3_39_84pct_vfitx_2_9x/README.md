# Top3_39.84pct_VFITX_2_9x

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
- 出局腿采用真实债券历史序列：**VUSTX 权重 0.0，VFITX 权重 1.0，债券杠杆 2.9x**

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
| Top3_39.84pct_VFITX_2_9x | $317,381,516 | 3173715.2% | 39.84% | -69.1% | 0.98 |

## 文件说明

- `strategy_03_top3_vfitx_2_9x.py`：该策略的可执行 Python 文件
- `common.py`：公共下载 / 因子 / 回测逻辑
- `summary.json`：策略摘要结果

## 运行方式

```bash
cd "/root/.openclaw/workspace-leader/20260319-strategy/repositories/Openclaw_A3/03_top3_39_84pct_vfitx_2_9x"
python3 strategy_03_top3_vfitx_2_9x.py
```
