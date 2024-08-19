import os
import pandas as pd


# 安全转换函数，避免数据错误导致读取失败
def safe_int(x):
    try:
        return int(x)
    except ValueError:
        return None

# 指定每列的数据类型，以优化读取速度
dtype = {
    'longitude': 'float32',  # 浮点型
    'latitude': 'float32',  # 浮点型
    'cog': 'float32',  # 浮点型
    'heading': 'float32',  # 浮点型
    'speed': 'float32',  # 浮点型
}

converters = {
    'mmsi': safe_int
}

# 指定主目录路径
directory_path = 'data/raw'  # 确保路径正确
output_path = 'data/'  # 合并后的文件路径

# 初始化一个空的DataFrame用于存放合并后的数据
df_combined = pd.DataFrame()

# 遍历所有文件夹和子文件夹
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)

            # 先读取文件头以检查包含的列
            temp_df = pd.read_csv(file_path, nrows=0)
            if 'post_time' in temp_df.columns:
                parse_dates = ['post_time']

                # 读取CSV文件
                df = pd.read_csv(file_path, dtype=dtype, converters=converters, parse_dates=parse_dates,
                                 low_memory=False)
                # 根据具体情况选择必要的字段进行提取
                df = df[['mmsi', 'longitude', 'latitude', 'cog', 'speed', 'post_time']]
            elif 'ts' in temp_df.columns:
                parse_dates = ['ts']

                # 读取CSV文件
                df = pd.read_csv(file_path, dtype=dtype, converters=converters, parse_dates=parse_dates,
                                 low_memory=False)
                # 根据具体情况选择必要的字段进行提取和重命名
                df = df[['mmsi', 'longitude', 'latitude', 'heading', 'speed', 'ts']]
                df.rename(columns={'ts': 'post_time', 'heading': 'cog'}, inplace=True)

            else:
                print(f"Skipping file {file} as it does not contain 'post_time' or 'ts' columns.")
                continue

            # 合并数据到df_combined中
            df_combined = pd.concat([df_combined, df], ignore_index=True)

            print(f"Processed {file_path}")

# # 将post_time列转换为日期时间格式，并移除多余位数
df_combined['post_time'] = df_combined['post_time'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')

# 保存合并后的数据为Feather格式
df_combined.to_feather(output_path + 'combined_data.feather')
print(f"Combined data saved to {output_path + 'combined_data.feather'}")

# 保存合并后的数据为Pickel格式
df_combined.to_pickle(output_path + 'combined_data.pkl')
print(f"Combined data saved to {output_path + 'combined_data.pkl'}")
