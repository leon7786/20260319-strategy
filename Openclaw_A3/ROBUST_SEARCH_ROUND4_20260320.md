# Robust Search Round 4 — 2026-03-20

这轮采用 **冠军邻域精扫（precision attack）**：

- 围绕当前 40.04% Full CAGR 冠军
- 继续保持 **binary + strict t-1 execution**
- 继续保留 **robust 约束**
- 在冠军邻域精确微调：
  - `LA`
  - `threshold`
  - `lev_low / lev_high`
  - `out leg`
  - `cross-asset filter`

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
| Frontier Obj | 67.37 |

## 本轮最优 frontier 候选

| 指标 | 数值 |
|---|---:|
| LA | 7.941 |
| Full CAGR | 37.66% |
| Full MDD | -69.1% |
| Old CAGR | 33.13% |
| Modern CAGR | 48.21% |
| Modern MDD | -49.1% |
| Min Block CAGR | 27.75% |
| Median Block CAGR | 38.03% |
| Gap | 15.07pp |
| RS Key | mix80 |
| RS Window | 2 |
| Out Leg | vfitx |
| Bond Mult | 3.00 |
| Threshold | 0.2308 |
| Lev Low | 0.10 |
| Lev High | 3.00 |
| Robust Obj | 69.63 |
| Frontier Obj | 69.82 |

## 本轮结论

- **仍然没有打破 40.04% Full CAGR**。
- 但出现了：
  - **20 个 robust objective 超过基线** 的候选。
- 说明：
  - 当前 40% 冠军作为纯收益解，非常难打破；
  - 但其稳健前沿已经被明显推进。

## Top 10 by Frontier Objective

| Tag | LA | Full CAGR | Full MDD | Old CAGR | Modern CAGR | Modern MDD | Min Block CAGR | Median Block CAGR | Gap | RS Key | Out Leg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| rand_25791 | 7.941 | 37.66% | -69.1% | 33.13% | 48.21% | -49.1% | 27.75% | 38.03% | 15.07pp | mix80 | vfitx |
| rand_67073 | 7.954 | 38.23% | -69.1% | 34.62% | 46.67% | -56.0% | 27.59% | 38.26% | 12.05pp | mix20 | mix20 |
| rand_89661 | 7.992 | 39.26% | -68.9% | 36.05% | 46.84% | -49.0% | 27.42% | 37.64% | 10.79pp | vfitx | vfitx |
| rand_27663 | 7.909 | 37.84% | -69.1% | 34.59% | 45.50% | -56.1% | 27.41% | 38.34% | 10.91pp | mix50 | mix20 |
| rand_92760 | 7.778 | 36.86% | -69.1% | 34.72% | 42.09% | -64.3% | 29.78% | 36.62% | 7.37pp | vfitx | mix50 |
| rand_31048 | 8.028 | 38.41% | -69.1% | 35.52% | 45.24% | -56.0% | 27.81% | 37.26% | 9.71pp | vfitx | mix20 |
| rand_91390 | 7.935 | 35.96% | -68.6% | 31.43% | 46.62% | -49.1% | 27.44% | 37.37% | 15.19pp | mix20 | vfitx |
| rand_27313 | 7.990 | 38.40% | -69.1% | 38.11% | 43.31% | -64.9% | 27.24% | 38.60% | 5.20pp | mix50 | mix50 |
| rand_2978 | 7.998 | 38.67% | -69.1% | 36.72% | 43.36% | -64.9% | 27.24% | 38.60% | 6.64pp | mix20 | mix50 |
| rand_45856 | 7.912 | 37.54% | -69.1% | 34.07% | 45.65% | -49.1% | 26.39% | 38.25% | 11.58pp | vustx | vfitx |
