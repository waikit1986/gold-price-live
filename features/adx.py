import pandas as pd

def add_adx(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    Add Average Directional Index (ADX), +DI, and -DI to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'High', 'Low', 'Close' columns.
        period (int): Number of periods for calculation.

    Returns:
        pd.DataFrame: DataFrame with 'adx', 'plus_di', and 'minus_di' columns.
    """
    high = df['High']
    low = df['Low']
    close = df['Close']

    up_move = high.diff()
    down_move = low.diff().abs()
    plus_dm = (up_move > down_move) & (up_move > 0) * up_move
    minus_dm = (down_move > up_move) & (low.shift(1) - low > 0) * down_move

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period, min_periods=1).mean()

    plus_di = 100 * (plus_dm.rolling(window=period).sum() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).sum() / atr)

    dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di))
    df['adx'] = dx.rolling(window=period, min_periods=1).mean()
    df['plus_di'] = plus_di
    df['minus_di'] = minus_di

    return df
