from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from aws.multi_page.app import app
from aws.multi_page.apps import realtime, history


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id="menu"),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link("realtime graph", href="/realtime"),
    html.Br(),
    dcc.Link("history_graph", href="/history")
])

@app.callback(Output('menu', 'children'),
              [Input('url', 'pathname')])
def display_menu(pathname):
    if((pathname != '/apps/realtime')&(pathname != '/apps/history')):
        return index_page

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/realtime':
         return realtime.layout
    elif pathname == '/apps/history':
         return history.layout
    else:
        return "404"

if __name__ == '__main__':
    app.run_server(debug=True)
