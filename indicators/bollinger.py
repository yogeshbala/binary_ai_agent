
import talib

def compute_bollinger(df, timeperiod=20, nbdevup=2, nbdevdn=2):
    upper, middle, lower = talib.BBANDS(
        df['Close'],
        timeperiod=timeperiod,
        nbdevup=nbdevup,
        nbdevdn=nbdevdn,
        matype=0
    )
    df['BB_upper'] = upper
    df['BB_middle'] = middle
    df['BB_lower'] = lower
    return df
