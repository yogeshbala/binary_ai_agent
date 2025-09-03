import pandas as pd
import talib

def compute_supertrend(df, atr_period=10, multiplier=3):
    df = df.copy()

    # Calculate ATR using talib
    df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=atr_period)

    # Calculate basic bands
    hl2 = (df['High'] + df['Low']) / 2
    df['UpperBand'] = hl2 + (multiplier * df['ATR'])
    df['LowerBand'] = hl2 - (multiplier * df['ATR'])

    # Initialize Supertrend column
    df['Supertrend'] = True
    df['FinalUpperBand'] = df['UpperBand']
    df['FinalLowerBand'] = df['LowerBand']

    for i in range(1, len(df)):
        curr_close = df['Close'].iloc[i]
        prev_close = df['Close'].iloc[i - 1]
        prev_supertrend = df['Supertrend'].iloc[i - 1]

        # Final bands logic
        if curr_close > df['FinalUpperBand'].iloc[i - 1]:
            df['Supertrend'].iloc[i] = True
        elif curr_close < df['FinalLowerBand'].iloc[i - 1]:
            df['Supertrend'].iloc[i] = False
        else:
            df['Supertrend'].iloc[i] = prev_supertrend
            if prev_supertrend:
                df['FinalLowerBand'].iloc[i] = max(df['LowerBand'].iloc[i], df['FinalLowerBand'].iloc[i - 1])
            else:
                df['FinalUpperBand'].iloc[i] = min(df['UpperBand'].iloc[i], df['FinalUpperBand'].iloc[i - 1])

    return df
