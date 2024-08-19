import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import nearest_points
from shapely.strtree import STRtree
import numpy as np
from tqdm import tqdm


# 1. 读取整个PKL文件
def read_pkl_file(file_path):
    return pd.read_pickle(file_path)


# 2. 计算经纬度的四分位数范围，并进行初步过滤
def filter_by_quartiles(df):
    lon_quartiles = df['longitude'].quantile([0.25, 0.75])
    lat_quartiles = df['latitude'].quantile([0.25, 0.75])
    filtered = df[(df['longitude'] >= lon_quartiles[0.25]) & (df['longitude'] <= lon_quartiles[0.75]) &
                  (df['latitude'] >= lat_quartiles[0.25]) & (df['latitude'] <= lat_quartiles[0.75])]
    return filtered


# 3. 读取GeoJSON文件并建立空间索引
def read_geojson_file_with_spatial_index(file_path):
    geo_df = gpd.read_file(file_path)
    spatial_index = STRtree(geo_df.geometry)
    return geo_df, spatial_index


# 4. 计算点到最近几何对象的距离
def calculate_nearest_distance_with_index(df, geo_df, spatial_index):
    points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    points = points.set_crs(geo_df.crs, allow_override=True)  # Ensure the CRS matches

    def nearest_distance(point):
        nearest_geoms = spatial_index.query(point)
        if len(nearest_geoms) > 0:
            actual_geom = geo_df.geometry.iloc[nearest_geoms[0]]  # 根据索引取得几何对象
            return point.distance(actual_geom)  # 计算距离
        else:
            return np.nan  # 如果没有找到相应的几何对象，返回 NaN

    distances = np.array([nearest_distance(point) for point in points.geometry])
    df.loc[:, 'nearest_distance'] = distances  # 使用 .loc 显式指定修改操作
    return df


# 5. 根据指定距离范围进一步过滤数据
def filter_by_distance(df, max_distance):
    filtered_df = df[df['nearest_distance'] <= max_distance].dropna(subset=['nearest_distance'])
    return filtered_df


# 主函数
from tqdm import tqdm  # 导入 tqdm


def process_data(pkl_file_path, geojson_file_path, max_distance, chunksize=100000):
    geo_df, spatial_index = read_geojson_file_with_spatial_index(geojson_file_path)

    # 读取整个PKL文件
    df = read_pkl_file(pkl_file_path)

    # 分块处理数据
    num_chunks = len(df) // chunksize + 1
    filtered_chunks = []

    # 使用 tqdm 包装循环以显示进度条
    for i in tqdm(range(num_chunks), desc="Processing chunks"):
        chunk = df[i * chunksize:(i + 1) * chunksize]
        filtered_chunk = filter_by_quartiles(chunk)
        # filtered_chunk = calculate_nearest_distance_with_index(filtered_chunk, geo_df, spatial_index)
        # filtered_chunk = filter_by_distance(filtered_chunk, max_distance)
        filtered_chunks.append(filtered_chunk)

    # 合并所有处理过的分块
    final_df = pd.concat(filtered_chunks, ignore_index=True)
    return final_df


# 调用函数
pkl_file_path = 'data/combined_data.pkl'
geojson_file_path = 'data/geojson/500000.geojson'
max_distance = 100  # 例如 100 米以内
output_path = 'data/filtered_data.pkl'

filtered_data = process_data(pkl_file_path, geojson_file_path, max_distance)
print(filtered_data.head())

filtered_data.to_pickle(output_path)
print(f"Filtered data saved to {output_path}")
