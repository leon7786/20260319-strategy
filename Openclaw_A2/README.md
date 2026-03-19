# Openclaw_A2 · Top5 Strategy Suite

> 基于 IXIC + VUSTX（1995-01-03 ~ 2025-12-29）的无未来函数月度策略组合。

## ✨ 策略目录（精简概要）

| 编号 | 文件夹 | 概要 |
|---|---|---|
| 01 | `01_AlphaPulse_Trend12_Vol18_12_Bond9_Slip05` | 高进攻主策略，收益最高 |
| 02 | `02_NovaBalance_Trend12_Vol16_12_Bond9_Slip05` | 平衡版本，Sharpe 更优 |
| 03 | `03_AlphaPulse_Trend12_Vol18_12_Bond9_Slip10` | Top1 高滑点压力测试 |
| 04 | `04_NovaBalance_Trend12_Vol16_12_Bond9_Slip10` | Top2 高滑点压力测试 |
| 05 | `05_AlphaPulse_Trend12_Vol18_12_Bond6_Slip05` | 债券动量窗口更短版本 |

## 📊 汇总表现

| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| Top1 · AlphaPulse | $11,133,412 | 111,234.1% | 25.47% | -49.59% | 0.76 |
| Top2 · NovaBalance | $11,054,837 | 110,448.4% | 25.44% | -49.82% | 0.77 |
| Top3 · AlphaPulse (High Slip) | $10,917,428 | 109,074.3% | 25.39% | -49.68% | 0.76 |
| Top4 · NovaBalance (High Slip) | $10,840,284 | 108,302.8% | 25.36% | -49.92% | 0.77 |
| Top5 · AlphaPulse (Bond6) | $10,761,002 | 107,510.0% | 25.33% | -50.75% | 0.76 |

## 📁 目录结构

```text
Openclaw_A2/
├── common.py
├── 01_AlphaPulse_Trend12_Vol18_12_Bond9_Slip05/
├── 02_NovaBalance_Trend12_Vol16_12_Bond9_Slip05/
├── 03_AlphaPulse_Trend12_Vol18_12_Bond9_Slip10/
├── 04_NovaBalance_Trend12_Vol16_12_Bond9_Slip10/
└── 05_AlphaPulse_Trend12_Vol18_12_Bond6_Slip05/
```

## 🧠 统一框架

- 趋势开关：`IXIC > MA(12)` 才进入风险资产
- 动态杠杆：`0.1x ~ 3.0x`（由近 3 个月波动率驱动）
- 季节目标波动率：旺季（11~4）高，淡季（5~10）低
- 风险外资产：VUSTX 债券动量为正时启用（2x），否则现金
- 全部策略都使用 **t-1 决策 t**（避免未来函数）
