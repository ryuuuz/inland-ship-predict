import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import shapely.geometry
from dash import Input, Output
import geopandas as gdf

# Load the preprocessed data
current_dir = os.getcwd()  # 获取当前脚本的路径
data = pd.read_pickle(current_dir + '/../output/segmented_data.pkl')

gdf = gdf.read_file(current_dir + '/../output/saved_trajectories.shp')
# 只要前 1000 行数据
gdf = gdf.head(1000)

n = 50  # Number of top trajectories to display

# Register callbacks for interactivity
def register_callbacks(app):
    @app.callback(
        Output('segmented-data-plot', 'figure'),
        Input('date-range-picker', 'start_date'),
        Input('date-range-picker', 'end_date')
    )
    def update_segmented_plot(start_date, end_date):
        start_hour, end_hour = 8, 12

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

        # Count points in each trajectory
        trajectory_counts = segments_to_plot.groupby(['mmsi', 'segment_id']).size()

        # Select top n trajectories with the most points
        top_trajectories = trajectory_counts.nlargest(n).index.tolist()

        # Filter the original data to include only these top trajectories
        top_trajectory_data = segments_to_plot[
            segments_to_plot.set_index(['mmsi', 'segment_id']).index.isin(top_trajectories)]

        # 设置地图
        fig = go.Figure()

        # 为每个轨迹段绘制线段
        for (mmsi, segment_id), segment_data in top_trajectory_data.groupby(['mmsi', 'segment_id']):
            # 创建悬停文本
            hover_text = [
                f"MMSI: {mmsi:.0f}<br>Lat: {lat:.6f}, Lon: {lon:.6f}<br>Time: {time}<br>Speed: {speed} knots"
                for lat, lon, time, speed in
                zip(segment_data['latitude'], segment_data['longitude'], segment_data['post_time'],
                    segment_data['speed'])
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
                'style': "basic",
                'center': {'lon': segments_to_plot['longitude'].mean(), 'lat': segments_to_plot['latitude'].mean()},
                'zoom': 13
            },
            showlegend=True,
            # title='Trajectories within Specified Date and Time Range'
        )
        return fig

    @app.callback(
        Output('trajectory-map-plot', 'figure'),
        Input('date-range-picker', 'start_date'),
        Input('date-range-picker', 'end_date')
    )
    def update_trajectory_map(start_date, end_date):
        lats = []
        lons = []
        names = []

        for feature, segment_id in zip(gdf.geometry, gdf.segment_id):
            if isinstance(feature, shapely.geometry.linestring.LineString):
                linestrings = [feature]
            elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
                linestrings = feature.geoms
            else:
                continue

            for linestring in linestrings:
                x, y = linestring.xy
                lons.extend(x)
                lats.extend(y)
                names.extend([segment_id] * len(x))

        fig = px.line_map(lat=lats,
                          lon=lons,
                          hover_name=names,
                          map_style="open-street-map",
                          center={"lat": 2.959095e+01, "lon": 1.066427e+02},
                          zoom=13)

        return fig


