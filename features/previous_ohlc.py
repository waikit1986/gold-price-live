import pandas as pd

def add_previous_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add previous period's Open, High, Low, Close as new features.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Open', 'High', 'Low', 'Close'.

    Returns:
        pd.DataFrame: DataFrame with 'prev_open', 'prev_high', 'prev_low', 'prev_close'.
    """
    df['prev_open'] = df['Open'].shift(1)
    df['prev_high'] = df['High'].shift(1)
    df['prev_low'] = df['Low'].shift(1)
    df['prev_close'] = df['Close'].shift(1)
    return df
