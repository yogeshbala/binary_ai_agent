import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="5m", period="1d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_trend(df):
    df['EMA12'] = talib.EMA(df['Close'], timeperiod=12)
    df['EMA26'] = talib.EMA(df['Close'], timeperiod=26)
    df['Trend'] = df['EMA12'] > df['EMA26']
    return df

def martingale_signal(df, last_result="LOSS", last_direction="CALL", base_amount=10):
    latest = df.iloc[-1]
    trend_up = latest['Trend']
    direction = "CALL" if trend_up else "PUT"

    if last_result == "LOSS" and last_direction == direction:
        amount = base_amount * 2
    else:
        amount = base_amount

    return direction, amount

if __name__ == "__main__":
    df = fetch_data()
    df = compute_trend(df)

    # Simulate last trade result
    last_result = "LOSS"  # or "WIN"
    last_direction = "CALL"
    direction, amount = martingale_signal(df, last_result, last_direction)
    print(f"Martingale Signal: {direction} with amount ${amount}")
