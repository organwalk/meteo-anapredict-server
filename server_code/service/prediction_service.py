"""
    定义模型预测业务
    by organwalk 2023-08-20
"""
from typing import List, Optional
from server_code.repository import repository
from tensorflow.keras.models import load_model
import numpy as np


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
        return _get_lstm_short_term(station, start_date)


def _get_lstm_short_term(station: str, date: str) -> Optional[List[List[float]]]:
    """
    获取LSTM短期模型的预测结果

    :param station: 气象站编号
    :param date: 日期
    :return:
        List[List[float]] or None: 返回值为二维数组的预测结果，无结果时返回None

    by organwalk 2023-09-17
    """
    # 0.获取归一化后的数据，及解归一化使用的scaler对象
    df_data, scaler = repository.get_one_csv_data(station, date)
    # 1.加载模型
    model = load_model('C:/Users/haruki/PycharmProjects/meteo-anapredict-server/meteo_model/short_term/lstm.h5')
    # 2.获取预测数据
    # 2.1将数据窗转为numpy数组
    input_data = np.array([df_data])
    # 2.2根据时间步长、特征值划分numpy数组
    x_input = input_data.reshape((1, 24, 8))
    # 2.3使用模型获取预测结果
    output_data = model.predict(x_input, verbose=1)
    # 2.4整数化预测结果
    int_output_data = np.round(output_data).astype(int)
    # 2.5
    reshape_int_output_data = np.clip(int_output_data, a_min=0, a_max=None).reshape((24, 8))
    # 2.6将预测结果解归一化
    non_scaler_output = scaler.inverse_transform(reshape_int_output_data).reshape((24, 8))
    # 2.7得到最终整数化的预测结果
    predict_result = np.round(non_scaler_output).astype(int)

    return predict_result if predict_result else None


_get_lstm_short_term('1', '2023-06-27')
