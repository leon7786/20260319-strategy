# No3 · QDKA LowDD

> 把回撤进一步往下压的版本，适合更看重防守的人。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 29.95% |
| Max DD | -40.13% |
| Sharpe | 0.95 |

## 策略说明

- 标的：`^IXIC`
- 频率：日频
- 区间：`1995-01-03 ~ 2025-12-29`
- 执行：**T 日收盘生成信号，T+1 执行**
- 无未来函数：全部基于历史滚动计算

## 参数

| 参数 | 值 |
|---|---:|
| `downside_window` | `14` |
| `target_down_vol` | `0.325` |
| `max_lev` | `2.5` |
| `ema_fast` | `50` |
| `ema_slow` | `190` |
| `dd_window` | `84` |
| `dd_cut` | `0.14` |
| `rf_annual` | `0.06` |

## 运行方式

```bash
cd Openclaw_A9/no3_QDKA_LowDD_CAGR29_DD40
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
