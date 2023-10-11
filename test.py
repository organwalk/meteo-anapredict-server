import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense


# 读取数据集文件夹
data_folder = "C:/Users/haruki/PycharmProjects/meteo-anapredict-server/meteo_data_csv/"
file_dates = pd.date_range(start="2023-06-27", end="2023-07-28", freq="D")

# 读取数据文件并合并
data = pd.DataFrame()
for date in file_dates:
    file_name = data_folder + "1_data_" + date.strftime("%Y-%m-%d") + ".csv"
    df = pd.read_csv(file_name)
    data = pd.concat([data, df], ignore_index=True)

# 提取每日平均数据
data['Time'] = pd.to_datetime(data['Time'])
data['Date'] = data['Time'].dt.date
daily_avg_data = data.groupby('Date').mean()

# 构建训练数据和目标数据
train_data = daily_avg_data.iloc[:-7, :]
target_data = daily_avg_data.iloc[7:, :]

# 数据预处理
train_data = (train_data - train_data.mean()) / train_data.std()
target_data = (target_data - target_data.mean()) / target_data.std()

# 转换为LSTM可用的输入格式
train_input = np.array(train_data).reshape(-1, 1, train_data.shape[1])
target_input = np.array(target_data).reshape(-1, 1, target_data.shape[1])

# 构建LSTM模型
model = Sequential()
model.add(LSTM(64, input_shape=(1, train_data.shape[1])))
model.add(Dense(target_data.shape[1]))

# 编译模型
model.compile(loss='mean_squared_error', optimizer='adam')

# 训练模型
model.fit(train_input, target_input, epochs=100, batch_size=32)

# 预测未来七日气象数据每日平均数据
last_day_data = np.array(train_data.iloc[-1, :]).reshape(1, 1, train_data.shape[1])
predictions = []
for _ in range(7):
    prediction = model.predict(last_day_data)
    predictions.append(prediction[0])
    last_day_data = np.concatenate((last_day_data[:, 1:, :], prediction.reshape(1, 1, target_data.shape[1])), axis=1)

# 将预测结果转为DataFrame格式
prediction_data = pd.DataFrame(predictions, columns=daily_avg_data.columns)

# 输出预测结果
print(prediction_data)