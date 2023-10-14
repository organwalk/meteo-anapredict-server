import config
from server_code.entity import res_entity
from config import FILE_PATH, MODEL_PATH
from server_code.application import get_mysql_obj
import pandas as pd
from typing import Union, List, Dict
from server_code.utils import data_utils
from typing import Tuple
from sklearn.preprocessing import MinMaxScaler
import json
from datetime import datetime, timedelta
import os


def get_model_info() -> Union[Dict, List]:
    """
    获取模型信息
    :return:
        OrderedDict or list: 返回封装为OrderedDict的结果，当结果为空时，返回空列表

    by organwalk 2023-08-15
    """
    with open(MODEL_PATH + 'model_info.json', 'r', encoding='utf-8') as file:
        json_data = file.read()
    model_info = json.loads(json_data)
    return res_entity.set_model_info(**model_info) if model_info else []


def get_model_report(model_type: str) -> Union[Dict, List]:
    """
    获取模型报告
    :return:
        OrderedDict or list: 返回封装为OrderedDict的结果，当结果为空时，返回空列表

    by organwalk 2023-10-14
    """
    path = ''
    if model_type == 'SHORTTERM_LSTM':
        path = config.TRAIN_LOG_PATH + 'training_short_lstm_log.txt'
    elif model_type == 'LONGTERM_LSTM':
        path = config.TRAIN_LOG_PATH + 'training_long_lstm_log.txt'
    # 读取文件内容
    data_dict = {}
    with open(path, "r") as file:
        lines = file.readlines()
    # 从文件的最后第二行开始读起
    i = len(lines) - 2
    while i >= 0:
        line = lines[i].strip()
        print(line)
        if line == "-----":
            break
        else:
            key, value = line.split(":", 1)
            data_dict[key] = value.strip()
        i -= 1
    return res_entity.set_model_report(**data_dict) if data_dict else {}


def validate_station_date(station: str, date: str) -> int:
    """
    校验指定气象站下的日期是否存在记录
    :param station: 气象站编号
    :param date: 需要校验的日期
    :return:
        int: 记录数

    by organwalk 2023-08-15
    """
    mysql = get_mysql_obj()
    mysql.execute("select count(id) from station_date where station = %s and date = %s", (station, date))
    return int(mysql.fetchall()[0][0])


def validate_station_date_range(station: str, start_date: str, end_date: str) -> int:
    """
    校验指定气象站下的日期范围是否有七天
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        int: 记录数
    """
    mysql = get_mysql_obj()
    str_sql = "select count(*) from station_date where station = %s and date >= %s and date <= %s"
    mysql.execute(str_sql, (station, start_date, end_date))
    return int(mysql.fetchall()[0][0])


def get_merged_csv_data(station: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取指定气象站点下起止日期连续时间段内合并的CSV数据
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        pd.DataFrame: 包含指定时间范围内CSV数据框

    by organwalk 2023-08-20
    """
    file_prefix = f"{FILE_PATH}{station}_data_"
    file_extension = ".csv"
    data_frames = []
    date_range = pd.date_range(start_date, end_date)

    # 在合并过程中，如果某一日期文件不存在，则采取前向填充手段
    previous_data = None
    for date in date_range:
        file_name = file_prefix + date.strftime("%Y-%m-%d") + file_extension
        try:
            data = pd.read_csv(file_name)
            data_frames.append(data)
            previous_data = data
        except FileNotFoundError:
            if previous_data is not None:
                data_frames.append(previous_data.copy())
    return pd.concat(data_frames) if not date_range.empty else None


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


def get_seven_csv_data(station: str, date: str) -> Tuple[list, MinMaxScaler]:
    start_date = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=-6)).strftime('%Y-%m-%d')
    existing_files = get_csv(station, start_date, date)
    all_data = list()
    scaler = None
    for file in existing_files:
        df = pd.read_csv(file)
        avg_df_data = data_utils.calculate_day_avg(df)
        df_data, scaler = data_utils.get_scaler_result(avg_df_data)
        all_data.append(df_data)
    return all_data, scaler
