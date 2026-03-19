# No2 · QDKA SharpeMax

> 更强调 Sharpe 的平衡版本，整体风险调整后表现很强。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 30.55% |
| Max DD | -41.65% |
| Sharpe | 0.96 |

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
| `target_down_vol` | `0.35` |
| `max_lev` | `2.5` |
| `ema_fast` | `50` |
| `ema_slow` | `190` |
| `dd_window` | `84` |
| `dd_cut` | `0.12` |
| `rf_annual` | `0.06` |

## 运行方式

```bash
cd Openclaw_A9/no2_QDKA_SharpeMax_CAGR30_DD41
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
