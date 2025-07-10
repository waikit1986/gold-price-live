import pandas as pd

def add_cci(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    Add Commodity Channel Index (CCI) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'High', 'Low', 'Close' columns.
        period (int): Number of periods for calculation.

    Returns:
        pd.DataFrame: DataFrame with 'cci' column.
    """
    tp = (df['High'] + df['Low'] + df['Close']) / 3  # Typical Price
    ma = tp.rolling(window=period).mean()
    md = tp.rolling(window=period).apply(lambda x: pd.Series(x).mad())
    df['cci'] = (tp - ma) / (0.015 * md)
    return df
