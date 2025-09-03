import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_heikin_ashi(df):
    ha_df = pd.DataFrame(index=df.index)
    ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha_df['HA_Open'] = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
    ha_df['HA_Open'].fillna(df['Open'], inplace=True)
    ha_df['HA_High'] = df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    ha_df['HA_Low'] = df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
    return ha_df

def compute_ema(df):
    df['EMA20'] = talib.EMA(df['Close'], timeperiod=20)
    df['EMA50'] = talib.EMA(df['Close'], timeperiod=50)
    return df

def generate_signal(df, ha_df):
    latest = df.iloc[-1]
    ha_latest = ha_df.iloc[-1]

    bullish_candle = ha_latest['HA_Close'] > ha_latest['HA_Open']
    bearish_candle = ha_latest['HA_Close'] < ha_latest['HA_Open']
    ema_bullish = latest['EMA20'] > latest['EMA50']
    ema_bearish = latest['EMA20'] < latest['EMA50']

    if bullish_candle and ema_bullish:
        return "CALL"
    elif bearish_candle and ema_bearish:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    ha_df = compute_heikin_ashi(df)
    df = compute_ema(df)
    signal = generate_signal(df, ha_df)
    print(f"Heikin Ashi + Trend Filter Signal: {signal}")
