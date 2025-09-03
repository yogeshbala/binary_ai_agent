import talib

def compute_ema(df, period=20):
    df['EMA'] = talib.EMA(df['Close'], timeperiod=period)
    return df
