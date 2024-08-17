import pandas as pd
import os
import matplotlib.pyplot as plt
import random


def preprocess_and_filter_data(directory_path):
    """
    读取CSV文件并合并数据，然后通过四分位数计算经纬度范围，排除不在范围内的数据点。

    Parameters:
        directory_path (str): CSV文件所在的目录路径。

    Returns:
        pd.DataFrame: 经过过滤后的数据。
    """
    # 获取目录下所有CSV文件的列表
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

    # 提前指定每列的数据类型，以避免pandas自动推断数据类型时消耗的时间。
    dtype = {
        'post_time': 'str',  # 字符串
        'ts': 'str',  # 字符串
        'mmsi': 'int64',  # 整型
        'longitude': 'float32',  # 浮点型
        'latitude': 'float32',  # 浮点型
        'cog': 'float32',  # 浮点型
        'heading': 'float32',  # 浮点型
        'speed': 'float32',  # 浮点型
        'status': 'float32',  # 浮点型
        'cyclic_velocity': 'float32',  # 浮点型
        'position_acc': 'float32'  # 浮点型
    }

    # 初始化一个空的DataFrame用于存放合并后的数据
    df_combined = pd.DataFrame()

    # 逐个读取CSV文件并合并到df_combined中
    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path, low_memory=False)

        # 根据具体情况，选择必要的字段进行提取和重命名
        if 'post_time' in df.columns:
            df = df[['mmsi', 'longitude', 'latitude', 'cog', 'speed', 'post_time']]
        elif 'ts' in df.columns:
            df = df[['mmsi', 'longitude', 'latitude', 'heading', 'speed', 'ts']]
            df.rename(columns={'ts': 'post_time', 'heading': 'cog'}, inplace=True)

        # 将当前文件的数据追加到合并的DataFrame中
        df_combined = pd.concat([df_combined, df])

    # 将时间字段统一为Datetime格式
    df_combined['post_time'] = pd.to_datetime(df_combined['post_time'])

    # 计算经度和纬度的四分位数范围
    longitude_q1 = df_combined['longitude'].quantile(0.25)
    longitude_q3 = df_combined['longitude'].quantile(0.75)
    latitude_q1 = df_combined['latitude'].quantile(0.25)
    latitude_q3 = df_combined['latitude'].quantile(0.75)

    # 过滤掉不在四分位数范围内的点
    df_filtered = df_combined[
        (df_combined['longitude'] >= longitude_q1) &
        (df_combined['longitude'] <= longitude_q3) &
        (df_combined['latitude'] >= latitude_q1) &
        (df_combined['latitude'] <= latitude_q3)
        ]

    return df_filtered


def visualize_sampled_data(df, num_samples=100):
    """
    随机抽取若干个mmsi的数据并进行可视化。

    Parameters:
        df (pd.DataFrame): 经过滤后的数据。
        num_samples (int): 要抽取的mmsi数量。
    """
    # 获取所有唯一的mmsi
    unique_mmsi = df['mmsi'].unique()

    # 随机抽取mmsi
    sampled_mmsi = random.sample(list(unique_mmsi), num_samples)

    # 过滤出抽取的mmsi对应的数据
    df_sampled = df[df['mmsi'].isin(sampled_mmsi)]

    # 绘制每个抽取的船舶轨迹
    plt.figure(figsize=(10, 8))

    for mmsi, group in df_sampled.groupby('mmsi'):
        plt.plot(group['longitude'], group['latitude'], marker='o', label=f'Ship {mmsi}')

    plt.title(f'Ship Trajectories (Sampled {num_samples} MMSI)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()


# 使用示例
directory_path = "data/raw/1. cq_tlx_device_1 export/1. cq_tlx_device_1 export"
df_filtered = preprocess_and_filter_data(directory_path)
visualize_sampled_data(df_filtered)
