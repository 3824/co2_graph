import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import datetime
from sqlalchemy import create_engine
import plotly
from statsmodels.tsa import arima_model
from loremipsum import get_sentences

import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Tabs(
            tabs=[
                {"label":"real time","value":0},
                {"label":"history","value":1}
            ],
            value=2,
            id="tabs",
            vertical=True
        ),
        html.Div(id="tab-output")
    ], style={
        "width": "80%",
        "fontFamily": "Sans-Serif",
        "margin-left": "auto",
        "margin-right": "auto"
    }),
    html.Div([
        html.Div([
            html.H4("温度と湿度とCO2"),
            html.Div(id="live-update-text"),
            dcc.Graph(id="live-update-graph", animate=True),
            dcc.Interval(
                id="interval-component",
                interval=1000 # ms
            )
        ]),
        html.Div([
            html.H3("test"),
            # TODO DatePickRangeで期間指定してグラフ表示＋変化点表示
            dcc.DatePickerRange(
                start_date = datetime.datetime(2017,9,1),
                end_date = datetime.datetime.today(),
                day_size = 30,
                calendar_orientation = "vertical",
                display_format = "YYYY-MM-DD"
            )
        ])
    ], style={
        "width":"80%",
        "fontFamily": "Sans-Serif",
        "margin-left": "auto",
        "margin-right": "auto"
    })
])

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    if value == 0:
        return 0
    elif value == 1:
        return 1


@app.callback(Output("live-update-text", "children"),
              events=[Event("interval-component", "interval")])
def update_metrics():
    str = load_data()
    style = {"padding":"5px", "fontSize":"16px"}
    return [
        html.Span(str, style=style)
    ]

def load_data():
    '''
    :return: CO2, 気温，湿度
    '''
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

pred_temp_timeline = []
pred_temp_values = []
pred_shi_timeline = []
pred_shi_values = []
pred_co2_timeline = []
pred_co2_values = []

query = "select * from sensor where temp<> -1 and shi<> -1 and obs_time> %(start_time)s"
engine = create_engine("mysql+pymysql://miyanishi:miyanishi@52.69.118.173:3306/log")

@app.callback(Output('live-update-graph','figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_live():
    start_time = (datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')
    df = pd.read_sql_query(query,engine,params={"start_time": start_time})

    fig = plotly.tools.make_subplots(rows=3,cols=1)#,vertical_spacing=100)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 30
    }
    fig['layout']['legend'] = {'x': 100, 'y': 1, 'xanchor': 'left'}

    print(df["obs_time"].max())
    #### ¥
    pred_time = (df["obs_time"].max() + datetime.timedelta(seconds=1))  # .strftime('%Y-%m-%d %H:%M:%S')
    temp_df = df.set_index("obs_time")
    try:
        temp_model = arima_model.ARIMA(temp_df["temp"], order=[4, 0, 0]).fit()
        pred_temp = temp_model.forecast()[0][0]
    except:
        pred_temp = temp_df.tail(1)["temp"].values[0]
    try:
        shi_model = arima_model.ARIMA(temp_df["shi"], order=[4, 0, 0]).fit()
        pred_shi = shi_model.forecast()[0][0]
    except:
        pred_shi = temp_df.tail(1)["shi"].values[0]
    try:
        co2_model = arima_model.ARIMA(temp_df["co2"], order=[4, 0, 0]).fit()
        pred_co2 = co2_model.forecast()[0][0]
    except:
        pred_co2 = temp_df.tail(1)["co2"].values[0]

    fig.append_trace({
        "x": df["obs_time"],
        "y": df["temp"],
        "type": "scatter",
        "name": "温度",
        "mode": "lines+markers",
        "marker": {
            "size": 4
        }
    }, 1, 1)
    fig.append_trace({
        "x": [pred_time],
        "y": [pred_temp],
        "showlegend": False,
        "mode": "markers+text",
        "text": ["予測温度"],
        "opacity": 0.5,
        "textposition": "top",
        "marker":{
            "color": "#11AAAA"
        }
    }, 1, 1)
    fig.append_trace({
        "x": pred_temp_timeline,
        "y": pred_temp_values,
        "type": "scatter",
        "name": "予測した温度",
        "mode": "lines+markers",
        "marker": {
            "size": 4
        },
        "opacity": 0.5
    }, 1, 1)

    fig.append_trace({
        "x": df["obs_time"],
        "y": df["shi"],
        "type": "scatter",
        "name": "湿度",
        "mode": "lines+markers",
        "marker": {
            "size": 4
        }
    }, 2, 1)
    fig.append_trace({
        "x": [pred_time],
        "y": [pred_shi],
        "showlegend": False,
        "mode": "markers+text",
        "text": ["予測湿度"],
        "opacity": 0.5,
        "textposition": "top",
        "marker":{
            "color": "#AAAA11"
        }
    }, 2, 1)
    fig.append_trace({
        "x": pred_shi_timeline,
        "y": pred_shi_values,
        "type": "scatter",
        "name": "予測した湿度",
        "mode": "lines+markers",
        "marker": {
            "size": 4
        },
        "opacity": 0.5
    }, 2, 1)

    fig.append_trace({
        "x": df["obs_time"],
        "y": df["co2"],
        "type": "scatter",
        "name": "CO2",
        "mode": "lines+markers",
        "marker": {
            "size": 4
        }
    }, 3, 1)
    fig.append_trace({
        "x": [pred_time],
        "y": [pred_co2],
        "showlegend": False,
        "mode": "markers+text",
        "text": ["予測PPM"],
        "opacity": 0.5,
        "textposition": "top",
        "marker":{
            "color": "#AA11AA"
        }
    }, 3, 1)
    fig.append_trace({
        "x": pred_co2_timeline,
        "y": pred_co2_values,
        "type": "scatter",
        "name": "予測したppm",
        "mode": "lines+markers",
        "marker": {
            "size": 4
        },
        "opacity": 0.5
    }, 3, 1)

#    timeline_length = 500
    timeline_length = 300

    pred_temp_timeline.append(pred_time)
    pred_temp_values.append(pred_temp)
    if len(pred_temp_timeline) > timeline_length:
        del pred_temp_timeline[0]
        del pred_temp_values[0]
    pred_shi_timeline.append(pred_time)
    pred_shi_values.append(pred_shi)
    if len(pred_shi_timeline) > timeline_length:
        del pred_shi_timeline[0]
        del pred_shi_values[0]
    pred_co2_timeline.append(pred_time)
    pred_co2_values.append(pred_co2)
    if len(pred_co2_timeline) > timeline_length:
        del pred_co2_timeline[0]
        del pred_co2_values[0]

    return fig



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
