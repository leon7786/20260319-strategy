> ⚠️ Audit warning: 当前这条月度 NASDAQ 策略线使用了 `BOND_ANNUAL` 年度映射折算 bond-side 月收益，存在 future leak / 前视偏差。以下指标暂不可视为有效实盘或严谨回测结果，需重算。

# no.6_breakout_best

## 策略简介
Regime breakout 路线：attack / normal / defense 三态杠杆 + drawdown guard，强调回撤改善。

## 回测指标
| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| breakout_lb13_vw2_ntv0.14_atv0.2_dtv0.08_max5.0_min1.5_cr-0.09_cd1_dd-0.15_am0.2_av0.06 | $64,277,049.63 | 642670.50% | 32.80% | -57.06% | 0.81 |

## 文件说明
- `strategy_nasdaq_monthly_breakout_best.py`：该策略独立 Python 入口
- `strategy_nasdaq_monthly_breakout_runner.py`：该策略家族 runner
- `strategy_nasdaq_monthly_shared.py`：共享底层回测工具
- `*_summary.csv`：指标摘要
- `*_equity.csv`：净值曲线
- `*_decisions.csv`：月度决策明细
- `*_report.md`：单策略报告
