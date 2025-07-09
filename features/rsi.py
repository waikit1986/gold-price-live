import pandas as pd

def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add Relative Strength Index (RSI) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.
        window (int): Window size for RSI calculation.

    Returns:
        pd.DataFrame: DataFrame with 'rsi' column added.
    """
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df
