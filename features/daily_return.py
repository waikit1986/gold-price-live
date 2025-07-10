import pandas as pd

def add_daily_return(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    Add return percentage over a given period to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.
        period (int): Number of periods over which to compute return.

    Returns:
        pd.DataFrame: DataFrame with 'return_{period}' column.
    """
    df[f'return_{period}'] = df['Close'].pct_change(periods=period) * 100
    return df
