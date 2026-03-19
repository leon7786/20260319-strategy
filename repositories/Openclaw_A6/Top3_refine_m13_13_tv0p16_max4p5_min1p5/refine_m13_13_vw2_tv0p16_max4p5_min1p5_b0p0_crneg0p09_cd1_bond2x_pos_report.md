# refine_m13_13_vw2_tv0.16_max4.5_min1.5_b0.0_cr-0.09_cd1_bond2x_pos

- 回测区间: 1995-01-31 ~ 2025-12-29
- 初始资金: $10,000.00
- 数据: 本地 IXIC 日线聚合为月末收盘
- 执行: 月末信号，次月收益生效
- 出场侧: 正债券年使用 2x bond，否则 cash

## 绩效
| 策略 | 最终价值 | 总收益 | 年化CAGR | 年化波动 | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|---:|---:|
| refine_m13_13_vw2_tv0.16_max4.5_min1.5_b0.0_cr-0.09_cd1_bond2x_pos | $75,393,635.27 | 753836.35% | 33.49% | 57.68% | -72.49% | 0.79 |

## 参数
- mom_fast: 13
- mom_slow: 13
- vol_window: 2
- target_vol: 0.16
- max_lev: 4.5
- min_lev: 1.5
- bonus: 0.0
- crash_filter: -0.09
- crash_cooldown: 1

## 输出文件
- refine_m13_13_vw2_tv0p16_max4p5_min1p5_b0p0_crneg0p09_cd1_bond2x_pos_summary.csv
- refine_m13_13_vw2_tv0p16_max4p5_min1p5_b0p0_crneg0p09_cd1_bond2x_pos_equity.csv
- refine_m13_13_vw2_tv0p16_max4p5_min1p5_b0p0_crneg0p09_cd1_bond2x_pos_decisions.csv