"""
    定义获取LSTM长短期模型预测结果的函数
    by organwalk 2023-09-18
"""
from server_code.repository import repository
from tensorflow.keras.models import load_model
from config import MODEL_PATH
import numpy as np
from typing import List


def get_short_term_predict(station: str, date: str) -> List[List[int]]:
    """
    获取LSTM短期模型的预测结果
    :param station: 气象站编号
    :param date: 日期
    :return:
        List[List[float]] or None: 返回值为二维数组的预测结果，无结果时返回None

    by organwalk 2023-09-17
    """
    time_step = 24
    feature = 8
    # 0. 获取归一化后的数据，及解归一化使用的scaler对象
    df_data, scaler = repository.get_one_csv_data(station, date)
    # 1. 加载模型
    model = load_model(f'{MODEL_PATH}/short_lstm.h5')
    # 2. 获取预测数据
    # 2.1 将输入数据窗转为numpy数组
    input_data = np.array([df_data])
    # 2.2 根据时间步长、特征值划分numpy数组为输入序列
    x_input = input_data.reshape((1, time_step, feature))
    # 2.3 使用模型获取预测结果
    output_data = model.predict(x_input, verbose=0)[0]
    # 2.4 将预测结果解归一化
    non_scaler_output = scaler.inverse_transform(output_data).reshape((time_step, feature))
    # 2.5 保留预测结果小数点后两位，二维数组化的预测结果
    predict_result = np.round(non_scaler_output).round(2).tolist()
    return predict_result


def get_long_term_predict(station: str, date: str) -> List[List[int]]:
    model = load_model(f'{MODEL_PATH}/long_lstm.h5')
    data_list, scaler = repository.get_seven_csv_data(station=station, date=date)
    # 0. 根据时间步长、特征值划分numpy数组为输入序列
    time_step = 7
    n_features = 8
    x_input = np.reshape([np.array(a[0]) for a in data_list], (1, time_step, n_features))
    # 1. 使用模型获取预测结果
    output_data = model.predict(x_input, verbose=1)[0]
    # 2. 获得解归一化的预测结果
    non_scaler_output = scaler.inverse_transform(output_data).reshape((time_step, n_features))
    # 3. 保留预测结果小数点后两位，二维数组化的预测结果
    predict_result = np.round(non_scaler_output).round(2).tolist()

    return predict_result
