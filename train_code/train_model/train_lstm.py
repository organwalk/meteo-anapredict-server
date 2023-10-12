"""
    定义了训练长、短期LSTM模型的函数
    by organwalk 2023-10-09
"""
from keras.models import Sequential
from keras.layers import LSTM, Dense, RepeatVector, TimeDistributed, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from typing import List


n_features = 8  # 气象数据特征值
model = Sequential()  # 创建模型对象


def build_short_term_model(input_seq: np.ndarray, output_seq: np.ndarray,
                           val_input_seq: np.ndarray, val_output_seq: np.ndarray) -> Sequential:
    """
    构建并训练LSTM短期模型
    :param input_seq: 训练集的输入序列
    :param output_seq: 训练集的输出序列
    :param val_input_seq: 验证集的输入序列
    :param val_output_seq: 验证集的输出序列
    :return:
        Sequential: LSTM短期模型容器对象

    by organwalk 2023-10-09
    """

    # 0. 定义时间步长
    time_step = 24

    # 1. 构建模型
    # 1.1 LSTM层 -> 500个LSTM单元
    model.add(LSTM(500, activation='relu', input_shape=(time_step, n_features)))
    # 1.2 Droput正则化，减少过拟合风险
    model.add(Dropout(0.5))
    # 1.3 为每一个时间步创建一个预测
    model.add(RepeatVector(time_step))
    # 1.4 LSTM层 -> 500个LSTM单元，返回完整序列
    model.add(LSTM(200, activation='relu', return_sequences=True))
    # 1.5 在每个时间步上应用一个全连接层，输出特征数量的预测
    model.add(TimeDistributed(Dense(n_features)))
    # 1.6 编译模型，指定常规优化器和损失函数
    model.compile(optimizer='adam', loss='mse')
    # 1.7 提前停止 -> 监控验证集损失，等待数个epoch以观察是否有改善
    early_stopping = EarlyStopping(monitor='val_loss', patience=10)
    model.fit(input_seq, output_seq, epochs=1000, verbose=1,
              validation_data=(val_input_seq, val_output_seq), callbacks=[early_stopping])

    return model


def build_long_term_model(input_seq: np.ndarray, output_seq: np.ndarray) -> Sequential:
    # 0. 定义时间步长
    n_steps_in, n_steps_out = 7, 7
    model.add(LSTM(500, activation='relu', input_shape=(n_steps_in, n_features)))
    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(500, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(n_features)))

    model.compile(optimizer='adam', loss='mse')
    model.fit(input_seq, output_seq, epochs=5, verbose=1)
    return model


def get_short_predict(train_model: Sequential, df_data: pd.DataFrame, scaler: MinMaxScaler) -> List[List[float]]:
    """
    获取LSTM短期模型的预测结果
    :param train_model: 训练后LSTM短期模型对象
    :param df_data: 被预测数据
    :param scaler: 解归一化缩放器
    :return:
        List[List[float]]: 浮点数类型二维数组化的预测结果

    by organwalk 2023-10-09
    """

    # 0. 根据时间步长、特征值划分numpy数组为输入序列
    time_step = 24
    input_data = np.array([df_data])
    x_input = input_data.reshape((1, time_step, n_features))
    # 1. 使用模型获取预测结果
    output_data = train_model.predict(x_input, verbose=1)[0]
    # 2. 获得解归一化的预测结果
    non_scaler_output = scaler.inverse_transform(output_data).reshape((time_step, n_features))
    # 3. 保留预测结果小数点后两位，二维数组化的预测结果
    predict_result = np.round(non_scaler_output).round(2).tolist()

    return predict_result


def get_long_predict(train_model: Sequential, data_list: list, scaler: MinMaxScaler) -> List[List[float]]:
    # 0. 根据时间步长、特征值划分numpy数组为输入序列
    time_step = 7
    print(data_list)
    x_input = np.reshape([np.array(a[0]) for a in data_list], (1, time_step, n_features))
    # 1. 使用模型获取预测结果
    output_data = train_model.predict(x_input, verbose=1)[0]
    # 2. 获得解归一化的预测结果
    non_scaler_output = scaler.inverse_transform(output_data).reshape((time_step, n_features))
    # 3. 保留预测结果小数点后两位，二维数组化的预测结果
    predict_result = np.round(non_scaler_output).round(2).tolist()

    return predict_result
