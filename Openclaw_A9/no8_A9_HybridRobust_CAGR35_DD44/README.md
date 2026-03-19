# No8 · A9 HybridRobust

> 重新设计的 A9 综合评分最强版：不是单看全样本，而是在 full / OOS / walk-forward 合成分数下排名第一。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 35.65% |
| Max DD | -44.85% |
| Sharpe | 1.10 |

## 设计思路

这不是旧 QDKA 的简单换参数，而是重新组合后的 A9 新框架：

- `QDKA downside-vol sizing`
- `trend filter (EMA fast/slow)`
- `panic momentum filter`
- `drawdown soft de-leveraging`
- `bond fallback with momentum gate`
- `seasonality target-vol`
- `T+1 execution / no future leak`

## 参数

| 参数 | 值 |
|---|---:|
| `downside_window` | `18` |
| `target_down_vol_strong` | `0.35` |
| `target_down_vol_weak` | `0.325` |
| `max_lev` | `2.75` |
| `ema_fast` | `60` |
| `ema_slow` | `190` |
| `dd_window` | `84` |
| `dd_soft` | `0.14` |
| `dd_lev_cut` | `0.5` |
| `panic_window` | `20` |
| `panic_thr` | `0.0` |
| `bond_lookback` | `84` |
| `bond_lev` | `2.0` |
| `rf_annual` | `0.06` |
| `strong_months` | `[11, 12, 1, 2, 3, 4]` |

## 运行方式

```bash
cd Openclaw_A9/no8_A9_HybridRobust_CAGR35_DD44
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
