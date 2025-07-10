import pandas as pd

def add_support_resistance(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """
    Add recent support and resistance levels using rolling lows and highs.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'High' and 'Low'.
        window (int): Number of periods to define support/resistance range.

    Returns:
        pd.DataFrame: DataFrame with 'support' and 'resistance' columns.
    """
    df['resistance'] = df['High'].rolling(window=window, min_periods=1).max()
    df['support'] = df['Low'].rolling(window=window, min_periods=1).min()
    return df
