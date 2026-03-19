# Openclaw_A9 · Curated Strategy Pack

> 持续进化中的 OpenClaw 自研策略库：保留旧版本，同时不断吸收外部仓库的有效结构，在**无未来函数 / T+1 执行 / 历史滚动指标**约束下迭代。

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
| 06 | `no6_A9_HybridBalanced_CAGR31_DD38` | A9 新设计平衡版 | 31.68% | -38.97% | 1.12 | 更偏现实可持有，回撤控制更好 |
| 07 | `no7_A9_HybridAggressive_CAGR34_DD43` | A9 新设计进攻版 | 34.80% | -43.35% | 1.11 | 比旧 no4 更强的进攻升级版 |
| 08 | `no8_A9_HybridRobust_CAGR35_DD44` | A9 新设计综合最强版 | 35.65% | -44.85% | 1.10 | 在 full/OOS/walk-forward 合成评分下第一 |


## A9 v2 新增策略（本轮新增）

这次新增的 `no6 ~ no8` 不是旧策略简单换参数，而是重新设计后的 **A9 Hybrid family**：

- 保留 **QDKA downside-vol sizing** 主干
- 加入 **seasonality target-vol**
- 加入 **panic momentum filter**
- 加入 **drawdown soft de-leveraging**
- 加入 **bond fallback with momentum gate**
- 全部保持 **T+1 执行**

### 新增策略定位

- **no6** → 更偏现实可持有 / 回撤控制更好
- **no7** → 更偏高质量进攻版
- **no8** → 在 full / OOS / walk-forward 合成评分下最强

## 目录结构

```text
Openclaw_A9/
├── common.py
├── requirements.txt
├── no1_QDKA_BestBlend_CAGR31_DD41/
├── no2_QDKA_SharpeMax_CAGR30_DD41/
├── no3_QDKA_LowDD_CAGR29_DD40/
├── no4_QDKA_Aggressive_CAGR32_DD43/
├── no5_AKVD_AdaptiveMomentum_CAGR21_DD45/
├── no6_A9_HybridBalanced_CAGR31_DD38/
├── no7_A9_HybridAggressive_CAGR34_DD43/
├── no8_A9_HybridRobust_CAGR35_DD44/
└── ... (future no9 / no10 / more)
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


## 使用建议

- 想要 **更稳、更像现实可持有版本** → 优先看 `no6_A9_HybridBalanced_CAGR31_DD38`
- 想要 **更高收益、同时不明显恶化回撤** → 看 `no7_A9_HybridAggressive_CAGR34_DD43`
- 想要 **综合评分最强** → 看 `no8_A9_HybridRobust_CAGR35_DD44`

## 风险提示

这些结果仍然是历史回测，不包含：
- 实盘冲击成本
- 真实融资与借券成本
- 税费
- 容量限制

所以建议把它们视为 **研究策略原型**，下一步仍应做：
- blind / OOS
- walk-forward
- 分时代稳健性验证
- 参数敏感性分析
