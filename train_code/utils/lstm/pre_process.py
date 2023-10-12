"""
    数据预处理模块
    by organwalk 2023.09.19
"""
from numpy import ndarray
from train_code.repository import repository
import pandas as pd
from train_code.utils import data_utils as dtools
import numpy as np
from typing import Tuple, Union, Optional, Any


def split_short_term_sequences(station: str, start_date: str, end_date: str) \
        -> Union[str, Tuple[ndarray, ndarray, Optional[Any]]]:
    """
    对短期LSTM模型的数据集进行输入序列和输出序列的划分
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        str:错误消息
        ||
        np.array(x):输入序列
        np.array(y)：输出序列
        scaler：解归一化缩放器

    by organwalk 2023-09-19
    """
    # 0. 获取有效数据文件路径数组
    existing_files = repository.get_csv(station, start_date, end_date)
    if isinstance(existing_files, str):
        return existing_files
    # 1. 划分输入和输出序列
    x, y = list(), list()
    scaler = None
    for i in range(len(existing_files) - 1):
        print(f"正在划分输入序列：{existing_files[i]}-->输出序列{existing_files[i + 1]}")
        # 1.1 读取当前（输入序列）和下一份数据（输出序列）
        df_current = pd.read_csv(existing_files[i])
        df_next = pd.read_csv(existing_files[i + 1])

        # 1.2 获取两份数据各自24小时的每小时平均值
        avg_df_current = dtools.calculate_hour_avg(df_current)
        avg_df_next = dtools.calculate_hour_avg(df_next)
        # 1.3 对小时化的数据进行归一化
        df_data_current, scaler = dtools.get_scaler_result(avg_df_current)
        df_data_next, _ = dtools.get_scaler_result(avg_df_next)

        # 1.4 添加到输入和输出序列中
        x.append(df_data_current)
        y.append(df_data_next)

    return np.array(x), np.array(y), scaler


def split_long_term_sequences(station: str, start_date: str, end_date: str) \
        -> Union[str, Tuple[ndarray, ndarray, Optional[Any]]]:
    """
    对长期LSTM模型进行输入序列和输出序列划分
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        str:错误消息
        ||
        np.array(x):输入序列
        np.array(y)：输出序列
        scaler：解归一化缩放器

    by organwalk 2023-10-11
    """
    existing_files = repository.get_csv(station, start_date, end_date)
    if isinstance(existing_files, str):
        return existing_files
    x, y = list(), list()
    scaler = None
    all_data = []
    n_step_in, n_step_out = 7, 7
    for file in existing_files:
        df = pd.read_csv(file)
        avg_df_data = dtools.calculate_day_avg(df)
        df_data, scaler = dtools.get_scaler_result(avg_df_data)
        all_data.append(df_data)
    for i in range(len(all_data)):
        end_ix = i + n_step_in
        out_end_ix = end_ix + n_step_out
        if out_end_ix <= len(all_data):
            seq_x = all_data[i:end_ix]
            seq_y = all_data[end_ix:out_end_ix]
            x.append(seq_x)
            y.append(seq_y)
    x = np.array(x)
    y = np.array(y)
    return x[0], y[0], scaler
