import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="15m", period="5d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_rsi(df):
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    return df

def detect_divergence(df):
    lows = df['Low'].tail(10)
    rsi_vals = df['RSI'].tail(10)

    # Bullish divergence: price lower low, RSI higher low
    if lows.iloc[-1] < lows.iloc[-3] and rsi_vals.iloc[-1] > rsi_vals.iloc[-3] and rsi_vals.iloc[-1] < 40:
        return "CALL"

    # Bearish divergence: price higher high, RSI lower high
    elif df['High'].iloc[-1] > df['High'].iloc[-3] and rsi_vals.iloc[-1] < rsi_vals.iloc[-3] and rsi_vals.iloc[-1] > 60:
        return "PUT"

    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_rsi(df)
    signal = detect_divergence(df)
    print(f"RSI Divergence Signal: {signal}")
