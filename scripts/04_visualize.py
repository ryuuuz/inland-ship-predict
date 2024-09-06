import os
import pandas as pd
import plotly.graph_objects as go


def plot_trajectories(data, start_date, end_date, start_hour, end_hour):
    # 转换时间
    data['post_time'] = pd.to_datetime(data['post_time'])

    # 筛选日期范围
    mask_date = (data['post_time'].dt.date >= pd.to_datetime(start_date).date()) & \
                (data['post_time'].dt.date <= pd.to_datetime(end_date).date())

    # 筛选时间范围
    mask_time = (data['post_time'].dt.hour >= start_hour) & (data['post_time'].dt.hour <= end_hour)

    # 应用筛选
    filtered_data = data[mask_date & mask_time]

    # 检查每个轨迹段的开始和结束时间是否在选择的时间段内
    segments_to_plot = filtered_data.groupby(['mmsi', 'segment_id']).filter(
        lambda x: (x['post_time'].min().hour <= end_hour and x['post_time'].max().hour >= start_hour))

    # 设置地图
    fig = go.Figure()

    # 为每个轨迹段绘制线段
    for (mmsi, segment_id), segment_data in segments_to_plot.groupby(['mmsi', 'segment_id']):
        # 创建悬停文本
        hover_text = [
            f"MMSI: {mmsi:.0f}<br>Lat: {lat:.6f}, Lon: {lon:.6f}<br>Time: {time}<br>Speed: {speed} knots"
            for lat, lon, time, speed in
            zip(segment_data['latitude'], segment_data['longitude'], segment_data['post_time'], segment_data['speed'])
        ]

        fig.add_trace(go.Scattermap(
            lon=segment_data['longitude'],
            lat=segment_data['latitude'],
            mode='lines+markers',
            marker={'size': 5},
            line={'width': 2},
            name=f'{segment_id}',
            text=hover_text,  # 设置悬停文本
            hoverinfo='text+name'  # 指定显示自定义文本
        ))

    # 设置地图布局
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        map={
            'style': "open-street-map",
            'center': {'lon': segments_to_plot['longitude'].mean(), 'lat': segments_to_plot['latitude'].mean()},
            'zoom': 13
        },
        showlegend=False,
        # title='Trajectories within Specified Date and Time Range'
    )

    fig.show()

if __name__ == '__main__':
    # 读取数据
    current_dir = os.getcwd() # 获取当前脚本的路径
    data = pd.read_pickle(current_dir + '/../data/segmented_data.pkl')

    # 绘制轨迹
    plot_trajectories(data, '2024-04-18', '2024-04-20', 8, 12)