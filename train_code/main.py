"""
    训练模型的执行代码主程序模块
    by organwalk 2023-10-09
"""
from train_model import train_lstm, evaluate_model as evalu
from utils.lstm import pre_process as pre_lstm
from repository import repository


def train_lstm_short_term():
    """
    此函数定义了训练短期LSTM模型的执行代码
    :return: None

    by organwalk 2023-10-09
    """

    # 0. 针对训练集和验证集划分输入序列和输出序列
    input_seq, output_seq, scaler = pre_lstm.split_short_term_sequences(station='1',
                                                                        start_date='2023-06-27',
                                                                        end_date='2023-07-15')
    val_input_seq, val_output_seq, val_scaler = pre_lstm.split_short_term_sequences(station='1',
                                                                                    start_date='2023-07-16',
                                                                                    end_date='2023-07-25')
    # 1. 构建并训练模型
    model = train_lstm.build_short_term_model(input_seq=input_seq,
                                              output_seq=output_seq,
                                              val_input_seq=val_input_seq,
                                              val_output_seq=val_output_seq)
    # 2. 获取被预测数据
    df_data, scaler = repository.get_one_csv_data(station='1', date='2023-07-26')
    # 3. 代入构建的训练模型与被预测数据，进行数据预测
    predict_result = train_lstm.get_short_predict(train_model=model, df_data=df_data, scaler=scaler)

    # 4. 评估模型
    nonscaler_val_seq = repository.get_one_csv_data_tolist(station='1', date='2023-07-27')
    # 4.1 均方误差
    evalu.get_rmse(pred_result=predict_result, val_seq=nonscaler_val_seq)
    # 4.2 平均绝对误差
    evalu.get_mae(pred_result=predict_result, val_seq=nonscaler_val_seq)
    # 4.3 决定系数
    evalu.get_r2score(pred_result=predict_result, val_seq=nonscaler_val_seq)
    # 4.4 模型复杂度
    comp_train_input, comp_train_output, _ = pre_lstm.split_short_term_sequences(station='1',
                                                                                 start_date='2023-06-27',
                                                                                 end_date='2023-06-28')
    comp_val_input, comp_val_output, _ = pre_lstm.split_short_term_sequences(station='1',
                                                                             start_date='2023-07-16',
                                                                             end_date='2023-07-17')
    evalu.get_complex(model=model,
                      train_input=comp_train_input,
                      train_output=comp_train_output,
                      val_input=comp_val_input,
                      val_output=comp_val_output)
    # 4.5 验证集与预测结果比较图表
    evalu.chart_compared(pred_result=predict_result, val_seq=nonscaler_val_seq)


def train_lstm_long_term():
    input_seq, output_seq, scaler = pre_lstm.split_long_term_sequences(station='1',
                                                                       start_date='2023-06-27',
                                                                       end_date='2023-07-20')
    # 1. 构建并训练模型
    model = train_lstm.build_long_term_model(input_seq=input_seq, output_seq=output_seq)
    # 2. 获取被预测数据
    data_list, scaler = repository.get_seven_csv_data(station='1', date='2023-07-21')
    # 3. 代入构建的训练模型与被预测数据，进行数据预测
    predict_result = train_lstm.get_long_predict(train_model=model, data_list=data_list, scaler=scaler)
    print(predict_result)
    # # 4. 评估模型
    # nonscaler_val_seq = repository.get_one_csv_data_tolist(station='1', date='2023-07-27')
    # # 4.1 均方误差
    # evalu.get_rmse(pred_result=predict_result, val_seq=nonscaler_val_seq)
    # # 4.2 平均绝对误差
    # evalu.get_mae(pred_result=predict_result, val_seq=nonscaler_val_seq)
    # # 4.3 决定系数
    # evalu.get_r2score(pred_result=predict_result, val_seq=nonscaler_val_seq)
    # # 4.4 模型复杂度
    # comp_train_input, comp_train_output, _ = pre_lstm.split_short_term_sequences(station='1',
    #                                                                              start_date='2023-06-27',
    #                                                                              end_date='2023-06-28')
    # comp_val_input, comp_val_output, _ = pre_lstm.split_short_term_sequences(station='1',
    #                                                                          start_date='2023-07-16',
    #                                                                          end_date='2023-07-17')
    # evalu.get_complex(model=model,
    #                   train_input=comp_train_input,
    #                   train_output=comp_train_output,
    #                   val_input=comp_val_input,
    #                   val_output=comp_val_output)
    # # 4.5 验证集与预测结果比较图表
    # evalu.chart_compared(pred_result=predict_result, val_seq=nonscaler_val_seq)


train_lstm_long_term()
