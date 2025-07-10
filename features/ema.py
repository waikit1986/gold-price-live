import pandas as pd
from typing import List

def add_ema(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
    """
    Add Exponential Moving Averages (EMA) to the dataframe.

    Parameters:
        df (pd.DataFrame): Input dataframe with 'Close' column.
        windows (List[int]): List of window sizes for EMAs.

    Returns:
        pd.DataFrame: DataFrame with new EMA columns.
    """
    for window in windows:
        df[f'ema_{window}'] = df['Close'].ewm(span=window, adjust=False).mean()
    return df
