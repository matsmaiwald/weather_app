import dash
import io
import base64
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from client import get_weather_data
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.dates as mdates
import pandas as pd
from typing import List


path_rain = (
    "./images/iconfinder_Weather_Weather_Forecast_Heavy_Rain_Cloud_Climate_3859135.png"
)
path_sun = "./images/iconfinder_Weather_Weather_Forecast_Hot_Sun_Day_3859136.png"
path_clouds = (
    "./images/iconfinder_Weather_Weather_Forecast_Cloudy_Season_Cloud_3859132.png"
)
path_snow = "./images/snow.png"
path_semi_cloudy = "./images/cloudy.png"

images = {
    "Rain": plt.imread(path_rain),
    "Sun": plt.imread(path_sun),
    "Clouds": plt.imread(path_clouds),
    "Snow": plt.imread(path_snow),
    "Clear": plt.imread(path_semi_cloudy),
}

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

font_options = {"font.size": 16}

plt.rcParams.update(font_options)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(
    Output("forecast_graph", "src"), [Input("interval-component", "n_intervals")]
)
def run_app(n):
    plt.close("all")
    df = get_weather_data()
    plot_graph_plus_symbols(
        x=df["timestamp"], y=df["temp"], symbol_keys=df["weather"], images=images
    )
    buf = io.BytesIO()  # in-memory files
    plt.savefig(buf, format="png")  # save to the above file object
    data = base64.b64encode(buf.getbuffer()).decode("utf8")  # encode to html elements
    plt.close()
    return "data:image/png;base64,{}".format(data)


def plot_graph_plus_symbols(
    x: pd.Series, y: pd.Series, symbol_keys: pd.Series, images: List, ax=None
):
    fig, ax = plt.subplots(figsize=(12, 7))
    # Plot temperature
    ax.plot(x, y, linewidth=5)

    # Plot symbol
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%H:%M"))

    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

    for xi, yi, zi in zip(x, y, symbol_keys):
        try:
            im = OffsetImage(images[zi], zoom=5 / ax.figure.dpi)
            im.image.axes = ax

            ab = AnnotationBbox(im, (xi, yi), frameon=False, pad=0.0,)

            ax.add_artist(ab)
        except KeyError as e:
            print(f"No image found for weather: {e}")

    return fig


app.layout = html.Div(
    children=[
        html.H1(children="Weather Forecast"),
        html.Div(children="""Hourly temperature and weather forecast."""),
        html.Img(id="forecast_graph", style={"height": "80%", "width": "80%"}),
        dcc.Interval(id="interval-component", interval=0.5 * 60 * 1000, n_intervals=0),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
