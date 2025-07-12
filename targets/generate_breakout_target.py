import pandas as pd

def generate_breakout_target(
    df: pd.DataFrame,
    close_col: str = 'Close',
    high_col: str = 'High',
    low_col: str = 'Low',
    window: int = 20,
    atr_window: int = 14,
    atr_multiplier: float = 0.5,
    target_col: str = 'target_cls_breakout'
) -> pd.DataFrame:
    """
    Adds a breakout classification target column to the DataFrame.

    Classes:
        1  = breakout up (above resistance)
       -1  = breakdown down (below support)
        0  = no breakout

    Parameters:
        df (pd.DataFrame): Data with OHLC columns.
        close_col (str): Column for close prices.
        high_col (str): Column for highs.
        low_col (str): Column for lows.
        window (int): Lookback period for local high/low (support/resistance).
        atr_window (int): Lookback for ATR calculation.
        atr_multiplier (float): ATR buffer added to high/low.
        target_col (str): Name of the column to add.

    Returns:
        pd.DataFrame: With added `target_col`.
    """
    df = df.copy()

    # Support / resistance levels
    df['_recent_high'] = df[high_col].rolling(window=window).max()
    df['_recent_low'] = df[low_col].rolling(window=window).min()

    # True Range calculation
    df['_hl'] = df[high_col] - df[low_col]
    df['_hc'] = abs(df[high_col] - df[close_col].shift(1))
    df['_lc'] = abs(df[low_col] - df[close_col].shift(1))
    df['_tr'] = df[['_hl', '_hc', '_lc']].max(axis=1)

    # ATR calculation
    df['_atr'] = df['_tr'].rolling(window=atr_window).mean()

    # Breakout / breakdown logic
    breakout_up = df[close_col] > (df['_recent_high'] + atr_multiplier * df['_atr'])
    breakout_down = df[close_col] < (df['_recent_low'] - atr_multiplier * df['_atr'])

    # Assign classes
    df[target_col] = 0
    df.loc[breakout_up, target_col] = 1
    df.loc[breakout_down, target_col] = -1

    # Clean up temporary columns
    df.drop(columns=[c for c in df.columns if c.startswith('_')], inplace=True)

    return df
