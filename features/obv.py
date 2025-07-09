import pandas as pd

def add_obv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add On-Balance Volume (OBV) to the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Close' and 'Volume' columns.

    Returns:
        pd.DataFrame: DataFrame with 'obv' column.
    """
    obv = [0]  # start with zero OBV
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i - 1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i - 1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    df['obv'] = obv
    return df
