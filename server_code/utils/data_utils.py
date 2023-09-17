import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def calculate_hour_avg(df_data: pd.DataFrame) -> pd.DataFrame:
    """
    计算数据窗的每小时的平均结果

    :param df_data: pandas数据窗
    :return:
        DataFrame: 返回24小时的整数数据窗

    by organwalk 2023-09-17
    """
    df_data['Time'] = pd.to_datetime(df_data['Time'])
    df = df_data.set_index('Time')

    df_hourly = df.resample('H').mean().round(2).reset_index().drop('Time', axis=1)

    return df_hourly.astype(int)


def get_scaler_result(df_data: pd.DataFrame) -> (pd.DataFrame, MinMaxScaler):
    """
    获取数据窗归一化后的结果

    :param df_data: pandas数据窗
    :return:
        DataFrame: 返回归一化后的数据及解归一化使用的scaler对象

    by organwalk 2023-09-17
    """
    scaler = MinMaxScaler()
    scaler.fit(df_data)
    return scaler.transform(df_data), scaler
