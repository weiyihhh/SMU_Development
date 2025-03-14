import csv
import os
from datetime import datetime

# 假设 measurement_manager.measurements_data 是你已经获取到的列表

def csv_make(measurements_data, save_path, file_name=None):
    # 如果没有提供文件名，自动生成一个文件名
    if file_name is None:
        file_name = f"smu_test_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    # 确保文件名以 .csv 结尾
    if not file_name.endswith('.csv'):
        file_name += '.csv'

    # 拼接文件路径和文件名
    csv_file_path = os.path.join(save_path, file_name)

    # 确保文件路径存在，若不存在则创建文件夹
    directory = os.path.dirname(csv_file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # 打开文件进行写入
    with open(csv_file_path, mode='w', newline='') as file:
        # 创建一个 CSV writer 对象
        writer = csv.DictWriter(file, fieldnames=measurements_data[0].keys())

        # 写入表头
        writer.writeheader()

        # 写入数据
        for measurement in measurements_data:
            writer.writerow(measurement)

    print(f"CSV 文件已保存至 {csv_file_path}")
