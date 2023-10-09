from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
import numpy as np


def build_short_term_model(input_seq, output_seq):
    n_steps_in = 24
    n_steps_out = 24
    n_features = 8
    model = Sequential()
    model.add(LSTM(500, activation='relu', input_shape=(n_steps_in, n_features)))
    model.add(RepeatVector(n_steps_out))
    model.add(LSTM(500, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(n_features)))

    model.compile(optimizer='adam', loss='mse')
    model.fit(input_seq, output_seq, epochs=1000, verbose=1)

    return model


def get_short_term_result(model, df_data, scaler):
    time_step = 24
    feature = 8
    input_data = np.array([df_data])
    # 0.根据时间步长、特征值划分numpy数组为输入序列
    x_input = input_data.reshape((1, time_step, feature))
    # 1.使用模型获取预测结果
    output_data = model.predict(x_input, verbose=1)
    print(output_data)
    # 2.保留小数点后两位预测结果
    int_output_data = np.round(output_data).round(2)
    # 3.根据时间步长、特征值重塑数组形状，其中每个元素都被限制在0及以上
    reshape_int_output_data = np.clip(int_output_data, a_min=0, a_max=None).reshape((time_step, feature))
    # 4.将预测结果解归一化
    non_scaler_output = scaler.inverse_transform(reshape_int_output_data).reshape((time_step, feature))
    # 5.得到最终整数化的预测结果
    predict_result = np.round(non_scaler_output).round(2).tolist()

    return predict_result
