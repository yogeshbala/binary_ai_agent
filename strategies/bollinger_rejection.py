import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_indicators(df):
    upper, middle, lower = talib.BBANDS(df['Close'], timeperiod=20)
    df['UpperBand'] = upper
    df['LowerBand'] = lower
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    return df

def detect_rejection(df):
    latest = df.iloc[-1]
    body = abs(latest['Close'] - latest['Open'])
    wick = latest['High'] - latest['Low']

    # Rejection logic
    if latest['Low'] < latest['LowerBand'] and latest['Close'] > latest['Open'] and latest['RSI'] < 30:
        return "CALL"
    elif latest['High'] > latest['UpperBand'] and latest['Close'] < latest['Open'] and latest['RSI'] > 70:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_indicators(df)
    signal = detect_rejection(df)
    print(f"Bollinger Rejection Signal: {signal}")
