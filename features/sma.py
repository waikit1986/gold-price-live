import pandas as pd

def add_sma(df: pd.DataFrame, windows=[10, 20, 50, 100, 200]) -> pd.DataFrame:
    """
    Add Simple Moving Averages (SMA) to the dataframe.
    
    Parameters:
        df (pd.DataFrame): Input dataframe with 'Close' column.
        windows (list): List of window sizes for SMAs.

    Returns:
        pd.DataFrame: DataFrame with new SMA columns.
    """
    for window in windows:
        df[f'sma_{window}'] = df['Close'].rolling(window=window).mean()
    return df
