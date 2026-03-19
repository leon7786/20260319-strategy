# No9 · A9 Defensive

> A9 的防守分支：明显压低回撤，牺牲部分收益，适合更重视净值稳定与持有舒适度的版本。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 18.01% |
| Max DD | -25.21% |
| Sharpe | 1.02 |

## 设计定位

更长 downside 窗口 + 更低弱市 target-vol + 更低 bond leverage + 更严格 panic 过滤，目标是把 MaxDD 压到 25% 左右。

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
| `downside_window` | `24` |
| `target_down_vol_strong` | `0.35` |
| `target_down_vol_weak` | `0.25` |
| `max_lev` | `2.0` |
| `ema_fast` | `60` |
| `ema_slow` | `190` |
| `dd_window` | `84` |
| `dd_soft` | `0.12` |
| `dd_lev_cut` | `0.35` |
| `panic_window` | `20` |
| `panic_thr` | `0.03` |
| `bond_lookback` | `84` |
| `bond_lev` | `0.5` |
| `rf_annual` | `0.06` |
| `strong_months` | `[11, 12, 1, 2, 3, 4]` |

## 运行方式

```bash
cd Openclaw_A9/no9_A9_Defensive_CAGR18_DD25
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
