"""
    定义模型的评估方法
    by organwalk 2023.10.09
"""
from keras.models import Sequential
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import List
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime


def get_rmse(pred_result: List[List[float]], val_seq: List[List[float]]):
    """
    获取均方根误差：
        0.RMSE是一种常用的回归问题性能指标，用于衡量模型的预测值与真实值之间的差异；
        1.RMSE越低，表示模型的预测越接近真实值。
    :param pred_result: 模型预测结果
    :param val_seq: 验证集序列
    :return: None

    by organwalk 2023.10.09
    """
    rmse = np.sqrt(mean_squared_error(val_seq, pred_result))
    print(f"-->均方根误差:{rmse}")
    _write_to_log(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    _write_to_log("rmse:" + str(rmse))


def get_mae(pred_result: List[List[float]], val_seq: List[List[float]]):
    """
    获取平均绝对误差：
        0.MAE是另一种常用的回归问题性能指标，它衡量模型的预测值与真实值之间的绝对差异的平均值；
        1.较低的MAE值表示模型的预测误差较小。
    :param pred_result: 模型预测结果
    :param val_seq: 验证集序列
    :return: None

    by organwalk 2023.10.09
    """
    mae = mean_absolute_error(val_seq, pred_result)
    print(f"-->平均绝对误差:{mae}")
    _write_to_log("mae:" + str(mae))


def get_r2score(pred_result: List[List[float]], val_seq: List[List[float]]):
    """
    获取决定系数：
        0.R-squared用于衡量模型对目标变量的解释能力，取值范围从0到1；
        1.较高的R-squared值表示模型能够较好地解释目标变量的方差。
    :param pred_result: 模型预测结果
    :param val_seq: 验证集序列
    :return: None

    by organwalk 2023.10.09
    """
    r2 = r2_score(val_seq, pred_result)
    print(f"-->决定系数:{r2}")
    _write_to_log("r2:" + str(r2))


def get_complex(model: Sequential, train_input: np.ndarray, train_output: np.ndarray,
                val_input: np.ndarray, val_output: np.ndarray):
    """
    获取训练集和验证集的损失函数，评估模型复杂度和拟合程度
    :param model: 训练后LSTM短期模型对象
    :param train_input: 训练集输入序列
    :param train_output: 训练集输出序列
    :param val_input: 验证集输入序列
    :param val_output: 验证集输出序列
    :return: None

    by organwalk 2023.10.09
    """
    train_loss = model.evaluate(train_input, train_output)
    val_loss = model.evaluate(val_input, val_output)

    print(f"-->训练集损失函数值:{train_loss}")
    print(f"-->验证集损失函数值:{val_loss}")
    _write_to_log("train_loss:" + str(train_loss))
    _write_to_log("val_loss:" + str(val_loss))
    _write_to_log("-" * 5)
    log_file.close()


def chart_compared(pred_result: List[List[float]], val_seq: List[List[float]]):
    """
    绘制图表对比验证集与预测结果差异
    :param pred_result: 模型预测结果
    :param val_seq: 验证集序列
    :return: None

    by organwalk 2023.10.09
    """
    num_features = len(pred_result[0])
    labels = ['Temperature', 'Humidity', 'Speed', 'Direction', 'Rain', 'Sunlight', 'PM2.5', 'PM10']
    scaler = MinMaxScaler()
    plt.figure(figsize=(19.20, 10.80))

    for i in range(num_features):
        true_vals = scaler.fit_transform(np.array([x[i] for x in val_seq]).reshape(-1, 1))
        pred_vals = scaler.transform(np.array([x[i] for x in pred_result]).reshape(-1, 1))

        plt.subplot(num_features, 1, i + 1)
        plt.plot(true_vals, label="True")
        plt.plot(pred_vals, label="Predicted")
        plt.legend()
        plt.ylabel(labels[i])

    plt.xlabel('Time')
    plt.tight_layout()
    plt.show()


log_file = open("C:/Users/haruki/PycharmProjects/meteo-anapredict-server/train_code/train_model/log/training_short_lstm_log.txt", "a")


def _write_to_log(message):
    log_file.write(str(message) + "\n")

