# S2_LowDDMomentum

> 低回撤动量方案，回撤控制最强，适合偏稳健。

## ✅ 反未来函数 / 反过拟合约束

- 信号使用 **t-1**，执行在 **t**（Close 近似）
- 使用固定规则，不使用未来数据
- 加入交易摩擦：`slip + month_cost`
- 提供 **OOS(2015-2025)** 检查结果

## 📈 Full Period (1995-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S2_LowDDMomentum | $26,663,412 | 28.99% | -43.72% | 0.97 |

## 🧪 OOS Segment (2015-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S2_LowDDMomentum | $75,416 | 20.18% | -43.72% | 0.75 |

## ⚙️ 参数

```python
{'ma_w': 252, 'mom_w': 189, 'mom_thr': -0.02, 'vol_w': 63, 'tv_str': 0.16, 'tv_wk': 0.14, 'min_lev': 0.2, 'max_lev': 2.8, 'blook': 84, 'bmult': 2.0, 'slip': 0.0005, 'month_cost': 0.0012, 'dd_w': 63, 'dd_thr': -0.1, 'dd_lev_cut': 0.8, 'panic_mom_w': 20, 'panic_mom_thr': 0.0}
```

## ▶️ 运行

```bash
cd Openclaw_A2/07_LowDDMomentum_DailyClose_AntiLookahead
python3 strategy.py
```
