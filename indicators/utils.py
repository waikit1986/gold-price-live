import pandas as pd

def resample_dataframe(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    df = df.set_index('timestamp')
    df = df.resample(timeframe).agg({'price': 'last'}).dropna()
    df = df.reset_index()
    return df
