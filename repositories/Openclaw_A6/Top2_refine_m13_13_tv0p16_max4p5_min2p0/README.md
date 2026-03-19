# Top2_refine_m13_13_tv0p16_max4p5_min2p0

## 策略简介
Top2 版本，与 Top1 基本相同，但 target vol 提升到 16%，因此收益略低但仍处于最强簇。

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
| refine_m13_13_vw2_tv0.16_max4.5_min2.0_b0.0_cr-0.09_cd1_bond2x_pos | $78,573,700.56 | 785637.01% | 33.67% | -72.48% | 0.79 |

## 文件说明
- `strategy_nasdaq_monthly_refine_top2.py`：该策略独立 Python 入口文件
- `strategy_nasdaq_monthly_refine_runner.py`：共享回测 runner
- `refine_m13_13_vw2_tv0p16_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_summary.csv`：指标摘要
- `refine_m13_13_vw2_tv0p16_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_equity.csv`：净值曲线
- `refine_m13_13_vw2_tv0p16_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_decisions.csv`：每月决策明细
- `refine_m13_13_vw2_tv0p16_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_report.md`：单策略报告
