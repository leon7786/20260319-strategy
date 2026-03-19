# no.8_attack_3629_best

## 策略简介
Attack overlay 首次破顶路线：强势 + 低波动 + 上月为正时进入更激进 target vol。

## 回测指标
| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| attack_lb13_vw2_btv0.15_atv0.24_amax4.5_min2.0_cr-0.09_cd1_am0.15_av0.07_..1 | $143,345,703.91 | 1433357.04% | 36.29% | -71.11% | 0.82 |

## 文件说明
- `strategy_nasdaq_monthly_attack_3629_best.py`：该策略独立 Python 入口
- `strategy_nasdaq_monthly_attack_family_runner.py`：该策略家族 runner
- `strategy_nasdaq_monthly_shared.py`：共享底层回测工具
- `*_summary.csv`：指标摘要
- `*_equity.csv`：净值曲线
- `*_decisions.csv`：月度决策明细
- `*_report.md`：单策略报告
