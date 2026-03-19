# Top9 策略说明

## 策略逻辑
- 分数动量窗口：LA=3.23（月）。
- 趋势过滤：trend_ma=9，use_trend_filter=True。
- 动态杠杆：rv_window=2，base_target_vol=0.182，winter_mult=1.251，summer_mult=1.289。
- 杠杆范围：0.09x ~ 3.0x。
- 空仓资产：VUSTX，risk_off_lev=2.35，risk_off_mom_window=6。
- 验证方式：Walk-forward，严格使用 t-1 决策 t，优先降低样本外过拟合风险。

## 绩效

| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| Top9 | $11,833,859 | 118238.59% | 25.72% | -61.79% | 0.76 |

## Walk-Forward 验证补充

- OOS CAGR（均值）：37.55%
- OOS 夏普（均值）：1.02
- OOS 平均最大回撤：-31.44%
- OOS 最差回撤：-44.10%
