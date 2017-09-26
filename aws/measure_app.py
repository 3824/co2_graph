import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import datetime
from sqlalchemy import create_engine
import plotly
from statsmodels.tsa import arima_model

import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="menu"),
    html.Div(id="page-content")
])

index_page = html.Div([
    dcc.Link("realtime graph", href="/realtime"),
    html.Br(),
    dcc.Link("history_graph", href="history")
])

realtime_layout = html.Div([
    html.Div([
        html.H4("温度と湿度とCO2"),
        html.Div(id="live-update-text"),
        dcc.Graph(id="live-update-graph"),
        dcc.Interval(
            id="interval-component",
            interval=1000 # ms
        )
    ])
])

history_layout = html.Div([
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

@app.callback(dash.dependencies.Output('menu', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname != "/realtime" & pathname != "/history":
        return index_page
    else:
        return ""

@app.callback(dash.dependencies.Output('page-content', 'children'),
                  [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/realtime":
        return realtime_layout
    elif pathname != "/history":
        return history_layout
    else:
        return ""






if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)

