import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_indicators(df):
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    macd, macd_signal, _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['EMA'] = talib.EMA(df['Close'], timeperiod=20)
    return df

def generate_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    macd_cross_up = prev['MACD'] < prev['MACD_signal'] and latest['MACD'] > latest['MACD_signal']
    macd_cross_down = prev['MACD'] > prev['MACD_signal'] and latest['MACD'] < latest['MACD_signal']

    if latest['RSI'] < 30 and macd_cross_up and latest['Close'] > latest['EMA']:
        return "CALL"
    elif latest['RSI'] > 70 and macd_cross_down and latest['Close'] < latest['EMA']:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_indicators(df)
    signal = generate_signal(df)
    print(f"Triple Indicator Signal: {signal}")
