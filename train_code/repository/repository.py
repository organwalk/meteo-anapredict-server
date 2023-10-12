"""
    定义获取数据源的方法
    by organwalk 2023-09-19
"""
from typing import Union, List
from config import FILE_PATH
from datetime import datetime, timedelta
import os
import numpy as np
import pandas as pd
from typing import Tuple
from train_code.utils import data_utils
from sklearn.preprocessing import MinMaxScaler
from train_code.utils import data_utils as dtools


def get_csv(station: str, start_date: str, end_date: str) -> Union[List[str], str]:
    """
    获取有效csv数据集文件路径列表
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        List[str] or AnyStr: 返回csv数据集文件路径列表，无法前向填充时返回错误消息

    by organwalk 2023-09-17
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    existing_files = []
    existing_path = ''
    current_date = start_date
    consecutive_missing_count = 0
    while current_date <= end_date:
        # 构建文件名
        file_path = f"{FILE_PATH}{station}_data_{current_date.strftime('%Y-%m-%d')}.csv"
        if os.path.exists(file_path):
            existing_files.append(file_path)
            consecutive_missing_count = 0
            existing_path = file_path
        else:
            if consecutive_missing_count < 5:
                existing_files.append(existing_path)
                consecutive_missing_count += 1
            else:
                return "连续时间段内缺失文件过多，无法进行前向填充"

        current_date += timedelta(days=1)

    return existing_files


def get_one_csv_data(station: str, date: str) -> Tuple[pd.DataFrame, MinMaxScaler]:
    """
    获取一份CSV数据集经过归一化处理后的数据窗
    :param station: 气象站编号
    :param date: 日期
    :return:
        DataFrame and MinMaxScaler: 归一化后的数据窗以及解归一化需要使用的MinMaxScaler对象

    by organwalk 2023-09-17
    """
    file_path = f"{FILE_PATH}{station}_data_{date}.csv"
    # 0.将指定数据集读取为pandas数据窗
    df_file_data = pd.read_csv(file_path)
    # 1.将数据窗的每个特征处理为保留小数点后两位的24小时平均值
    df_avg_data = data_utils.calculate_hour_avg(df_file_data)
    # 2.将上一步数据进行归一化处理，获得最终的数据窗
    df_scaler_data, scaler = data_utils.get_scaler_result(df_avg_data)
    return df_scaler_data, scaler


def get_seven_csv_data(station: str, date: str) -> Tuple[list, MinMaxScaler]:
    datetime_date = datetime.strptime(date, '%Y-%m-%d')
    end_date = datetime_date + timedelta(days=6)
    print(end_date)
    end_date = end_date.strftime('%Y-%m-%d')
    existing_files = get_csv(station, date, end_date)
    all_data = list()
    scaler = None
    for file in existing_files:
        df = pd.read_csv(file)
        avg_df_data = dtools.calculate_day_avg(df)
        df_data, scaler = dtools.get_scaler_result(avg_df_data)
        all_data.append(df_data)
    print(all_data)
    print(type(all_data))
    return all_data, scaler


def get_one_csv_data_tolist(station: str, date: str) -> List[List[float]]:
    file_path = f"{FILE_PATH}{station}_data_{date}.csv"
    # 0. 将指定数据集读取为pandas数据窗
    df_file_data = pd.read_csv(file_path)
    # 1. 将数据窗的每个特征处理为保留小数点后两位的24小时平均值
    df_avg_data = data_utils.calculate_hour_avg(df_file_data)
    # 2. 返回二维数组
    np_avg_data = np.round(df_avg_data.values).astype(float)
    return np_avg_data.tolist()

# print(get_csv('1', '2023-07-28', '2023-08-03'))
