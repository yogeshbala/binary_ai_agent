import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_indicators(df):
    macd, macdsignal, _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd
    df['MACDSignal'] = macdsignal
    df['EMA12'] = talib.EMA(df['Close'], timeperiod=12)
    df['EMA26'] = talib.EMA(df['Close'], timeperiod=26)
    return df

def generate_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    macd_cross_up = prev['MACD'] < prev['MACDSignal'] and latest['MACD'] > latest['MACDSignal']
    macd_cross_down = prev['MACD'] > prev['MACDSignal'] and latest['MACD'] < latest['MACDSignal']
    ema_bullish = latest['EMA12'] > latest['EMA26']
    ema_bearish = latest['EMA12'] < latest['EMA26']

    if macd_cross_up and ema_bullish:
        return "CALL"
    elif macd_cross_down and ema_bearish:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_indicators(df)
    signal = generate_signal(df)
    print(f"MACD + EMA Signal: {signal}")
