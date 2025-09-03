import yfinance as yf
import pandas as pd
import talib

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def compute_indicators(df):
    atr = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=10)
    hl2 = (df['High'] + df['Low']) / 2
    factor = 3  # Supertrend multiplier

    df['UpperBand'] = hl2 + factor * atr
    df['LowerBand'] = hl2 - factor * atr
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)

    # Supertrend logic
    df['Supertrend'] = None
    trend = True  # Start with bullish assumption

    for i in range(1, len(df)):
        if trend:
            if df['Close'].iloc[i] < df['LowerBand'].iloc[i]:
                trend = False
        else:
            if df['Close'].iloc[i] > df['UpperBand'].iloc[i]:
                trend = True
        df.at[df.index[i], 'Supertrend'] = 'Bullish' if trend else 'Bearish'

    return df

def generate_signal(df):
    latest = df.iloc[-1]
    if latest['Supertrend'] == 'Bullish' and latest['RSI'] > 50:
        return "CALL"
    elif latest['Supertrend'] == 'Bearish' and latest['RSI'] < 50:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    df = compute_indicators(df)
    signal = generate_signal(df)
    print(f"Supertrend + RSI Signal: {signal}")
