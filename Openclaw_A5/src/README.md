# Openclaw_A5 决策系统（草案）

## 定位
A5 不是单纯回测脚本，而是后续可用于“检测到行情后直接生成交易决策”的 Python 系统。

## 当前能力
- 拉取 `^IXIC` 与 `VUSTX` 数据
- 计算策略特征
- 严格使用 `t-1` 决策 `t`，避免未来函数
- 输出目标资产 / 目标杠杆 / 建议订单
- 记录当前状态与历史信号
- 默认 `dry_run`，不自动下单

## 运行方式
```bash
cd src
python3 runner.py
```

## 后续扩展
- 接入 broker API
- 支持 paper trading
- 支持盘前 / 收盘后调度
- 支持 Telegram 通知
