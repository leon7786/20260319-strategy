# S1_BalancedBreakout

> 平衡突破方案，收益/回撤都明显优于 25.47% | -49.59% 阈值。  
> 已提供 **可实盘守护进程版**（每日多次执行，收盘前触发自动下单）。

## ✅ 反未来函数 / 反过拟合约束

- 信号使用 **t-1**，执行在 **t**（Close 近似）
- 固定规则，不使用未来数据
- 加入交易摩擦：`slip + month_cost`
- 提供 OOS（2015-2025）检查

## 📈 Full Period (1995-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S1_BalancedBreakout | $35,898,857 | 30.24% | -48.78% | 0.98 |

## 🧪 OOS Segment (2015-2025)

| 策略 | 最终价值 | 年化CAGR | 最大回撤 | 夏普 |
|---|---:|---:|---:|---:|
| S1_BalancedBreakout | $108,801 | 24.26% | -48.77% | 0.82 |

---

## ⚙️ 参数

```python
{
  'ma_w': 273, 'mom_w': 40, 'mom_thr': -0.05,
  'vol_w': 21, 'tv_str': 0.16, 'tv_wk': 0.14,
  'min_lev': 0.1, 'max_lev': 2.8,
  'blook': 84, 'bmult': 2.0,
  'slip': 0.0008, 'month_cost': 0.0015,
  'dd_w': 252, 'dd_thr': -0.3, 'dd_lev_cut': 0.7,
  'panic_mom_w': 20, 'panic_mom_thr': 0.0,
}
```

## ▶️ 回测运行

```bash
cd Openclaw_A2/06_BalancedBreakout_DailyClose_AntiLookahead
python3 strategy.py
```

## 🛡️ 实盘守护进程（Daily 多次执行，收盘前触发）

文件：`live_daemon.py`

### 1) Dry-run（强烈建议先跑）

```bash
cd /root/projects/20260319-strategy
python3 Openclaw_A2/06_BalancedBreakout_DailyClose_AntiLookahead/live_daemon.py --once --broker paper
```

### 2) 常驻轮询（paper）

```bash
python3 Openclaw_A2/06_BalancedBreakout_DailyClose_AntiLookahead/live_daemon.py \
  --broker paper \
  --poll-sec 120 \
  --preclose-start 15:50 \
  --preclose-end 16:00 \
  --tz America/New_York
```

### 3) Live 下单（Alpaca）

先配置环境变量：

```bash
export ALPACA_API_KEY='xxx'
export ALPACA_API_SECRET='xxx'
export ALPACA_BASE_URL='https://paper-api.alpaca.markets'   # 先用 paper
```

然后执行：

```bash
python3 Openclaw_A2/06_BalancedBreakout_DailyClose_AntiLookahead/live_daemon.py \
  --broker alpaca \
  --live \
  --poll-sec 120
```

### 4) systemd 托管

参考：`systemd_s1.service.example`

```bash
sudo cp Openclaw_A2/06_BalancedBreakout_DailyClose_AntiLookahead/systemd_s1.service.example /etc/systemd/system/s1-daemon.service
sudo systemctl daemon-reload
sudo systemctl enable --now s1-daemon.service
sudo systemctl status s1-daemon.service
```

---

## 交易逻辑说明

- **每次轮询都计算最新状态**
- 仅在收盘前窗口（默认 15:50~16:00 ET）执行一次当天再平衡
- 当天已经执行过则不重复下单
- `min_rebalance_ratio` 控制最小调仓阈值，避免过度交易

## 风险提示

- 默认 `dry_run=True`（除非显式传 `--live`）
- 任何实盘前请先在 paper 环境跑至少 2 周
- 若 broker 不支持 notional/MOC，请根据券商 API 做适配
