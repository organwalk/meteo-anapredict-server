"""
    定义获取数据源的方法
    by organwalk 2023-09-19
"""
from typing import Union, List
from server_code.config.application import FILE_PATH
from datetime import datetime, timedelta
import os


def get_csv(station: str, start_date: str, end_date: str) -> Union[List[str], str]:
    """
    获取有效csv数据集文件路径列表
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        List[str] or AnyStr: 返回csv数据集文件路径列表，无法前向填充时返回错误消息
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


# print(get_csv('1', '2023-07-28', '2023-08-03'))
