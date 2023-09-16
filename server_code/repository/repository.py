from server_code.entity import res_entity
from server_code.config.application import get_mysql_obj
from server_code.config.application import FILE_PATH
import server_code.repository.mysql_statements as mysql_statements
import pandas as pd
from typing import Union, List, Dict


def get_model_info() -> Union[Dict, List]:
    """
    获取模型信息

    :return:
        OrderedDict or list: 返回封装为OrderedDict的结果，当结果为空时，返回空列表

    by organwalk 2023-08-15
    """
    mysql = get_mysql_obj()
    mysql.execute(mysql_statements.NEW_MODEL_INFO)
    result = mysql.fetchall()[0][1:7]
    return res_entity.set_model_info(*result) if result else []


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
    mysql.execute(mysql_statements.VALID_DATE, (station, date))
    return int(mysql.fetchall()[0][0])


def get_merged_csv_data(station: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取指定气象站点下起止日期连续时间段内的CSV数据

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
