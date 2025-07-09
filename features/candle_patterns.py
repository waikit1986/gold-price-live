import pandas as pd

def add_candle_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple candlestick pattern flags: Doji, Hammer, Engulfing.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Open', 'High', 'Low', 'Close'.

    Returns:
        pd.DataFrame: DataFrame with pattern flags (1 if detected, else 0).
    """
    body = (df['Close'] - df['Open']).abs()
    range_ = df['High'] - df['Low']
    
    # Avoid division by zero
    body_pct = body / range_.replace(0, 0.0001)

    # Doji: open ≈ close
    df['doji'] = (body_pct < 0.1).astype(int)

    # Hammer: small body, long lower shadow
    lower_shadow = df['Open'].where(df['Close'] > df['Open'], df['Close']) - df['Low']
    df['hammer'] = ((body_pct < 0.3) & (lower_shadow > 2 * body)).astype(int)

    # Bullish Engulfing
    prev_open = df['Open'].shift(1)
    prev_close = df['Close'].shift(1)
    df['bullish_engulfing'] = (
        (df['Open'] < df['Close']) & (prev_close < prev_open) &
        (df['Open'] < prev_close) & (df['Close'] > prev_open)
    ).astype(int)

    return df
