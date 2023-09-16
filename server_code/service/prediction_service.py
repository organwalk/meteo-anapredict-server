"""
    定义模型预测业务
    by organwalk 2023-08-20
"""
from typing import List, Optional


def predict_by_model(station: str, start_date: str, end_date: str, model_type: str) \
        -> Optional[List[List[float]]]:
    """
    根据model_type使用指定的模型进行预测

    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 截止日期
    :param model_type: 模型类型
    :return:
        List[List[float]] or None: 返回值为二维数组的预测结果，无结果时返回None

    by organwalk 2023-08-20
    """
    if model_type == 'SHORTTERM_LSTM':
        return _get_lstm_short_term(station, start_date, end_date)


def _get_lstm_short_term(station: str, start_date: str, end_date: str):
    print(123)