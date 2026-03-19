# Openclaw_A5 架构说明

## 目标
A5 是一个“交易决策系统”，不是单纯的回测脚本。
同一套策略逻辑同时支持：
- 回测模式
- 每日信号模式
- dry_run 执行建议模式

## 核心原则
1. 无未来函数：严格使用 t-1 决策 t
2. 默认 dry_run：先输出目标仓位与建议订单，不直接下单
3. 回测 / 实盘逻辑统一：共用同一套特征、信号、仓位引擎
4. 可扩展：未来可接 broker API

## 模块
- config.py：全局配置
- data_feed.py：行情获取与对齐
- features.py：特征计算
- signal_engine.py：信号生成
- allocation_engine.py：目标仓位与杠杆
- risk_engine.py：风控拦截
- portfolio_state.py：状态持久化
- execution_engine.py：dry_run 订单建议
- strategy_core.py：统一编排策略逻辑
- runner.py：统一入口
