# no.10_duration_3755_best

## 策略简介
当前最新冠军：进一步提升 attack target vol 到 0.28，并验证 hold duration 不是核心增益点。

## 回测指标
| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| duration_lb13_btv0.15_atv0.28_amax4.5_min2.0_cr-0.09_am0.14_av0.07_hold0_full | $190,505,015.40 | 1904950.15% | 37.55% | -71.11% | 0.83 |

## 文件说明
- `strategy_nasdaq_monthly_duration_3755_best.py`：该策略独立 Python 入口
- `strategy_nasdaq_monthly_attack_family_runner.py`：该策略家族 runner
- `strategy_nasdaq_monthly_shared.py`：共享底层回测工具
- `*_summary.csv`：指标摘要
- `*_equity.csv`：净值曲线
- `*_decisions.csv`：月度决策明细
- `*_report.md`：单策略报告
