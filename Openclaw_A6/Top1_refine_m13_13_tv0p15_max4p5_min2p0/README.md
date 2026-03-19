# Top1_refine_m13_13_tv0p15_max4p5_min2p0

## 策略简介
Top1 版本，13个月动量 + 2个月波动窗口 + target vol 15% + 最大杠杆 4.5x + 最小杠杆 2.0x，单月跌幅达到 -9% 后触发 1 个月 cooldown，空仓期仅在正债券年切换 2x bond。

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
| refine_m13_13_vw2_tv0.15_max4.5_min2.0_b0.0_cr-0.09_cd1_bond2x_pos | $78,852,151.29 | 788421.51% | 33.68% | -71.33% | 0.80 |

## 文件说明
- `strategy_nasdaq_monthly_refine_top1.py`：该策略独立 Python 入口文件
- `strategy_nasdaq_monthly_refine_runner.py`：共享回测 runner
- `refine_m13_13_vw2_tv0p15_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_summary.csv`：指标摘要
- `refine_m13_13_vw2_tv0p15_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_equity.csv`：净值曲线
- `refine_m13_13_vw2_tv0p15_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_decisions.csv`：每月决策明细
- `refine_m13_13_vw2_tv0p15_max4p5_min2p0_b0p0_crneg0p09_cd1_bond2x_pos_report.md`：单策略报告
