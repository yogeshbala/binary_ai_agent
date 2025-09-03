
import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="1m", period="1d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_momentum(df):
    df['BodySize'] = abs(df['Close'] - df['Open'])
    df['VolumeSpike'] = df['Volume'] > df['Volume'].rolling(window=10).mean() * 1.5
    df['Momentum'] = talib.MOM(df['Close'], timeperiod=5)
    return df

def generate_signal(df, body_threshold=0.0005):
    latest = df.iloc[-1]
    if latest['BodySize'] > body_threshold and latest['VolumeSpike']:
        direction = "CALL" if latest['Momentum'] > 0 else "PUT"
        return direction
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_momentum(df)
    signal = generate_signal(df)
    print(f"Momentum Scalping Signal: {signal}")
