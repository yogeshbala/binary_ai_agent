import talib

def compute_rsi(df, period=14):
    df['RSI'] = talib.RSI(df['Close'], timeperiod=period)
    return df
