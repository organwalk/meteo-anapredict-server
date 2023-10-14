import pandas as pd
from config import FILE_PATH
import redis
from server_code.application import REDIS_CONFIG
import csv
from datetime import datetime, timedelta


def etl_data(station: str, start_date: str, end_date: str):
    """
    具有抽取、转换和加载的数据清洗方法
    :param station: 气象站编号
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
        None: 直到ETL操作完成为止

    by organwalk 2023-10-14
    """
    r = redis.Redis(**REDIS_CONFIG)
    # 定义起始日期和结束日期
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    # 遍历日期范围
    current_date = start_date
    while current_date <= end_date:
        # 根据日期生成文件名和 Redis 键名
        date_str = current_date.strftime("%Y-%m-%d")
        file_name = f"{FILE_PATH}{station}/{station}_data_{date_str}.csv"
        redis_key = f"{station}_data_{date_str}"
        # 从 Redis 中获取数据
        data = r.zrange(redis_key, 0, -1)
        # 创建 CSV 文件并写入数据
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            # 写入 CSV 文件的列标题
            writer.writerow(
                ['Time', 'Temperature', 'Humidity', 'Speed', 'Direction', 'Rain', 'Sunlight', 'PM2.5', 'PM10'])
            # 将每行数据写入 CSV 文件
            for item in data:
                values = eval(item)
                writer.writerow(values)
        # 清洗处理此文件
        _cleaned_data(station, current_date.strftime("%Y-%m-%d"))
        # 增加一天
        current_date += timedelta(days=1)


def _cleaned_data(station: str, date: str):
    """
    数据清洗核心方法
    :param station: 气象站编号
    :param date: 日期
    :return:
        None: 直到清洗完成为止

    by organwalk 2023-10-14
    """
    # 读取原始csv文件
    path = FILE_PATH + f'{station}/{station}_data_{date}.csv'
    data = pd.read_csv(path)
    # 缺失值处理：直接丢弃含有缺失值的行
    data = data.dropna()
    # 噪音数据处理：基于标准方差进行过滤
    cols = ['Temperature', 'Humidity', 'Speed', 'Direction', 'Rain', 'Sunlight', 'PM2.5', 'PM10']
    for col in cols:
        mean = data[col].mean()
        std = data[col].std()
        threshold = mean + 3 * std
        data = data[data[col] <= threshold]
    # 清空原始数据集文件内容
    with open(path, 'w') as file:
        file.write('')
    # 将内容重写为清洗转换后的数据
    with open(path, 'a') as file:
        file.write(','.join(data.columns) + '\n')
        file.write(data.to_csv(header=False, index=False))

