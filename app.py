import dash
import dash_core_components as dcc
from plotly.tools import mpl_to_plotly
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
from client import get_weather_data
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

path_rain = "/home/mats/Downloads/iconfinder_Weather_Weather_Forecast_Heavy_Rain_Cloud_Climate_3859135.png"
path_sun = (
    "/home/mats/Downloads/iconfinder_Weather_Weather_Forecast_Hot_Sun_Day_3859136.png"
)
path_clouds = "/home/mats/Downloads/iconfinder_Weather_Weather_Forecast_Cloudy_Season_Cloud_3859132.png"
images = {
    "Rain": plt.imread(path_rain),
    "Sun": plt.imread(path_sun),
    "Clouds": plt.imread(path_clouds),
}

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(
    Output("example-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def make_data(n):
    plt.close("all")
    df = get_weather_data()
    # fig = px.line(df, x="timestamp", y="temp")
    fig = plot_weather(x=df["timestamp"], y=df["temp"], z=df["weather"], images=images)
    return mpl_to_plotly(fig)


def plot_weather(x, y, z, images, ax=None):
    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax = ax or plt.gca()

    for xi, yi, zi in zip(x, y, z):
        im = OffsetImage(images[zi], zoom=5 / ax.figure.dpi)
        im.image.axes = ax

        ab = AnnotationBbox(im, (xi, yi), frameon=False, pad=0.0,)

        ax.add_artist(ab)

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
        dcc.Interval(id="interval-component", interval=10 * 1000, n_intervals=0),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

