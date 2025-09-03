
import yfinance as yf
import pandas as pd

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    df['Time'] = df.index.time
    return df

def is_valid_time_window(time, start="09:00", end="11:00"):
    from datetime import datetime
    fmt = "%H:%M"
    return datetime.strptime(start, fmt).time() <= time <= datetime.strptime(end, fmt).time()

def filter_by_time(df, start="09:00", end="11:00"):
    latest = df.iloc[-1]
    if is_valid_time_window(latest['Time'], start, end):
        return "TRADE ALLOWED"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    signal = filter_by_time(df)
    print(f"Time Filter Signal: {signal}")
