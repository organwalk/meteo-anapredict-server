"""
    定义配置信息
    by organwalk 2023-08-15
"""
FILE_PATH = "../meteo_data_csv/"  # 数据集文件路径
MODEL_PATH = "../meteo_model/"  # 模型文件路径
TRAIN_LOG_PATH = "../train_log/"  # 模型训练日志路径

SHORT_TERM_MODEL_LIST = [
    'SHORTTERM_LSTM',
    'SHORTTERM_ARIMA',
    'SHORTTERM_PROPHET',
    'SHORTTERM_MIXED'
]  # 短期（24小时）模型列表

LONG_TERM_MODEL_LIST = [
    'LONGTERM_LSTM',
    'LONGTERM_ARIMA',
    'LONGTERM_PROPHET',
    'LONGTERM_MIXED'
]  # 长期（七日）模型列表
