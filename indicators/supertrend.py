import pandas as pd

def compute_supertrend(df, period=10, multiplier=3):
    hl2 = (df['High'] + df['Low']) / 2
    df['ATR'] = df['High'].rolling(window=period).max() - df['Low'].rolling(window=period).min()
    df['UpperBand'] = hl2 + (multiplier * df['ATR'])
    df['LowerBand'] = hl2 - (multiplier * df['ATR'])

    df['Supertrend'] = True
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['UpperBand'].iloc[i - 1]:
            df['Supertrend'].iloc[i] = True
        elif df['Close'].iloc[i] < df['LowerBand'].iloc[i - 1]:
            df['Supertrend'].iloc[i] = False
        else:
            df['Supertrend'].iloc[i] = df['Supertrend'].iloc[i - 1]
    return df
