# Top8 策略说明

## 策略逻辑
- 分数动量窗口：LA=3.32（月）。
- 趋势过滤：trend_ma=12，use_trend_filter=False。
- 动态杠杆：rv_window=12，base_target_vol=0.178，winter_mult=1.883，summer_mult=1.302。
- 杠杆范围：0.32x ~ 3.0x。
- 空仓资产：VUSTX，risk_off_lev=2.48，risk_off_mom_window=0。
- 验证方式：Walk-forward，严格使用 t-1 决策 t，避免未来函数。

## 绩效

| 策略 | 最终价值 | 总收益 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|
| Top8 | $14,084,272 | 140742.72% | 26.43% | -73.61% | 0.74 |

## Walk-Forward 验证补充

- OOS CAGR（均值）：38.84%
- OOS 夏普（均值）：1.01
- OOS 平均最大回撤：-39.31%
- OOS 最差回撤：-71.97%
