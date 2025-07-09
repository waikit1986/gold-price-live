import pandas as pd

def add_ema(df: pd.DataFrame, windows=[10, 20, 50, 100, 200]) -> pd.DataFrame:
    """
    Add Exponential Moving Averages (EMA) to the dataframe.

    Parameters:
        df (pd.DataFrame): Input dataframe with 'Close' column.
        windows (list): List of window sizes for EMAs.

    Returns:
        pd.DataFrame: DataFrame with new EMA columns.
    """
    for window in windows:
        df[f'ema_{window}'] = df['Close'].ewm(span=window, adjust=False).mean()
    return df
