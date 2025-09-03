from strategies import bollinger_rejection, macd_ema_crossover, triple_indicator
from data.fetch_data import fetch_data
from utils.backtest import backtest_strategy

strategies = {
    "Bollinger Rejection": bollinger_rejection,
    "MACD EMA Crossover": macd_ema_crossover,
    "Triple Indicator": triple_indicator
}

df = fetch_data(symbol="EURUSD=X", interval="15m", period="7d")

for name, module in strategies.items():
    df_ind = module.compute_indicators(df.copy())
    trades = backtest_strategy(module, df_ind)
    win_rate = sum(1 for t in trades if t > 0) / len(trades) if trades else 0
    print(f"{name}: {len(trades)} trades, Win Rate: {win_rate:.2%}")
