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
    # 0. 获取有效数据文件路径数组
    existing_files = repository.get_csv(station, start_date, end_date)
    if isinstance(existing_files, str):
        return existing_files
    x, y = list(), list()
    scaler = None
    for i in range(len(existing_files)):
        df_current = pd.read_csv(existing_files[i])
        avg_df_current = dtools.calculate_day_avg(df_current)
        df_data_current, scaler = dtools.get_scaler_result(avg_df_current)
        x.append(df_data_current)
        output_group = []
        if len(existing_files) - i >= 7:
            for output_index in range(1, len(existing_files)):
                df_next = pd.read_csv(existing_files[i + output_index])
                avg_df_next = dtools.calculate_day_avg(df_next)
                df_next, _ = dtools.get_scaler_result(avg_df_next)
                output_group.append(df_next)
                if output_index > 7:
                    break
        y.append(output_group)
    return np.array(x), np.array(y), scaler
