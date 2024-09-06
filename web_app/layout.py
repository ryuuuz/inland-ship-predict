from dash import dcc, html

layout = html.Div(
    children=[
        html.H1("Data Visualization Dashboard"),

        # 日期选择器容器
        html.Div(
            className="date-picker-container",
            children=[
                html.Label("Select Date Range", className="date-picker-label"),
                dcc.DatePickerRange(
                    id='date-range-picker',
                    start_date='2024-04-19',
                    end_date='2024-04-20',
                    display_format='YYYY-MM-DD',
                    className="dash-datepicker"
                )
            ]
        ),

        # Tabs for different figures
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(label='Trajectory Map', children=[
                    dcc.Graph(id='trajectory-map-plot')
                ]),
                dcc.Tab(label='Segmented Data Plot', children=[
                    dcc.Graph(id='segmented-data-plot')
                ]),
            ]
        )
    ]
)
