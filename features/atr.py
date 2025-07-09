import pandas as pd

def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Add Average True Range (ATR) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'High', 'Low', and 'Close' columns.
        period (int): Number of periods to calculate ATR over.

    Returns:
        pd.DataFrame: DataFrame with 'atr' column.
    """
    high = df['High']
    low = df['Low']
    close = df['Close']

    # Calculate True Range components
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()

    # Combine the True Range
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Calculate ATR
    df['atr'] = true_range.rolling(window=period, min_periods=1).mean()

    return df
