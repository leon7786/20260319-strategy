# Openclaw_A9 · Curated Strategy Pack

> OpenClaw 当前筛出来的较优秀 IXIC **日频**策略合集。
> 核心原则：**无未来函数**、**T 日收盘生成信号，T+1 执行**、全部基于历史滚动指标。

## 回测设定

- **回测区间**：1995-01-03 ~ 2025-12-29
- **标的**：IXIC（Yahoo `^IXIC`）
- **初始资金**：$10,000
- **频率**：Daily
- **执行规则**：全部使用 `shift(1)` / T+1 执行

## 策略总览

| No. | 文件夹 | 类型 | CAGR | Max DD | Sharpe | 说明 |
|---|---|---|---:|---:|---:|---|
| 01 | `no1_QDKA_BestBlend_CAGR31_DD41` | QDKA 优化平衡版 | 31.01% | -41.41% | 0.94 | 当前最推荐，收益/回撤兼顾 |
| 02 | `no2_QDKA_SharpeMax_CAGR30_DD41` | QDKA 高 Sharpe 版 | 30.55% | -41.65% | 0.96 | Sharpe 更高，更稳一点 |
| 03 | `no3_QDKA_LowDD_CAGR29_DD40` | QDKA 低回撤版 | 29.95% | -40.13% | 0.95 | 更注重压回撤 |
| 04 | `no4_QDKA_Aggressive_CAGR32_DD43` | QDKA 激进版 | 32.27% | -43.82% | 0.95 | 冲更高 CAGR |
| 05 | `no5_AKVD_AdaptiveMomentum_CAGR21_DD45` | AKVD 原强策略 | 21.93% | -45.80% | 0.78 | 旧强基线之一 |

## 目录结构

```text
Openclaw_A9/
├── common.py
├── requirements.txt
├── no1_QDKA_BestBlend_CAGR31_DD41/
├── no2_QDKA_SharpeMax_CAGR30_DD41/
├── no3_QDKA_LowDD_CAGR29_DD40/
├── no4_QDKA_Aggressive_CAGR32_DD43/
└── no5_AKVD_AdaptiveMomentum_CAGR21_DD45/
```

## 运行方式

```bash
cd Openclaw_A9/no1_QDKA_BestBlend_CAGR31_DD41
python3 strategy.py
```

首次运行会自动下载 `^IXIC` 数据，并缓存到：

```text
Openclaw_A9/_cache/ixic_daily.csv
```

之后重复运行会优先使用本地缓存。

## 说明

- 这些是当前 OpenClaw 在本地工作区回测后筛出来的**较强版本**。
- 并非实盘建议；未纳入交易冲击、税费、真实融资成本、容量约束。
- 适合继续做 walk-forward、blind/OOS、参数敏感性测试。
