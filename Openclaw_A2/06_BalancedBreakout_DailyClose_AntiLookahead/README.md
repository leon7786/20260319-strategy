# S1_BalancedBreakout

> 平衡突破方案，收益/回撤都明显优于 25.47% | -49.59% 阈值。

## ✅ 反未来函数 / 反过拟合约束

- 信号使用 **t-1**，执行在 **t**（Close 近似）
- 使用固定规则，不使用未来数据
- 加入交易摩擦：`slip + month_cost`
- 提供 **OOS(2015-2025)** 检查结果

## 📈 Full Period (1995-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S1_BalancedBreakout | $35,898,857 | 30.24% | -48.78% | 0.98 |

## 🧪 OOS Segment (2015-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S1_BalancedBreakout | $119,729 | 25.35% | -48.77% | 0.87 |

## ⚙️ 参数

```python
{'ma_w': 273, 'mom_w': 40, 'mom_thr': -0.05, 'vol_w': 21, 'tv_str': 0.16, 'tv_wk': 0.14, 'min_lev': 0.1, 'max_lev': 2.8, 'blook': 84, 'bmult': 2.0, 'slip': 0.0008, 'month_cost': 0.0015, 'dd_w': 252, 'dd_thr': -0.3, 'dd_lev_cut': 0.7, 'panic_mom_w': 20, 'panic_mom_thr': 0.0}
```

## ▶️ 运行

```bash
cd Openclaw_A2/06_BalancedBreakout_DailyClose_AntiLookahead
python3 strategy.py
```
