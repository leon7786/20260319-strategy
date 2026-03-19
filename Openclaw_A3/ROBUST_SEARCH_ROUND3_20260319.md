# Robust Search Round 3 — 2026-03-19

这一轮新增了 **cross-asset regime filter**，但仍保持：

- **binary regime**
- **严格 t-1 执行**
- **不引入复杂状态机**
- **继续避免未来函数**
- **继续抑制过拟合**

## 新增因子

除了原来的：
- 趋势
- 短周期动量
- 波动率
- 回撤

本轮新增：
- **Nasdaq / Bond 相对强弱（relative strength）**

也就是把跨资产关系纳入 score，但不靠复杂结构硬堆参数。

## 基线（40.04% 全样本冠军）

| 指标 | 数值 |
|---|---:|
| Full CAGR | 40.04% |
| Full MDD | -69.1% |
| Old CAGR | 37.24% |
| Modern CAGR | 46.72% |
| Modern MDD | -49.2% |
| Min Block CAGR | 24.78% |
| Median Block CAGR | 37.71% |
| Gap | 9.48pp |
| Robust Obj | 67.33 |

## 本轮最稳健候选

| 指标 | 数值 |
|---|---:|
| LA | 7.99 |
| Full CAGR | 36.43% |
| Full MDD | -67.2% |
| Old CAGR | 33.33% |
| Modern CAGR | 43.75% |
| Modern MDD | -62.1% |
| Min Block CAGR | 27.76% |
| Median Block CAGR | 37.56% |
| Gap | 10.42pp |
| Robust Obj | 67.99 |
| RS Key | vfitx |
| RS Window | 4 |
| Out Leg | mix20 |
| Bond Mult | 3.00 |

## 本轮结论

- cross-asset regime filter **有用**。
- 这一轮找到了 **1 个 robust objective 超过基线** 的候选。
- 但目前仍然**没有打破 40.04% 全样本 CAGR**。
- 说明跨资产 filter 更像是在提高稳健性，而不是直接把收益上限抬穿。

## Top 10 by Robust Objective

| Tag | LA | Full CAGR | Full MDD | Old CAGR | Modern CAGR | Modern MDD | Min Block CAGR | Median Block CAGR | Gap | RS Key | Out Leg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| rand_1671 | 7.99 | 36.43% | -67.2% | 33.33% | 43.75% | -62.1% | 27.76% | 37.56% | 10.42pp | vfitx | mix20 |
| baseline | 8.01 | 40.04% | -69.1% | 37.24% | 46.72% | -49.2% | 24.78% | 37.71% | 9.48pp | vfitx | vfitx |
| rand_48527 | 7.94 | 36.36% | -66.3% | 33.17% | 43.88% | -53.7% | 25.95% | 36.27% | 10.72pp | vustx | mix20 |
| rand_23653 | 7.91 | 33.76% | -61.8% | 31.61% | 42.65% | -56.2% | 26.54% | 35.33% | 11.04pp | mix20 | mix20 |
| rand_23219 | 7.79 | 31.14% | -68.6% | 28.83% | 36.62% | -60.0% | 29.01% | 34.43% | 7.80pp | vfitx | mix50 |
| rand_38911 | 7.92 | 35.79% | -69.1% | 34.08% | 39.93% | -56.3% | 25.88% | 36.15% | 5.86pp | mix50 | vfitx |
| rand_22956 | 7.78 | 33.97% | -69.1% | 32.12% | 38.43% | -56.3% | 25.35% | 37.70% | 6.30pp | mix50 | vfitx |
| rand_17092 | 7.93 | 33.35% | -67.0% | 28.25% | 45.38% | -56.1% | 27.15% | 34.39% | 17.13pp | mix80 | vfitx |
| rand_15075 | 7.88 | 33.73% | -68.5% | 31.50% | 42.74% | -48.9% | 23.76% | 37.83% | 11.23pp | mix20 | vfitx |
| rand_42969 | 8.02 | 35.17% | -61.8% | 34.19% | 41.46% | -56.0% | 24.43% | 37.04% | 7.28pp | vustx | mix20 |
