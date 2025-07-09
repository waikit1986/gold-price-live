import pandas as pd

def add_daily_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add daily return percentage to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.

    Returns:
        pd.DataFrame: DataFrame with 'daily_return' column.
    """
    df['daily_return'] = df['Close'].pct_change() * 100
    return df
