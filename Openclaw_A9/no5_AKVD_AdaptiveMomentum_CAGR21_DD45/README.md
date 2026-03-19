# No5 · AKVD AdaptiveMomentum

> 较早跑出来的强策略之一，收益与回撤都明显优于买入持有。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 21.93% |
| Max DD | -45.80% |
| Sharpe | 0.78 |

## 策略说明

- 标的：`^IXIC`
- 频率：日频
- 区间：`1995-01-03 ~ 2025-12-29`
- 执行：**T 日收盘生成信号，T+1 执行**
- 无未来函数：全部基于历史滚动计算

## 参数

| 参数 | 值 |
|---|---:|
| `ema_fast` | `50` |
| `ema_slow` | `200` |
| `mom_63_w` | `0.2` |
| `mom_126_w` | `0.3` |
| `mom_252_w` | `0.5` |
| `target_vol` | `0.4` |
| `max_leverage` | `3.0` |
| `vol_window` | `20` |

## 运行方式

```bash
cd Openclaw_A9/no5_AKVD_AdaptiveMomentum_CAGR21_DD45
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
