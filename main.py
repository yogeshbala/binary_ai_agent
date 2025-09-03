
from strategies import (
    bollinger_rejection, breakout_volume, heikin_ashi_trend, macd_ema_crossover,
    martingale_trend, momentum_scalping, retest_level, rsi_divergence,
    stoch_sr_bounce, supertrend_rsi, time_filter, triple_indicator
)

def run_all_strategies(symbol="EURUSD=X", interval="15m"):
    strategy_modules = {
        "Bollinger Rejection": bollinger_rejection,
        "Breakout Volume": breakout_volume,
        "Heikin Ashi Trend": heikin_ashi_trend,
        "MACD EMA Crossover": macd_ema_crossover,
        "Martingale Trend": martingale_trend,
        "Momentum Scalping": momentum_scalping,
        "Retest Level": retest_level,
        "RSI Divergence": rsi_divergence,
        "Stoch SR Bounce": stoch_sr_bounce,
        "Supertrend RSI": supertrend_rsi,
        "Time Filter": time_filter,
        "Triple Indicator": triple_indicator
    }

    results = {}
    for name, module in strategy_modules.items():
        try:
            df = module.fetch_data(symbol=symbol, interval=interval)
            df = module.compute_indicators(df)
            signal = module.generate_signal(df)
            results[name] = signal
        except Exception as e:
            results[name] = f"Error: {str(e)}"
    return results
