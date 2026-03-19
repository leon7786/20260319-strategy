# Openclaw_A2 · Top5 Strategy Suite

> 无未来函数（t-1 决策 t）的 IXIC + VUSTX 月度策略合集。

## 📊 汇总表现（Top5）

| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| Top1 · AlphaPulse | $11,133,412 | 111,234.1% | 25.47% | -49.59% | 0.76 |
| Top2 · NovaBalance | $11,054,837 | 110,448.4% | 25.44% | -49.82% | 0.77 |
| Top3 · AlphaPulse (High Slip) | $10,917,428 | 109,074.3% | 25.39% | -49.68% | 0.76 |
| Top4 · NovaBalance (High Slip) | $10,840,284 | 108,302.8% | 25.36% | -49.92% | 0.77 |
| Top5 · AlphaPulse (Bond6) | $10,761,002 | 107,510.0% | 25.33% | -50.75% | 0.76 |

## 📌 回测设定

- **回测区间**：1995-01-03 ~ 2025-12-29
- **样本标的**：IXIC（NASDAQ Composite）+ VUSTX（长期美债基金）
- **数据频率**：月度（由日线重采样）
- **初始资金（成本）**：**$10,000**
- **交易成本模型**：杠杆成本 + 切换滑点（见各策略参数）

## ✨ 策略目录（精简概要）

| 编号 | 文件夹 | 概要 |
|---|---|---|
| 01 | `01_AlphaPulse_Trend12_Vol18_12_Bond9_Slip05` | 高进攻主策略，收益最高 |
| 02 | `02_NovaBalance_Trend12_Vol16_12_Bond9_Slip05` | 平衡版本，Sharpe 更优 |
| 03 | `03_AlphaPulse_Trend12_Vol18_12_Bond9_Slip10` | Top1 高滑点压力测试 |
| 04 | `04_NovaBalance_Trend12_Vol16_12_Bond9_Slip10` | Top2 高滑点压力测试 |
| 05 | `05_AlphaPulse_Trend12_Vol18_12_Bond6_Slip05` | 债券动量窗口更短版本 |

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
