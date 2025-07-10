import pandas as pd
import numpy as np

def add_obv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add On-Balance Volume (OBV) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' and 'Volume' columns.

    Returns:
        pd.DataFrame: DataFrame with 'obv' column.
    """
    direction = np.sign(df['Close'].diff().fillna(0))
    df['obv'] = (direction * df['Volume']).fillna(0).cumsum()
    return df
