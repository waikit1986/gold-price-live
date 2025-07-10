import pandas as pd

def add_volatility_breakout(df: pd.DataFrame, atr_period: int, multiplier: float) -> pd.DataFrame:
    """
    Add a breakout signal when the price moves beyond a multiple of ATR from the previous close.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close', 'High', 'Low'.
        atr_period (int): Period to compute ATR.
        multiplier (float): ATR multiplier for breakout threshold.

    Returns:
        pd.DataFrame: DataFrame with 'volatility_breakout' column (1 if breakout, else 0).
    """
    high = df['High']
    low = df['Low']
    close = df['Close']
    prev_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=atr_period).mean()

    breakout = ((high - prev_close) > multiplier * atr) | ((prev_close - low) > multiplier * atr)
    df['volatility_breakout'] = breakout.astype(int)

    return df
