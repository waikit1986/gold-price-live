
import pandas as pd

def generate_regression_targets(
    df: pd.DataFrame,
    close_col: str = 'Close',
    steps_ahead: int = 3,
    target_price_col: str = 'target_reg_close',
    target_return_col: str = 'target_reg_return'
) -> pd.DataFrame:
    """
    Adds future close price and return regression targets.

    Parameters:
        df: Price DataFrame with a close price column.
        close_col: Column name for current price.
        steps_ahead: How many future steps to shift.
        target_price_col: Output column for future price (regression).
        target_return_col: Output column for log return (optional).

    Returns:
        DataFrame with 1–2 new columns:
            - target_reg_close (price in N steps)
            - target_reg_return (log return over N steps)
    """
    df = df.copy()

    # Future price target
    df[target_price_col] = df[close_col].shift(-steps_ahead)

    # Future return (optional)
    df[target_return_col] = (df[target_price_col] / df[close_col]).apply(lambda x: pd.NA if pd.isna(x) else pd.np.log(x))

    return df
