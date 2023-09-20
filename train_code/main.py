from train_model import train_lstm
from utils.lstm import pre_process as pre_lstm
from repository import repository


def train_lstm_short_term():
    input_seq, output_seq, scaler = pre_lstm.split_short_term_sequences('1', '2023-06-27', '2023-07-04')
    model = train_lstm.build_short_term_model(input_seq, output_seq)
    df_data, scaler = repository.get_one_csv_data('1', '2023-07-21')
    predict_result = train_lstm.get_short_term_result(model, df_data, scaler)
    print(predict_result)


train_lstm_short_term()