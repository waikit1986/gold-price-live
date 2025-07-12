import pandas as pd

def generate_volatility_spike(
    df: pd.DataFrame,
    close_col: str = 'Close',
    return_window: int = 5,
    vol_window: int = 20,
    spike_threshold: float = 2.0,
    target_col: str = 'target_cls_volatility_spike'
) -> pd.DataFrame:
    """
    Adds a binary classification target that indicates a volatility spike.
    
    Spike is defined as:
        rolling volatility > mean + N * std of volatility

    Parameters:
        df: DataFrame with close prices
        close_col: column name of close prices
        return_window: window to compute returns for volatility
        vol_window: window to compute rolling volatility stats
        spike_threshold: number of std deviations above mean to call a spike
        target_col: output column name

    Returns:
        DataFrame with new binary column:
            1 = spike
            0 = no spike
    """
    df = df.copy()

    # Log returns
    df['_log_return'] = (df[close_col] / df[close_col].shift(1)).apply(lambda x: pd.NA if pd.isna(x) else pd.np.log(x))

    # Rolling volatility (std of returns)
    df['_volatility'] = df['_log_return'].rolling(window=return_window).std()

    # Mean and std of volatility
    vol_mean = df['_volatility'].rolling(window=vol_window).mean()
    vol_std = df['_volatility'].rolling(window=vol_window).std()

    # Spike condition
    spike = df['_volatility'] > (vol_mean + spike_threshold * vol_std)
    df[target_col] = 0
    df.loc[spike, target_col] = 1

    # Clean up
    df.drop(columns=['_log_return', '_volatility'], inplace=True)

    return df
