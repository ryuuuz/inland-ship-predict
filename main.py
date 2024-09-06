import pandas as pd

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。

pkl_file_path = 'data/combined_data.pkl'
hdf_file_path = 'data/combined_data.h5'

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

    # 读取整个 pkl 文件
    df = pd.read_pickle(pkl_file_path)

    # 将其保存为 hdf5 格式
    df.to_hdf(hdf_file_path, key='data', mode='w')

    # 查看数据
    print(df.head())

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
