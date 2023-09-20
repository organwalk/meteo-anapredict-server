from train_code.repository import repository
import pandas as pd
from train_code.utils import data_utils as dtools
import numpy as np


def split_short_term_sequences(station: str, start_date: str, end_date: str):
    """
    对短期模型的数据集进行输入序列和输出序列的划分

    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:

    by organwalk 2023-09-19
    """
    existing_files = repository.get_csv(station, start_date, end_date)
    if isinstance(existing_files, str):
        return existing_files
    x, y = list(), list()
    scaler = None
    for i in range(len(existing_files) - 1):
        print(f"正在划分输入序列：{existing_files[i]}, 划分输出序列{existing_files[i + 1]}")
        # 读取当前和下一个数据
        df_current = pd.read_csv(existing_files[i])
        df_next = pd.read_csv(existing_files[i + 1])

        # 对小时化的数据进行归一化
        df_data_current, scaler = dtools.get_scaler_result(dtools.calculate_hour_avg(df_current))
        df_data_next, _ = dtools.get_scaler_result(dtools.calculate_hour_avg(df_next))

        # 添加到输入和输出序列中
        x.append(df_data_current)
        y.append(df_data_next)

    return np.array(x), np.array(y), scaler


# print(split_short_term_sequences('1', '2023-06-27', '2023-07-05'))
