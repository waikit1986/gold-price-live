import pandas as pd

def add_macd(df: pd.DataFrame,
             fast_period: int = 12,
             slow_period: int = 26,
             signal_period: int = 9) -> pd.DataFrame:
    """
    Add MACD, MACD Signal Line, and MACD Histogram to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.
        fast_period (int): Short-term EMA period.
        slow_period (int): Long-term EMA period.
        signal_period (int): Signal line EMA period.

    Returns:
        pd.DataFrame: DataFrame with 'macd', 'macd_signal', and 'macd_hist' columns added.
    """
    ema_fast = df['Close'].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow_period, adjust=False).mean()
    df['macd'] = ema_fast - ema_slow
    df['macd_signal'] = df['macd'].ewm(span=signal_period, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    return df
