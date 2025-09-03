
import yfinance as yf
import pandas as pd

def fetch_data(symbol="EURUSD=X", interval="15m", period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df.dropna(inplace=True)
    return df

def identify_levels(df, window=20):
    recent_high = df['High'].rolling(window=window).max().iloc[-1]
    recent_low = df['Low'].rolling(window=window).min().iloc[-1]
    return recent_high, recent_low

def detect_breakout_and_retest(df, high, low):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    breakout_up = prev['Close'] < high and latest['Close'] > high
    breakout_down = prev['Close'] > low and latest['Close'] < low

    retest_up = latest['Low'] <= high and latest['Close'] > high
    retest_down = latest['High'] >= low and latest['Close'] < low

    rejection_up = latest['Close'] > latest['Open'] and (latest['Low'] < high)
    rejection_down = latest['Close'] < latest['Open'] and (latest['High'] > low)

    if breakout_up and retest_up and rejection_up:
        return "CALL"
    elif breakout_down and retest_down and rejection_down:
        return "PUT"
    else:
        return "NO TRADE"

if __name__ == "__main__":
    df = fetch_data()
    high, low = identify_levels(df)
    signal = detect_breakout_and_retest(df, high, low)
    print(f"Retest Level Signal: {signal}")
