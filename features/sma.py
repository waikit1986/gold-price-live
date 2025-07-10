import pandas as pd
from typing import List

def add_sma(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
    """
    Add Simple Moving Averages (SMA) to the dataframe.

    Parameters:
        df (pd.DataFrame): Input dataframe with 'Close' column.
        windows (List[int]): List of window sizes for SMAs.

    Returns:
        pd.DataFrame: DataFrame with new SMA columns.
    """
    for window in windows:
        df[f'sma_{window}'] = df['Close'].rolling(window=window).mean()
    return df

