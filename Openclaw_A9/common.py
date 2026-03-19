from pathlib import Path
import json

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / '_cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_PATH = CACHE_DIR / 'ixic_daily.csv'
START = '1995-01-03'
END = '2025-12-29'


def load_ixic_data():
    if CACHE_PATH.exists():
        df = pd.read_csv(CACHE_PATH, index_col=0, parse_dates=True)
        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df, 'local_cache'

    df = yf.download('^IXIC', start=START, end=END, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.title)
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CACHE_PATH)
    return df, 'download'


def get_stats(returns, navs, years):
    cagr = (navs.iloc[-1] ** (1 / years)) - 1
    max_dd = ((navs - navs.cummax()) / navs.cummax()).min()
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    return float(cagr), float(max_dd), float(sharpe)


def print_report(title, summary):
    strat = summary['strategy']
    bnh = summary['buy_hold']
    print(f'\n{title}')
    print('-' * 68)
    print(f"{'指标':<18} | {'策略':<16} | {'买入持有 (IXIC)'}")
    print('-' * 68)
    print(f"{'年化收益 (CAGR)':<16} | {strat['cagr']*100:>13.2f}% | {bnh['cagr']*100:>10.2f}%")
    print(f"{'最大回撤 (Max DD)':<16} | {strat['max_drawdown']*100:>13.2f}% | {bnh['max_drawdown']*100:>10.2f}%")
    print(f"{'夏普比率 (Sharpe)':<16} | {strat['sharpe']:>13.2f} | {bnh['sharpe']:>10.2f}")
    print('-' * 68)
    print(f"数据来源: {summary['data_source']}")
    print(f"结果目录: {summary['files']['summary_json']}")


def run_qdka_backtest(strategy_name, params, strategy_dir):
    strategy_dir = Path(strategy_dir)
    outdir = strategy_dir / 'results'
    outdir.mkdir(parents=True, exist_ok=True)

    df, data_source = load_ixic_data()
    df = df.loc[(df.index >= pd.Timestamp(START)) & (df.index <= pd.Timestamp(END))].copy()
    df['Ret'] = df['Close'].pct_change()

    df['Negative_Ret'] = np.minimum(df['Ret'], 0)
    df['Downside_Vol'] = df['Negative_Ret'].rolling(window=params['downside_window']).std() * np.sqrt(252)
    df['Target_Leverage'] = (params['target_down_vol'] / df['Downside_Vol']).clip(lower=0, upper=params['max_lev'])

    fast_col = f"EMA{params['ema_fast']}"
    slow_col = f"EMA{params['ema_slow']}"
    df[fast_col] = df['Close'].ewm(span=params['ema_fast'], adjust=False).mean()
    df[slow_col] = df['Close'].ewm(span=params['ema_slow'], adjust=False).mean()
    trend_filter = (df['Close'] > df[slow_col]) & (df[fast_col] > df[slow_col])

    max_col = f"Rolling_Max_{params['dd_window']}"
    df[max_col] = df['Close'].rolling(window=params['dd_window']).max()
    df['Drawdown_From_Peak'] = (df['Close'] - df[max_col]) / df[max_col]
    circuit_breaker = df['Drawdown_From_Peak'] > -params['dd_cut']

    df['Leverage_T'] = np.where(trend_filter & circuit_breaker, df['Target_Leverage'], 0)
    df['Actual_Leverage'] = df['Leverage_T'].shift(1).fillna(0)

    daily_rf = params['rf_annual'] / 252
    df['Cash_Ratio'] = np.maximum(0, 1 - df['Actual_Leverage'])
    df['Strategy_Ret'] = (df['Actual_Leverage'] * df['Ret']) + (df['Cash_Ratio'] * daily_rf)
    df['BnH_Ret'] = df['Ret']

    df['Strategy_NAV'] = (1 + df['Strategy_Ret']).cumprod()
    df['BnH_NAV'] = (1 + df['BnH_Ret']).cumprod()
    df = df.dropna(subset=['Strategy_NAV', 'BnH_NAV']).copy()

    years = (df.index[-1] - df.index[0]).days / 365.25
    cagr_s, mdd_s, sharpe_s = get_stats(df['Strategy_Ret'], df['Strategy_NAV'], years)
    cagr_b, mdd_b, sharpe_b = get_stats(df['BnH_Ret'], df['BnH_NAV'], years)

    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Strategy_NAV'], label=f"{strategy_name} (CAGR: {cagr_s*100:.1f}%)", color='#ff0055', linewidth=1.6)
    plt.plot(df.index, df['BnH_NAV'], label=f"Buy & Hold IXIC (CAGR: {cagr_b*100:.1f}%)", color='#888888', alpha=0.6)
    plt.yscale('log')
    plt.title(f'{strategy_name} vs Buy & Hold (Log Scale)')
    plt.ylabel('Cumulative NAV (Log)')
    plt.legend()
    plt.grid(True, which='both', ls=':', alpha=0.4)
    plot_path = outdir / 'strategy_vs_buyhold.png'
    plt.savefig(plot_path, dpi=160, bbox_inches='tight')
    plt.close()

    equity_path = outdir / 'equity_curve.csv'
    df[['Close', 'Actual_Leverage', 'Cash_Ratio', 'Strategy_Ret', 'BnH_Ret', 'Strategy_NAV', 'BnH_NAV']].to_csv(equity_path)

    summary = {
        'strategy_name': strategy_name,
        'data_source': data_source,
        'start': str(df.index[0].date()),
        'end': str(df.index[-1].date()),
        'bars': int(len(df)),
        'params': params,
        'strategy': {
            'cagr': cagr_s,
            'max_drawdown': mdd_s,
            'sharpe': sharpe_s,
            'final_nav': float(df['Strategy_NAV'].iloc[-1]),
        },
        'buy_hold': {
            'cagr': cagr_b,
            'max_drawdown': mdd_b,
            'sharpe': sharpe_b,
            'final_nav': float(df['BnH_NAV'].iloc[-1]),
        },
        'files': {
            'equity_curve_csv': str(equity_path),
            'plot_png': str(plot_path),
            'summary_json': str(outdir / 'summary.json'),
        },
    }
    (outdir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def run_akvd_backtest(strategy_name, strategy_dir, params=None):
    strategy_dir = Path(strategy_dir)
    outdir = strategy_dir / 'results'
    outdir.mkdir(parents=True, exist_ok=True)

    if params is None:
        params = {
            'ema_fast': 50,
            'ema_slow': 200,
            'mom_63_w': 0.2,
            'mom_126_w': 0.3,
            'mom_252_w': 0.5,
            'target_vol': 0.40,
            'max_leverage': 3.0,
            'vol_window': 20,
        }

    df, data_source = load_ixic_data()
    df = df.loc[(df.index >= pd.Timestamp(START)) & (df.index <= pd.Timestamp(END))].copy()
    df['Daily_Return'] = df['Close'].pct_change()

    df[f"EMA{params['ema_fast']}"] = df['Close'].ewm(span=params['ema_fast'], adjust=False).mean()
    df[f"EMA{params['ema_slow']}"] = df['Close'].ewm(span=params['ema_slow'], adjust=False).mean()
    df['Bull_Regime'] = np.where(
        (df['Close'] > df[f"EMA{params['ema_slow']}"]) & (df[f"EMA{params['ema_fast']}"] > df[f"EMA{params['ema_slow']}"]),
        1,
        0,
    )

    df['Mom_63'] = df['Close'].pct_change(63)
    df['Mom_126'] = df['Close'].pct_change(126)
    df['Mom_252'] = df['Close'].pct_change(252)
    df['Mom_Score'] = (
        df['Mom_63'] * params['mom_63_w']
        + df['Mom_126'] * params['mom_126_w']
        + df['Mom_252'] * params['mom_252_w']
    )
    df['Mom_Filter'] = np.where(df['Mom_Score'] > 0, 1, 0)

    df['Realized_Vol'] = df['Daily_Return'].rolling(window=params['vol_window']).std() * np.sqrt(252)
    df['Target_Leverage'] = (params['target_vol'] / df['Realized_Vol']).clip(lower=0, upper=params['max_leverage'])

    df['Target_Position_T'] = df['Bull_Regime'] * df['Mom_Filter'] * df['Target_Leverage']
    df['Actual_Position'] = df['Target_Position_T'].shift(1).fillna(0)

    df['Strategy_Return'] = df['Actual_Position'] * df['Daily_Return']
    df['BnH_Return'] = df['Daily_Return']
    df['Strategy_NetValue'] = (1 + df['Strategy_Return']).cumprod()
    df['BnH_NetValue'] = (1 + df['BnH_Return']).cumprod()
    df = df.dropna(subset=['Strategy_NetValue', 'BnH_NetValue']).copy()

    years = (df.index[-1] - df.index[0]).days / 365.25
    cagr_s, mdd_s, sharpe_s = get_stats(df['Strategy_Return'], df['Strategy_NetValue'], years)
    cagr_b, mdd_b, sharpe_b = get_stats(df['BnH_Return'], df['BnH_NetValue'], years)

    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Strategy_NetValue'], label=f"{strategy_name} (CAGR: {cagr_s*100:.1f}%)", color='#0066ff', linewidth=1.6)
    plt.plot(df.index, df['BnH_NetValue'], label=f"Buy & Hold IXIC (CAGR: {cagr_b*100:.1f}%)", color='#888888', alpha=0.6)
    plt.yscale('log')
    plt.title(f'{strategy_name} vs Buy & Hold (Log Scale)')
    plt.ylabel('Cumulative NAV (Log)')
    plt.legend()
    plt.grid(True, which='both', ls=':', alpha=0.4)
    plot_path = outdir / 'strategy_vs_buyhold.png'
    plt.savefig(plot_path, dpi=160, bbox_inches='tight')
    plt.close()

    equity_path = outdir / 'equity_curve.csv'
    df[['Close', 'Actual_Position', 'Strategy_Return', 'BnH_Return', 'Strategy_NetValue', 'BnH_NetValue']].to_csv(equity_path)

    summary = {
        'strategy_name': strategy_name,
        'data_source': data_source,
        'start': str(df.index[0].date()),
        'end': str(df.index[-1].date()),
        'bars': int(len(df)),
        'params': params,
        'strategy': {
            'cagr': cagr_s,
            'max_drawdown': mdd_s,
            'sharpe': sharpe_s,
            'final_nav': float(df['Strategy_NetValue'].iloc[-1]),
        },
        'buy_hold': {
            'cagr': cagr_b,
            'max_drawdown': mdd_b,
            'sharpe': sharpe_b,
            'final_nav': float(df['BnH_NetValue'].iloc[-1]),
        },
        'files': {
            'equity_curve_csv': str(equity_path),
            'plot_png': str(plot_path),
            'summary_json': str(outdir / 'summary.json'),
        },
    }
    (outdir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def load_bond_data():
    repo_cache = ROOT.parent / 'data' / 'VUSTX_daily_yf.csv'
    if repo_cache.exists():
        df = pd.read_csv(repo_cache, parse_dates=['Date']).set_index('Date').sort_index()
        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df['Close'].rename('BOND'), 'repo_cache'

    raw = yf.download('VUSTX', start=START, end=END, auto_adjust=False, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    s = raw['Close'].copy().squeeze()
    s.index = pd.to_datetime(s.index).tz_localize(None)
    return s.rename('BOND'), 'download'


def run_a9_hybrid_backtest(strategy_name, params, strategy_dir):
    strategy_dir = Path(strategy_dir)
    outdir = strategy_dir / 'results'
    outdir.mkdir(parents=True, exist_ok=True)

    ixic_df, ixic_source = load_ixic_data()
    bond_close, bond_source = load_bond_data()

    df = pd.concat([
        ixic_df.loc[(ixic_df.index >= pd.Timestamp(START)) & (ixic_df.index <= pd.Timestamp(END)), 'Close'].rename('IXIC'),
        bond_close.rename('BOND')
    ], axis=1).dropna().copy()

    df['Ret_IXIC'] = df['IXIC'].pct_change()
    df['Ret_BOND'] = df['BOND'].pct_change()
    df['Negative_Ret'] = np.minimum(df['Ret_IXIC'], 0)
    df['Downside_Vol'] = df['Negative_Ret'].rolling(window=params['downside_window']).std() * np.sqrt(252)

    strong_months = df.index.month.isin(params.get('strong_months', [11, 12, 1, 2, 3, 4]))
    df['Target_Down_Vol'] = np.where(strong_months, params['target_down_vol_strong'], params['target_down_vol_weak'])
    df['Base_Leverage'] = (df['Target_Down_Vol'] / df['Downside_Vol']).clip(lower=0, upper=params['max_lev'])

    df[f"EMA{params['ema_fast']}"] = df['IXIC'].ewm(span=params['ema_fast'], adjust=False).mean()
    df[f"EMA{params['ema_slow']}"] = df['IXIC'].ewm(span=params['ema_slow'], adjust=False).mean()
    trend_filter = (df['IXIC'] > df[f"EMA{params['ema_slow']}"]) & (df[f"EMA{params['ema_fast']}"] > df[f"EMA{params['ema_slow']}"])

    df[f"Rolling_Max_{params['dd_window']}"] = df['IXIC'].rolling(window=params['dd_window']).max()
    df['Drawdown_From_Peak'] = (df['IXIC'] - df[f"Rolling_Max_{params['dd_window']}"]) / df[f"Rolling_Max_{params['dd_window']}"]
    lev_multiplier = np.where(df['Drawdown_From_Peak'] <= -params['dd_soft'], params['dd_lev_cut'], 1.0)

    df[f"Panic_Mom_{params['panic_window']}"] = df['IXIC'].pct_change(params['panic_window'])
    panic_filter = df[f"Panic_Mom_{params['panic_window']}"] > params['panic_thr']
    risk_on = trend_filter & panic_filter

    df['Target_Lev_IXIC'] = np.where(risk_on, df['Base_Leverage'] * lev_multiplier, 0.0)

    df[f"Bond_Mom_{params['bond_lookback']}"] = df['BOND'].pct_change(params['bond_lookback'])
    bond_on = (~risk_on) & (df[f"Bond_Mom_{params['bond_lookback']}"] > 0)
    df['Target_Lev_BOND'] = np.where(bond_on, params['bond_lev'], 0.0)

    df['Actual_Lev_IXIC'] = df['Target_Lev_IXIC'].shift(1).fillna(0)
    df['Actual_Lev_BOND'] = df['Target_Lev_BOND'].shift(1).fillna(0)
    df['Cash_Ratio'] = np.maximum(0, 1 - (df['Actual_Lev_IXIC'] + df['Actual_Lev_BOND']))

    daily_rf = params['rf_annual'] / 252
    df['Strategy_Ret'] = (
        df['Actual_Lev_IXIC'] * df['Ret_IXIC']
        + df['Actual_Lev_BOND'] * df['Ret_BOND']
        + df['Cash_Ratio'] * daily_rf
    )
    df['BnH_Ret'] = df['Ret_IXIC']
    df['Strategy_NAV'] = (1 + df['Strategy_Ret']).cumprod()
    df['BnH_NAV'] = (1 + df['BnH_Ret']).cumprod()
    df = df.dropna(subset=['Strategy_NAV', 'BnH_NAV']).copy()

    years = (df.index[-1] - df.index[0]).days / 365.25
    cagr_s, mdd_s, sharpe_s = get_stats(df['Strategy_Ret'], df['Strategy_NAV'], years)
    cagr_b, mdd_b, sharpe_b = get_stats(df['BnH_Ret'], df['BnH_NAV'], years)

    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Strategy_NAV'], label=f"{strategy_name} (CAGR: {cagr_s*100:.1f}%)", color='#13aa52', linewidth=1.6)
    plt.plot(df.index, df['BnH_NAV'], label=f"Buy & Hold IXIC (CAGR: {cagr_b*100:.1f}%)", color='#888888', alpha=0.6)
    plt.yscale('log')
    plt.title(f'{strategy_name} vs Buy & Hold (Log Scale)')
    plt.ylabel('Cumulative NAV (Log)')
    plt.legend()
    plt.grid(True, which='both', ls=':', alpha=0.4)
    plot_path = outdir / 'strategy_vs_buyhold.png'
    plt.savefig(plot_path, dpi=160, bbox_inches='tight')
    plt.close()

    equity_path = outdir / 'equity_curve.csv'
    df[['IXIC', 'BOND', 'Actual_Lev_IXIC', 'Actual_Lev_BOND', 'Cash_Ratio', 'Strategy_Ret', 'BnH_Ret', 'Strategy_NAV', 'BnH_NAV']].to_csv(equity_path)

    summary = {
        'strategy_name': strategy_name,
        'data_source': {'ixic': ixic_source, 'bond': bond_source},
        'start': str(df.index[0].date()),
        'end': str(df.index[-1].date()),
        'bars': int(len(df)),
        'params': params,
        'strategy': {
            'cagr': cagr_s,
            'max_drawdown': mdd_s,
            'sharpe': sharpe_s,
            'final_nav': float(df['Strategy_NAV'].iloc[-1]),
        },
        'buy_hold': {
            'cagr': cagr_b,
            'max_drawdown': mdd_b,
            'sharpe': sharpe_b,
            'final_nav': float(df['BnH_NAV'].iloc[-1]),
        },
        'files': {
            'equity_curve_csv': str(equity_path),
            'plot_png': str(plot_path),
            'summary_json': str(outdir / 'summary.json'),
        },
    }
    (outdir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary
