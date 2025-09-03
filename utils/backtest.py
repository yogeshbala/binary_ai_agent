def backtest_strategy(strategy_module, df, hold_period=3):
    trades = []
    for i in range(len(df) - hold_period):
        window = df.iloc[i:i+hold_period+1]
        signal_data = strategy_module.generate_signal(window)
        if signal_data["signal"] in ["CALL", "PUT"]:
            entry = signal_data["entry_price"]
            exit = window['Close'].iloc[-1]
            direction = 1 if signal_data["signal"] == "CALL" else -1
            pnl = (exit - entry) * direction
            trades.append(pnl)
    return trades
