# Openclaw_A5

可用于“检测到行情后直接生成交易决策”的 Python 决策系统。

## 设计目标
- **无未来函数**：严格使用 `t-1` 决策 `t`
- **默认 dry_run**：先输出目标仓位与建议订单，不直接实盘下单
- **回测 / 决策逻辑统一**：同一套特征、信号、仓位引擎
- **便于以后接 broker API**：先做决策系统，再接自动交易执行

## 目录结构
- `src/config.py`：参数与风控配置
- `src/data_feed.py`：行情获取与对齐
- `src/features.py`：特征计算
- `src/signal_engine.py`：信号生成（含 `shift(1)`，避免未来函数）
- `src/allocation_engine.py`：目标资产与目标杠杆
- `src/risk_engine.py`：风控拦截
- `src/portfolio_state.py`：仓位状态保存
- `src/execution_engine.py`：生成 dry_run 建议订单
- `src/strategy_core.py`：统一调度策略逻辑
- `src/runner.py`：统一运行入口

## 当前默认策略思路
当前 A5 采用更偏稳健的 walk-forward 平衡版参数作为默认策略底座：
- `la = 3.23`
- `trend_ma = 9`
- `rv_window = 2`
- `base_target_vol = 0.182`
- `winter_mult = 1.251`
- `summer_mult = 1.289`
- `min_lev = 0.09`
- `max_lev = 3.0`
- `risk_off_asset = VUSTX`
- `risk_off_lev = 2.35`
- `risk_off_mom_window = 6`
- `use_trend_filter = True`

## 运行方式
```bash
cd Openclaw_A5/src
python3 runner.py
```

## 输出内容
运行后会输出：
- 当前日期对应的目标资产
- 目标杠杆
- 是否通过风控
- 建议订单（ENTER / EXIT / HOLD / NO_TRADE）
- 上一状态与下一状态

## 说明
当前版本用于：
1. **每日信号决策**
2. **dry_run 验证**
3. **为未来接实盘 API 做结构准备**

默认还**不直接下单**。
