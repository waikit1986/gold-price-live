import pandas as pd

def add_volume_ma(df: pd.DataFrame, windows=[10, 20, 50]) -> pd.DataFrame:
    """
    Add Volume Moving Averages (MA) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Volume' column.
        windows (list): List of moving average window sizes.

    Returns:
        pd.DataFrame: DataFrame with volume MA columns added.
    """
    for window in windows:
        df[f'volume_ma_{window}'] = df['Volume'].rolling(window=window).mean()
    return df
