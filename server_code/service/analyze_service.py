"""
    定义数据分析业务
    by organwalk 2023-08-15
"""
from server_code.analyze import meteo_data_analyze
from server_code.repository import repository
from typing import List, Optional


def get_correlation_list(station: str, start_date: str, end_date: str, correlation: str)\
        -> Optional[List[List[float]]]:
    """
    获取计算后的协相关矩阵
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :param correlation: 需要进行相关系数矩阵计算的气象要素
    :return:
        [List[List[float]]] or None: 返回计算结果二维数组，如果计算失败则返回None

    by organwalk 2023-08-20
    """
    merged_data = repository.get_merged_csv_data(station, start_date, end_date)
    if merged_data is None:
        return None
    return meteo_data_analyze.calculate_correlation_matrix(correlation, merged_data)
