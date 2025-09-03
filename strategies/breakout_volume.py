import yfinance as yf
import pandas as pd

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_volume_average(df, period=20):
    df['AvgVolume'] = df['Volume'].rolling(window=period).mean()
    return df

def detect_breakout(df):
    latest = df.iloc[-1]
    prev_high = df['High'].iloc[-21:-1].max()
    prev_low = df['Low'].iloc[-21:-1].min()

    is_bull_breakout = latest['Close'] > prev_high and latest['Volume'] > latest['AvgVolume']
    is_bear_breakout = latest['Close'] < prev_low and latest['Volume'] > latest['AvgVolume']

    if is_bull_breakout:
        return "CALL"
    elif is_bear_breakout:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_volume_average(df)
    signal = detect_breakout(df)
    print(f"Breakout Volume Signal: {signal}")
