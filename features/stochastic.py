import pandas as pd

def add_stochastic(df: pd.DataFrame, k_period: int, d_period: int) -> pd.DataFrame:
    """
    Add Stochastic Oscillator (%K and %D) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'High', 'Low', 'Close' columns.
        k_period (int): Lookback period for %K.
        d_period (int): Smoothing period for %D.

    Returns:
        pd.DataFrame: DataFrame with '%k' and '%d' columns.
    """
    low_min = df['Low'].rolling(window=k_period, min_periods=1).min()
    high_max = df['High'].rolling(window=k_period, min_periods=1).max()
    df['%k'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['%d'] = df['%k'].rolling(window=d_period, min_periods=1).mean()
    return df
