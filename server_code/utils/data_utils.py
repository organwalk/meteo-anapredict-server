import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def calculate_hour_avg(df_data: pd.DataFrame) -> pd.DataFrame:
    df_data['Time'] = pd.to_datetime(df_data['Time'])
    df = df_data.set_index('Time')

    df_hourly = df.resample('H').mean().round(2).reset_index().drop('Time', axis=1)

    return df_hourly.astype(int)


def get_scaler_result(df_data: pd.DataFrame):
    scaler = MinMaxScaler()
    scaler.fit(df_data)
    return scaler.transform(df_data), scaler
