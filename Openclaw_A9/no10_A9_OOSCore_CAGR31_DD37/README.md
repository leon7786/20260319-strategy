# No10 · A9 OOSCore

> A9 的高 OOS 稳健分支：不是追最猛全样本，而是优先兼顾 2015+ / 2020+ OOS 稳定性。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 31.31% |
| Max DD | -37.01% |
| Sharpe | 1.13 |

## 设计定位

控制债券 fallback 杠杆与 drawdown 去杠杆强度，换取更好的 OOS 连续性和更轻的回撤。

## 核心模块

- QDKA downside-vol sizing
- EMA trend filter
- panic momentum filter
- drawdown soft de-leveraging
- bond fallback with momentum gate
- seasonality target-vol
- T+1 execution

## 参数

| 参数 | 值 |
|---|---:|
| `downside_window` | `18` |
| `target_down_vol_strong` | `0.325` |
| `target_down_vol_weak` | `0.325` |
| `max_lev` | `2.5` |
| `ema_fast` | `60` |
| `ema_slow` | `190` |
| `dd_window` | `84` |
| `dd_soft` | `0.14` |
| `dd_lev_cut` | `0.35` |
| `panic_window` | `20` |
| `panic_thr` | `0.0` |
| `bond_lookback` | `84` |
| `bond_lev` | `0.5` |
| `rf_annual` | `0.06` |
| `strong_months` | `[11, 12, 1, 2, 3, 4]` |

## 运行方式

```bash
cd Openclaw_A9/no10_A9_OOSCore_CAGR31_DD37
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
