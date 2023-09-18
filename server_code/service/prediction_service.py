"""
    定义模型预测业务
    by organwalk 2023-08-20
"""
from typing import List
from server_code.prediction import model_lstm


def predict_by_model(station: str, start_date: str, end_date: str, model_type: str) \
        -> List[List[int]]:
    """
    根据model_type使用指定的模型进行预测

    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 截止日期
    :param model_type: 模型类型
    :return:
        List[List[int]]: 返回值为二维数组的预测结果

    by organwalk 2023-08-20
    """
    if model_type == 'SHORTTERM_LSTM':
        return model_lstm.get_short_term_predict(station, start_date)
