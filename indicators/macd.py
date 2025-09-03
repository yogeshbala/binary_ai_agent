
import talib

def compute_macd(df, fastperiod=12, slowperiod=26, signalperiod=9):
    macd, macd_signal, macd_hist = talib.MACD(
        df['Close'],
        fastperiod=fastperiod,
        slowperiod=slowperiod,
        signalperiod=signalperiod
    )
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['MACD_hist'] = macd_hist
    return df
