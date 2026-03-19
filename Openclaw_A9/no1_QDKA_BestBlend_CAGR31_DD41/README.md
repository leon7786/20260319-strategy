# No1 · QDKA BestBlend

> 当前最推荐的 QDKA 优化版：同时把 CAGR 推到 31% 左右，同时把 MaxDD 压到 -41% 左右。

## 参考表现

| 指标 | 数值 |
|---|---:|
| CAGR | 31.01% |
| Max DD | -41.41% |
| Sharpe | 0.94 |

## 策略说明

- 标的：`^IXIC`
- 频率：日频
- 区间：`1995-01-03 ~ 2025-12-29`
- 执行：**T 日收盘生成信号，T+1 执行**
- 无未来函数：全部基于历史滚动计算

## 参数

| 参数 | 值 |
|---|---:|
| `downside_window` | `12` |
| `target_down_vol` | `0.325` |
| `max_lev` | `2.75` |
| `ema_fast` | `60` |
| `ema_slow` | `190` |
| `dd_window` | `84` |
| `dd_cut` | `0.12` |
| `rf_annual` | `0.06` |

## 运行方式

```bash
cd Openclaw_A9/no1_QDKA_BestBlend_CAGR31_DD41
python3 strategy.py
```

运行后会在当前目录下生成：

```text
results/
├── equity_curve.csv
├── strategy_vs_buyhold.png
└── summary.json
```
