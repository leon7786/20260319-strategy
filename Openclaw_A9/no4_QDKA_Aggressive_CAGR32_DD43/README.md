# No4 · QDKA Aggressive

> 更激进的收益冲刺版，CAGR 更高，但回撤比平衡版略差。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 32.27% |
| Max DD | -43.82% |
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
| `downside_window` | `16` |
| `target_down_vol` | `0.35` |
| `max_lev` | `2.75` |
| `ema_fast` | `50` |
| `ema_slow` | `190` |
| `dd_window` | `84` |
| `dd_cut` | `0.14` |
| `rf_annual` | `0.06` |

## 运行方式

```bash
cd Openclaw_A9/no4_QDKA_Aggressive_CAGR32_DD43
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
