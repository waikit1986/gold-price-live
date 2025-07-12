import pandas as pd

def generate_return_classification(
    df: pd.DataFrame,
    close_col: str = 'Close',
    steps_ahead: int = 3,
    pos_threshold: float = 0.005,  # +0.5% = up move
    neg_threshold: float = -0.005, # -0.5% = down move
    target_col: str = 'target_cls_return'
) -> pd.DataFrame:
    """
    Adds a classification target based on % future return.

    Classes:
        1  → price goes up (return > pos_threshold)
        -1 → price goes down (return < neg_threshold)
        0  → price stays in between (no strong move)

    Parameters:
        df: DataFrame with at least a close price column
        close_col: Name of price column
        steps_ahead: How far in the future to measure return
        pos_threshold: % return above which it's a "buy"
        neg_threshold: % return below which it's a "sell"
        target_col: Output column name

    Returns:
        DataFrame with new target_col added
    """
    df = df.copy()

    # Future return
    future_price = df[close_col].shift(-steps_ahead)
    future_return = (future_price - df[close_col]) / df[close_col]

    # Initialize all as 0
    df[target_col] = 0
    df.loc[future_return > pos_threshold, target_col] = 1
    df.loc[future_return < neg_threshold, target_col] = -1

    return df
