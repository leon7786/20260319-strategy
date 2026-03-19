# no.9_refine_3720_best

## 策略简介
Attack overlay refine 路线：更早 attack + 更高 attack target vol 的局部精修版本。

## 回测指标
| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| refine_attack_lb13_vw2_btv0.15_atv0.26_amax4.5_min2.0_cr-0.09_cd1_am0.12_av0.07 | $175,996,294.23 | 1759862.94% | 37.20% | -71.11% | 0.83 |

## 文件说明
- `strategy_nasdaq_monthly_refine_3720_best.py`：该策略独立 Python 入口
- `strategy_nasdaq_monthly_attack_family_runner.py`：该策略家族 runner
- `strategy_nasdaq_monthly_shared.py`：共享底层回测工具
- `*_summary.csv`：指标摘要
- `*_equity.csv`：净值曲线
- `*_decisions.csv`：月度决策明细
- `*_report.md`：单策略报告
