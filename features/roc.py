import pandas as pd

def add_roc(df: pd.DataFrame, period: int = 12) -> pd.DataFrame:
    """
    Add Rate of Change (ROC) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' column.
        period (int): Number of periods over which to calculate ROC.

    Returns:
        pd.DataFrame: DataFrame with 'roc' column.
    """
    df['roc'] = df['Close'].pct_change(periods=period) * 100
    return df
