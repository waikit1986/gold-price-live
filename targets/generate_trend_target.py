import pandas as pd

def generate_trend_target(df: pd.DataFrame, column: str = 'Close', steps: int = None) -> pd.DataFrame:
    """
    Adds a 'target_cls_trend' column to the input DataFrame.
    
    Parameters:
        df (pd.DataFrame): Must contain a 'Close' or similar price column.
        column (str): Column name to use for trend detection (default: 'Close').
        steps (int): How many future bars to look ahead (e.g., 3 for 3-day or 3-bar trend).
                     Must be explicitly provided when calling the function.

    Returns:
        pd.DataFrame: Original DataFrame with new 'target_cls_trend' column.
            1  → Uptrend
           -1 → Downtrend
            0  → Sideways (default if neither up nor down trend detected)
    """

    if steps is None:
        raise ValueError("Please specify the number of future steps (e.g., steps=3)")

    df = df.copy()

    # Create shifted future close columns
    for i in range(1, steps + 1):
        df[f'future_close_{i}'] = df[column].shift(-i)

    # Define uptrend: all future closes > current close
    up = df[[f'future_close_{i}' for i in range(1, steps + 1)]].gt(df[column], axis=0).all(axis=1)

    # Define downtrend: all future closes < current close
    down = df[[f'future_close_{i}' for i in range(1, steps + 1)]].lt(df[column], axis=0).all(axis=1)

    # Assign target values
    df['target_cls_trend'] = 0  # Default: sideways
    df.loc[up, 'target_cls_trend'] = 1
    df.loc[down, 'target_cls_trend'] = -1

    # Drop temporary columns
    df.drop(columns=[f'future_close_{i}' for i in range(1, steps + 1)], inplace=True)

    return df
