"""
    训练模型的执行代码主程序模块
    by organwalk 2023-10-09
"""
from train_model import train_lstm
from utils.lstm import pre_process as pre_lstm
from repository import repository


def train_lstm_short_term():
    """
    此函数定义了训练短期LSTM模型的执行代码
    :return: None

    by organwalk 2023-10-09
    """

    # 1. 针对训练集和验证集划分输入序列和输出序列
    input_seq, output_seq, scaler = \
        pre_lstm.split_short_term_sequences(station='1', start_date='2023-06-27', end_date='2023-07-15')
    val_input_seq, val_output_seq, val_scaler = \
        pre_lstm.split_short_term_sequences(station='1', start_date='2023-07-16', end_date='2023-07-25')

    # 2. 构建并训练模型
    model = train_lstm.build_short_term_model(input_seq=input_seq, output_seq=output_seq,
                                              val_input_seq=val_input_seq, val_output_seq=val_output_seq)

    # 3. 获取被预测数据
    df_data, scaler = repository.get_one_csv_data(station='1', date='2023-07-26')

    # 4. 代入构建的训练模型与被预测数据，进行数据预测
    predict_result = train_lstm.get_short_term_result(model=model, df_data=df_data, scaler=scaler)
    print(predict_result)


train_lstm_short_term()