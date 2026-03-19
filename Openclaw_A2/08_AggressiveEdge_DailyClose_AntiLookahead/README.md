# S3_AggressiveEdge

> 高进攻边际版本，收益最高，但全周期DD略高于阈值。

## ✅ 反未来函数 / 反过拟合约束

- 信号使用 **t-1**，执行在 **t**（Close 近似）
- 使用固定规则，不使用未来数据
- 加入交易摩擦：`slip + month_cost`
- 提供 **OOS(2015-2025)** 检查结果

## 📈 Full Period (1995-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S3_AggressiveEdge | $38,939,358 | 30.58% | -49.67% | 0.93 |

## 🧪 OOS Segment (2015-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S3_AggressiveEdge | $117,461 | 25.13% | -39.19% | 0.83 |

## ⚙️ 参数

```python
{'ma_w': 231, 'mom_w': 20, 'mom_thr': 0.0, 'vol_w': 42, 'tv_str': 0.24, 'tv_wk': 0.16, 'min_lev': 0.2, 'max_lev': 3.0, 'blook': 84, 'bmult': 2.0, 'slip': 0.001, 'month_cost': 0.0018, 'dd_w': 252, 'dd_thr': -0.15, 'dd_lev_cut': 0.6, 'panic_mom_w': 20, 'panic_mom_thr': -0.1}
```

## ▶️ 运行

```bash
cd Openclaw_A2/08_AggressiveEdge_DailyClose_AntiLookahead
python3 strategy.py
```
