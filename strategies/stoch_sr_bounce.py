import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_indicators(df):
    slowk, slowd = talib.STOCH(df['High'], df['Low'], df['Close'],
                               fastk_period=14, slowk_period=3, slowk_matype=0,
                               slowd_period=3, slowd_matype=0)
    df['SlowK'] = slowk
    df['SlowD'] = slowd
    return df

def identify_zones(df, lookback=20):
    recent_high = df['High'].tail(lookback).max()
    recent_low = df['Low'].tail(lookback).min()
    return recent_high, recent_low

def generate_signal(df):
    latest = df.iloc[-1]
    recent_high, recent_low = identify_zones(df)

    # Rejection logic
    if latest['Low'] <= recent_low and latest['SlowK'] > latest['SlowD'] and latest['SlowK'] < 30:
        return "CALL"
    elif latest['High'] >= recent_high and latest['SlowK'] < latest['SlowD'] and latest['SlowK'] > 70:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_indicators(df)
    signal = generate_signal(df)
    print(f"Stochastic + S/R Bounce Signal: {signal}")
