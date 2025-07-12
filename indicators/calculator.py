# indicators/calculator.py
import pandas as pd
import numpy as np

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Lagged price features
    df['price_lag_1'] = df['price'].shift(1)
    df['price_lag_2'] = df['price'].shift(2)

    # Simple Moving Average (SMA)
    df['sma_20'] = df['price'].rolling(window=20).mean()
    df['sma_50'] = df['price'].rolling(window=50).mean()
    df['sma_20_lag_1'] = df['sma_20'].shift(1)
    df['sma_50_lag_1'] = df['sma_50'].shift(1)

    # Exponential Moving Average (EMA)
    df['ema_20'] = df['price'].ewm(span=20, adjust=False).mean()
    df['ema_50'] = df['price'].ewm(span=50, adjust=False).mean()
    df['ema_20_lag_1'] = df['ema_20'].shift(1)
    df['ema_50_lag_1'] = df['ema_50'].shift(1)

    # RSI (Relative Strength Index) 14 periods
    delta = df['price'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['rsi_14'] = 100 - (100 / (1 + rs))
    df['rsi_14_lag_1'] = df['rsi_14'].shift(1)

    # MACD (12,26) and Signal (9)
    ema_12 = df['price'].ewm(span=12, adjust=False).mean()
    ema_26 = df['price'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema_12 - ema_26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    df['macd_lag_1'] = df['macd'].shift(1)
    df['macd_signal_lag_1'] = df['macd_signal'].shift(1)
    df['macd_hist_lag_1'] = df['macd_hist'].shift(1)

    # Bollinger Bands (20, 2 std)
    sma_20 = df['price'].rolling(window=20).mean()
    std_20 = df['price'].rolling(window=20).std()
    df['bb_upper'] = sma_20 + 2 * std_20
    df['bb_middle'] = sma_20
    df['bb_lower'] = sma_20 - 2 * std_20
    df['bb_upper_lag_1'] = df['bb_upper'].shift(1)
    df['bb_middle_lag_1'] = df['bb_middle'].shift(1)
    df['bb_lower_lag_1'] = df['bb_lower'].shift(1)

    # ATR (Average True Range) 14 periods
    high = df['price']  # Assuming no separate high, low, close; you may need to adjust this
    low = df['price']
    close = df['price']
    df['tr'] = pd.concat([
        (high - low).abs(),
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    df['atr_14'] = df['tr'].rolling(window=14).mean()
    df['atr_14_lag_1'] = df['atr_14'].shift(1)
    df.drop(columns=['tr'], inplace=True)

    # Stochastic Oscillator %K and %D (14,3)
    low_14 = df['price'].rolling(window=14).min()
    high_14 = df['price'].rolling(window=14).max()
    df['stochastic_k'] = 100 * (df['price'] - low_14) / (high_14 - low_14)
    df['stochastic_d'] = df['stochastic_k'].rolling(window=3).mean()
    df['stochastic_k_lag_1'] = df['stochastic_k'].shift(1)
    df['stochastic_d_lag_1'] = df['stochastic_d'].shift(1)

    return df
