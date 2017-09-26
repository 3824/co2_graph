from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import datetime
from sqlalchemy import create_engine

from aws.multi_page.app import app

layout = html.Div([
    html.Div([
        html.H3("history"),
        # TODO DatePickRangeで期間指定してグラフ表示＋変化点表示
        dcc.DatePickerRange(
            start_date = datetime.datetime(2017,9,1),
            end_date = datetime.datetime.today(),
            day_size = 30,
            calendar_orientation = "vertical",
            display_format = "YYYY-MM-DD"
        )
    ]),
    html.Div([
        html.H4("温度と湿度とCO2"),
        dcc.Graph(id="history-graph")
    ])
])

query = "select * from sensor where temp<> -1 and shi<> -1 and obs_time> %(start_time) and obs_time< %(end_time)"
engine = create_engine("mysql+pymysql://miyanishi:miyanishi@52.69.118.173:3306/log")

