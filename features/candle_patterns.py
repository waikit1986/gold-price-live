import pandas as pd

def add_candle_patterns(
    df: pd.DataFrame,
    doji_threshold: float,
    hammer_body_threshold: float,
    hammer_shadow_multiplier: float
) -> pd.DataFrame:
    """
    Add simple candlestick pattern flags: Doji, Hammer, Bullish Engulfing.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Open', 'High', 'Low', 'Close'.
        doji_threshold (float): Max body-to-range ratio for Doji.
        hammer_body_threshold (float): Max body-to-range ratio for Hammer.
        hammer_shadow_multiplier (float): Minimum lower shadow length as multiple of body.

    Returns:
        pd.DataFrame: DataFrame with pattern flags (1 if detected, else 0).
    """
    body = (df['Close'] - df['Open']).abs()
    range_ = df['High'] - df['Low']
    body_pct = body / range_.replace(0, 0.0001)

    # Doji: open ≈ close
    df['doji'] = (body_pct < doji_threshold).astype(int)

    # Hammer: small body, long lower shadow
    lower_shadow = df[['Open', 'Close']].min(axis=1) - df['Low']
    df['hammer'] = ((body_pct < hammer_body_threshold) & (lower_shadow > hammer_shadow_multiplier * body)).astype(int)

    # Bullish Engulfing
    prev_open = df['Open'].shift(1)
    prev_close = df['Close'].shift(1)
    df['bullish_engulfing'] = (
        (df['Open'] < df['Close']) & (prev_close < prev_open) &
        (df['Open'] < prev_close) & (df['Close'] > prev_open)
    ).astype(int)

    return df
