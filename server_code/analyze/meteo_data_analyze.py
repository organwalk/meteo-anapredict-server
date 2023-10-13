"""
    定义数据分析的各类方法
    by organwalk 2023-08-20
"""
import pandas as pd
from typing import List, Optional


def calculate_correlation_matrix(elements: str, merged_data: pd.DataFrame) -> Optional[List]:
    """
    计算协相关矩阵
    :param elements: 需要进行计算的气象要素
    :param merged_data: 连续时间段CSV合并数据
    :return:
        list or None: 协相关矩阵的二维数组, 计算结果为空时返回None

    by organwalk 2023-08-20
    """
    elements_map = {
        '1': 'Temperature',
        '2': 'Humidity',
        '3': 'Speed',
        '4': 'Direction',
        '5': 'Rain',
        '6': 'Sunlight',
        '7': 'PM2.5',
        '8': 'PM10'
    }
    selected_columns = [elements_map[element] for element in elements.split(',')]
    selected_data = merged_data[selected_columns]
    correlation_matrix = selected_data.corr()

    # 替换NaN值为0，保留两位小数，将相关系数矩阵转换为二维数组
    return list(correlation_matrix.fillna(0).round(2).values.tolist()) if not correlation_matrix.empty else None
