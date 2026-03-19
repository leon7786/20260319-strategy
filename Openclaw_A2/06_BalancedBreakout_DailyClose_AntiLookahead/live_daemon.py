#!/usr/bin/env python3
"""
S1_BalancedBreakout 实盘守护进程版（Daily 多次轮询，收盘前触发下单）

核心原则：
- 无未来函数：使用 t-1 日信号，t 日执行
- 每日多次执行（轮询），仅在收盘前窗口触发下单
- 默认 dry-run，防止误下单

默认交易映射：
- 风险资产：QQQ
- 债券资产：TLT
- 信号资产：^IXIC + TLT（可配置）
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, date, time as dtime
from pathlib import Path
from typing import Dict, Optional
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import requests
import yfinance as yf


S1_PARAMS = {
    "ma_w": 273,
    "mom_w": 40,
    "mom_thr": -0.05,
    "vol_w": 21,
    "tv_str": 0.16,
    "tv_wk": 0.14,
    "min_lev": 0.1,
    "max_lev": 2.8,
    "blook": 84,
    "bmult": 2.0,
    "slip": 0.0008,
    "month_cost": 0.0015,
    "dd_w": 252,
    "dd_thr": -0.30,
    "dd_lev_cut": 0.7,
    "panic_mom_w": 20,
    "panic_mom_thr": 0.0,
}


@dataclass
class TargetState:
    as_of: pd.Timestamp
    regime: str          # risk | bond | cash
    leverage: float
    reason: str


@dataclass
class DaemonConfig:
    timezone: str = "America/New_York"
    poll_interval_sec: int = 300
    preclose_start: str = "15:50"
    preclose_end: str = "16:00"
    dry_run: bool = True

    signal_risk_symbol: str = "^IXIC"
    signal_bond_symbol: str = "TLT"

    trade_risk_symbol: str = "QQQ"
    trade_bond_symbol: str = "TLT"

    broker: str = "paper"  # paper | alpaca
    min_rebalance_ratio: float = 0.01

    state_file: str = ".s1_daemon_state.json"


class AlpacaBroker:
    def __init__(self, base_url: str, api_key: str, api_secret: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
            "Content-Type": "application/json",
        }

    def _req(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        r = requests.request(method, url, headers=self.headers, timeout=30, **kwargs)
        if r.status_code >= 400:
            raise RuntimeError(f"Alpaca API error {r.status_code}: {r.text}")
        return r.json() if r.text else {}

    def get_equity(self) -> float:
        data = self._req("GET", "/v2/account")
        return float(data.get("equity", 0.0))

    def list_positions(self) -> Dict[str, dict]:
        pos = self._req("GET", "/v2/positions")
        return {p["symbol"]: p for p in pos}

    def close_position(self, symbol: str):
        self._req("DELETE", f"/v2/positions/{symbol}")

    def submit_notional_order(self, symbol: str, side: str, notional: float):
        payload = {
            "symbol": symbol,
            "notional": f"{notional:.2f}",
            "side": side,
            "type": "market",
            "time_in_force": "day",
        }
        return self._req("POST", "/v2/orders", json=payload)


class PaperBroker:
    """仅记录动作，不下真实单。"""

    def __init__(self, init_equity: float = 100000.0):
        self.equity = init_equity
        self.positions: Dict[str, float] = {}

    def get_equity(self) -> float:
        return self.equity

    def list_positions(self) -> Dict[str, dict]:
        out = {}
        for sym, mv in self.positions.items():
            out[sym] = {"symbol": sym, "market_value": str(mv), "side": "long" if mv >= 0 else "short"}
        return out

    def close_position(self, symbol: str):
        if symbol in self.positions:
            logging.info("[PAPER] close %s", symbol)
            self.positions.pop(symbol, None)

    def submit_notional_order(self, symbol: str, side: str, notional: float):
        logging.info("[PAPER] order %s %s notional=%.2f", side, symbol, notional)
        cur = self.positions.get(symbol, 0.0)
        if side == "buy":
            self.positions[symbol] = cur + notional
        else:
            self.positions[symbol] = cur - notional
        return {"paper": True, "symbol": symbol, "side": side, "notional": notional}


def parse_hhmm(s: str) -> dtime:
    hh, mm = s.split(":")
    return dtime(hour=int(hh), minute=int(mm))


def now_in_tz(tz: str) -> datetime:
    return datetime.now(ZoneInfo(tz))


def is_weekday(d: datetime) -> bool:
    return d.weekday() < 5


def in_preclose_window(d: datetime, start: dtime, end: dtime) -> bool:
    t = d.time()
    return start <= t < end


def download_close(symbol: str, start: str = "1990-01-01") -> pd.Series:
    df = yf.download(symbol, start=start, interval="1d", auto_adjust=True, progress=False)
    if df.empty:
        raise RuntimeError(f"No data for symbol: {symbol}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df["Close"].dropna().rename(symbol)


def compute_target_state(risk_close: pd.Series, bond_close: pd.Series, params: dict) -> TargetState:
    # align
    data = pd.concat([risk_close.rename("RISK"), bond_close.rename("BOND")], axis=1).dropna()
    if len(data) < 400:
        raise RuntimeError("Not enough bars to compute strategy")

    ix = data["RISK"]
    bond = data["BOND"]

    rix = ix.pct_change().fillna(0.0)

    ma = ix.rolling(params["ma_w"]).mean()
    mom = ix / ix.shift(params["mom_w"]) - 1
    vol = rix.rolling(params["vol_w"]).std()
    rolling_high = ix.rolling(params["dd_w"]).max()

    bond_mom = bond / bond.shift(params["blook"]) - 1
    panic_mom = ix / ix.shift(params["panic_mom_w"]) - 1

    i = len(data) - 1  # 最新可用收盘（t-1）
    as_of = data.index[i]

    # season target vol (daily)
    m = as_of.month
    tv_str_daily = params["tv_str"] / np.sqrt(21)
    tv_wk_daily = params["tv_wk"] / np.sqrt(21)
    target_vol = tv_str_daily if m in (11, 12, 1, 2, 3, 4) else tv_wk_daily

    risk_on = False
    if pd.notna(ma.iloc[i]) and pd.notna(mom.iloc[i]):
        risk_on = (ix.iloc[i] > ma.iloc[i]) and (mom.iloc[i] > params["mom_thr"])

    if pd.notna(panic_mom.iloc[i]) and panic_mom.iloc[i] < params["panic_mom_thr"]:
        risk_on = False

    lev = params["min_lev"]
    if pd.notna(vol.iloc[i]) and vol.iloc[i] > 1e-12:
        lev = target_vol / vol.iloc[i]
    lev = max(params["min_lev"], min(params["max_lev"], lev))

    reason = []
    reason.append(f"close={ix.iloc[i]:.2f}, ma={ma.iloc[i]:.2f}, mom={mom.iloc[i]:.4f}")

    if pd.notna(rolling_high.iloc[i]) and rolling_high.iloc[i] > 0:
        idx_dd = ix.iloc[i] / rolling_high.iloc[i] - 1
        reason.append(f"idx_dd={idx_dd:.4f}")
        if idx_dd < params["dd_thr"]:
            lev = max(params["min_lev"], min(params["max_lev"], lev * params["dd_lev_cut"]))
            reason.append("dd_cut_applied")

    if risk_on:
        return TargetState(as_of=as_of, regime="risk", leverage=float(lev), reason="; ".join(reason))

    # risk_off branch
    bond_ok = pd.notna(bond_mom.iloc[i]) and (bond_mom.iloc[i] > 0)
    reason.append(f"bond_mom={bond_mom.iloc[i]:.4f}" if pd.notna(bond_mom.iloc[i]) else "bond_mom=nan")
    if bond_ok:
        return TargetState(as_of=as_of, regime="bond", leverage=float(params["bmult"]), reason="; ".join(reason))
    return TargetState(as_of=as_of, regime="cash", leverage=0.0, reason="; ".join(reason))


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(path: Path, state: dict):
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def rebalance_to_target(
    broker,
    cfg: DaemonConfig,
    target: TargetState,
    dry_run: bool,
):
    positions = broker.list_positions()
    equity = broker.get_equity()

    risk_symbol = cfg.trade_risk_symbol
    bond_symbol = cfg.trade_bond_symbol

    if target.regime == "risk":
        target_symbol = risk_symbol
        target_notional = equity * target.leverage
    elif target.regime == "bond":
        target_symbol = bond_symbol
        target_notional = equity * target.leverage
    else:
        target_symbol = None
        target_notional = 0.0

    # close non-target positions
    for sym in list(positions.keys()):
        if (target_symbol is None) or (sym != target_symbol):
            if dry_run:
                logging.info("[DRY_RUN] close position %s", sym)
            else:
                broker.close_position(sym)

    if target_symbol is None:
        logging.info("Target = CASH. All positions should be closed.")
        return

    positions = broker.list_positions()
    cur_pos = positions.get(target_symbol)
    cur_notional = float(cur_pos.get("market_value", 0.0)) if cur_pos else 0.0
    delta = target_notional - cur_notional

    if equity <= 0:
        raise RuntimeError("equity <= 0, abort")

    if abs(delta) / equity < cfg.min_rebalance_ratio:
        logging.info("No rebalance needed. delta/equity=%.4f", abs(delta) / equity)
        return

    side = "buy" if delta > 0 else "sell"
    notional = abs(delta)

    if dry_run:
        logging.info(
            "[DRY_RUN] rebalance %s %s notional=%.2f (target=%.2f, current=%.2f)",
            side,
            target_symbol,
            notional,
            target_notional,
            cur_notional,
        )
    else:
        broker.submit_notional_order(target_symbol, side, notional)
        logging.info(
            "Order sent: %s %s notional=%.2f (target=%.2f, current=%.2f)",
            side,
            target_symbol,
            notional,
            target_notional,
            cur_notional,
        )


def build_broker(cfg: DaemonConfig):
    if cfg.broker.lower() == "alpaca":
        key = os.getenv("ALPACA_API_KEY")
        secret = os.getenv("ALPACA_API_SECRET")
        base = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
        if not key or not secret:
            raise RuntimeError("ALPACA_API_KEY / ALPACA_API_SECRET not set")
        return AlpacaBroker(base_url=base, api_key=key, api_secret=secret)
    return PaperBroker()


def run_once(cfg: DaemonConfig, broker, dry_run: bool):
    risk_close = download_close(cfg.signal_risk_symbol)
    bond_close = download_close(cfg.signal_bond_symbol)
    target = compute_target_state(risk_close, bond_close, S1_PARAMS)

    logging.info(
        "TargetState as_of=%s regime=%s lev=%.3f reason=%s",
        target.as_of.date(),
        target.regime,
        target.leverage,
        target.reason,
    )

    rebalance_to_target(broker, cfg, target, dry_run=dry_run)
    return target


def daemon_loop(cfg: DaemonConfig, once: bool = False):
    start_t = parse_hhmm(cfg.preclose_start)
    end_t = parse_hhmm(cfg.preclose_end)

    state_path = Path(__file__).resolve().parent / cfg.state_file
    state = load_state(state_path)

    broker = build_broker(cfg)

    while True:
        now = now_in_tz(cfg.timezone)
        today = now.date().isoformat()

        try:
            if once:
                run_once(cfg, broker, dry_run=cfg.dry_run)
                return

            if is_weekday(now) and in_preclose_window(now, start_t, end_t):
                last_exec_day = state.get("last_exec_day")
                if last_exec_day != today:
                    target = run_once(cfg, broker, dry_run=cfg.dry_run)
                    state["last_exec_day"] = today
                    state["last_target"] = {
                        "as_of": str(target.as_of.date()),
                        "regime": target.regime,
                        "leverage": target.leverage,
                    }
                    save_state(state_path, state)
                else:
                    logging.info("Already executed today in pre-close window. waiting...")
            else:
                logging.info("Outside pre-close window. now=%s", now.strftime("%Y-%m-%d %H:%M:%S %Z"))

        except Exception as e:
            logging.exception("Daemon error: %s", e)

        time.sleep(cfg.poll_interval_sec)


def parse_args():
    p = argparse.ArgumentParser(description="S1 实盘守护进程（收盘前触发）")
    p.add_argument("--once", action="store_true", help="只执行一次")
    p.add_argument("--live", action="store_true", help="真实下单（默认 dry-run）")
    p.add_argument("--broker", default=os.getenv("S1_BROKER", "paper"), choices=["paper", "alpaca"])
    p.add_argument("--poll-sec", type=int, default=int(os.getenv("S1_POLL_SEC", "300")))
    p.add_argument("--preclose-start", default=os.getenv("S1_PRECLOSE_START", "15:50"))
    p.add_argument("--preclose-end", default=os.getenv("S1_PRECLOSE_END", "16:00"))
    p.add_argument("--tz", default=os.getenv("S1_TZ", "America/New_York"))
    p.add_argument("--signal-risk", default=os.getenv("S1_SIGNAL_RISK", "^IXIC"))
    p.add_argument("--signal-bond", default=os.getenv("S1_SIGNAL_BOND", "TLT"))
    p.add_argument("--trade-risk", default=os.getenv("S1_TRADE_RISK", "QQQ"))
    p.add_argument("--trade-bond", default=os.getenv("S1_TRADE_BOND", "TLT"))
    p.add_argument("--min-rebalance", type=float, default=float(os.getenv("S1_MIN_REBALANCE", "0.01")))
    return p.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    cfg = DaemonConfig(
        timezone=args.tz,
        poll_interval_sec=args.poll_sec,
        preclose_start=args.preclose_start,
        preclose_end=args.preclose_end,
        dry_run=not args.live,
        signal_risk_symbol=args.signal_risk,
        signal_bond_symbol=args.signal_bond,
        trade_risk_symbol=args.trade_risk,
        trade_bond_symbol=args.trade_bond,
        broker=args.broker,
        min_rebalance_ratio=args.min_rebalance,
    )

    logging.info(
        "Start daemon. once=%s dry_run=%s broker=%s trade=(%s/%s) signal=(%s/%s)",
        args.once,
        cfg.dry_run,
        cfg.broker,
        cfg.trade_risk_symbol,
        cfg.trade_bond_symbol,
        cfg.signal_risk_symbol,
        cfg.signal_bond_symbol,
    )

    daemon_loop(cfg, once=args.once)


if __name__ == "__main__":
    main()
