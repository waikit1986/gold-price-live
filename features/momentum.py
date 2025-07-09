import pandas as pd

def add_momentum(df: pd.DataFrame, period: int = 10) -> pd.DataFrame:
    """
    Add Momentum indicator to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.
        period (int): Number of periods for momentum calculation.

    Returns:
        pd.DataFrame: DataFrame with 'momentum' column.
    """
    df['momentum'] = df['Close'] - df['Close'].shift(period)
    return df
