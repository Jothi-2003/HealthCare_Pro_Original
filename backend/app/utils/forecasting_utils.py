# utils/forecasting_utils.py
import pandas as pd

def prepare_forecast_data(df: pd.DataFrame, date_col: str, value_col: str):
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).sort_index()
    return df[[value_col]]