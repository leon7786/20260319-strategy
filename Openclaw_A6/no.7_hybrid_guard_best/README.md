> ⚠️ Audit warning: 当前这条月度 NASDAQ 策略线使用了 `BOND_ANNUAL` 年度映射折算 bond-side 月收益，存在 future leak / 前视偏差。以下指标暂不可视为有效实盘或严谨回测结果，需重算。

# no.7_hybrid_guard_best

## 策略简介
Hybrid guard 路线：高收益底层 + defensive overlay + recovery hysteresis，主打更低回撤。

## 回测指标
| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| hybrid_dd-0.18_rec-0.04_dtv0.08_dmax2.5_dmin1.0_ax0.02_am0.15_av0.06 | $18,141,395.82 | 181313.96% | 27.47% | -51.15% | 0.78 |

## 文件说明
- `strategy_nasdaq_monthly_hybrid_guard_best.py`：该策略独立 Python 入口
- `strategy_nasdaq_monthly_hybrid_guard_runner.py`：该策略家族 runner
- `strategy_nasdaq_monthly_shared.py`：共享底层回测工具
- `*_summary.csv`：指标摘要
- `*_equity.csv`：净值曲线
- `*_decisions.csv`：月度决策明细
- `*_report.md`：单策略报告
