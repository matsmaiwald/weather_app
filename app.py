import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
from client import get_weather_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(
    Output("example-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def make_data(n):
    df = get_weather_data()
    fig = px.line(df, x="timestamp", y="temp")
    return fig


app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        dcc.Graph(id="example-graph"),
        dcc.Interval(id="interval-component", interval=60 * 1000, n_intervals=0),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

