import pandas as pd
from typing import List

def add_volume_ma(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
    """
    Add Volume Moving Averages (MA) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Volume' column.
        windows (List[int]): List of moving average window sizes.

    Returns:
        pd.DataFrame: DataFrame with volume MA columns added.
    """
    for window in windows:
        df[f'volume_ma_{window}'] = df['Volume'].rolling(window=window).mean()
    return df
