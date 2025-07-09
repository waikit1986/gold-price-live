import pandas as pd

def add_volatility(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add rolling volatility (standard deviation) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.
        window (int): Window size for rolling standard deviation.

    Returns:
        pd.DataFrame: DataFrame with 'volatility' column.
    """
    df['volatility'] = df['Close'].rolling(window=window).std()
    return df
