> ⚠️ Audit warning: 当前这条月度 NASDAQ 策略线使用了 `BOND_ANNUAL` 年度映射折算 bond-side 月收益，存在 future leak / 前视偏差。以下指标暂不可视为有效实盘或严谨回测结果，需重算。

# Top4_refine_m13_13_tv0p15_max4p5_min1p5

## 策略简介
Top4 版本综合了较低 target vol 与较低 min lev，在风险和收益之间形成另一条强候选路径。

## 核心逻辑
- 标的：NASDAQ / IXIC（月度）
- 动量信号：13 个月动量主簇
- 风控：单月跌幅达到阈值后触发 cooldown
- 杠杆：目标波动率动态杠杆，最高 4.5x
- 空仓资产：仅在正债券年切换 2x bond，否则持有 cash
- 执行方式：月末信号，次月收益生效

## 回测指标
| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| refine_m13_13_vw2_tv0.15_max4.5_min1.5_b0.0_cr-0.09_cd1_bond2x_pos | $74,362,992.28 | 743529.92% | 33.43% | -71.34% | 0.80 |

## 文件说明
- `strategy_nasdaq_monthly_refine_top4.py`：该策略独立 Python 入口文件
- `strategy_nasdaq_monthly_refine_runner.py`：共享回测 runner
- `refine_m13_13_vw2_tv0p15_max4p5_min1p5_b0p0_crneg0p09_cd1_bond2x_pos_summary.csv`：指标摘要
- `refine_m13_13_vw2_tv0p15_max4p5_min1p5_b0p0_crneg0p09_cd1_bond2x_pos_equity.csv`：净值曲线
- `refine_m13_13_vw2_tv0p15_max4p5_min1p5_b0p0_crneg0p09_cd1_bond2x_pos_decisions.csv`：每月决策明细
- `refine_m13_13_vw2_tv0p15_max4p5_min1p5_b0p0_crneg0p09_cd1_bond2x_pos_report.md`：单策略报告
