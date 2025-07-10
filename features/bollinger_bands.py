import pandas as pd

def add_bollinger_bands(df: pd.DataFrame, window: int, num_std: float) -> pd.DataFrame:
    """
    Add Bollinger Bands to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.
        window (int): Rolling window size.
        num_std (float): Number of standard deviations for the bands.

    Returns:
        pd.DataFrame: DataFrame with 'bb_upper', 'bb_middle', 'bb_lower' columns added.
    """
    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()

    df['bb_middle'] = rolling_mean
    df['bb_upper'] = rolling_mean + (num_std * rolling_std)
    df['bb_lower'] = rolling_mean - (num_std * rolling_std)
    return df
