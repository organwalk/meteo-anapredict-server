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
        # 检查是否需要前向填充
        _missing_data_fill(station, current_date.strftime("%Y-%m-%d"))
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
    path = f'{FILE_PATH}{station}/{station}_data_{date}.csv'
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
        for index, row in data.iterrows():
            if index != 0:
                file.write('\n')  # 写入换行符
            file.write(','.join(map(str, row)))


def _missing_data_fill(station: str, date: str):
    """
    检查数据集在24小时内每小时是否都具有记录，若连续时间段内存在小时数据缺失，则前向填充一条记录
    :param station: 气象站编号
    :param date: 日期
    :return:
        None: 直到填充完成为止

    by organwalk
    """
    path = f'{FILE_PATH}{station}/{station}_data_{date}.csv'
    df = pd.read_csv(path, index_col='Time')
    # 将索引转换为datetime格式，方便后续处理
    df.index = pd.to_datetime(df.index)
    # 检查是否有24个不同的小时值
    if len(df.index.hour.unique()) != 24:
        # 创建一个空的DataFrame，用于存储补全后的数据
        new_df = pd.DataFrame()
        # 遍历24个小时，每个小时为一个循环
        for hour in range(24):
            # 获取当前小时的数据
            hour_df = df[df.index.hour == hour]
            # 如果当前小时没有数据
            if hour_df.empty:
                # 获取前一个小时的最后一行数据
                last_row = new_df.iloc[-1]
                # 将最后一行数据的时间索引修改为当前小时的最后一分钟
                last_row.name = last_row.name.replace(hour=hour, minute=59)
                # 将修改后的数据添加到新的DataFrame中
                new_df = new_df.append(last_row)
            # 如果当前小时有数据
            else:
                # 将当前小时的数据添加到新的DataFrame中
                new_df = new_df.append(hour_df)
        # 重置索引，将Time列恢复为普通列
        new_df = new_df.reset_index()
        # 将Time列的格式转换为hh:MM:SS
        new_df['Time'] = new_df['Time'].dt.strftime('%H:%M:%S')
        # 输出新的csv文件，包含Time列
        new_df.to_csv(path, index=False)
