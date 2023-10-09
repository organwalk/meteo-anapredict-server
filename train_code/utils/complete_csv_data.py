import csv
from datetime import datetime, timedelta
import server_code.config.application as config
input_file = config.FILE_PATH + '1_data_2023-07-03.csv'
output_file = config.FILE_PATH + 'output.csv'

# 读取CSV文件
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# 获取最后一行的时间
last_row = rows[-1]
last_time_str = last_row['Time']
last_time = datetime.strptime(last_time_str, '%H:%M:%S')

# 创建新的数据行，直到23:59:00为止
end_time = datetime.strptime('23:59:00', '%H:%M:%S')
current_time = last_time + timedelta(minutes=1)

while current_time <= end_time:
    new_row = {}

    # 复制最后一行的数据
    for key, value in last_row.items():
        if key == 'Time':
            # 更新时间字段
            new_row[key] = current_time.strftime('%H:%M:%S')
        else:
            new_row[key] = value

    rows.append(new_row)
    current_time += timedelta(minutes=1)

# 写入CSV文件
with open(output_file, 'w', newline='') as file:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("数据复制完成，已保存到", output_file)