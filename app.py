import base64
import io
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.figure
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from client import get_weather_forecast_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

font_options = {"font.size": 16}

plt.rcParams.update(font_options)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def plot_temperature_graph_plus_icons(
    timestamps: pd.Series, temperatures: pd.Series, icon_codes: pd.Series,
) -> matplotlib.figure:
    """Create the plot of temperatures and weather icons."""

    def load_icon(icon_code: str) -> np.array:
        """Load the image data associated with a specific icon code."""
        return plt.imread(f"./images/{icon_code}.png")

    def plot_icon(icon: np.array, x_cord: float, y_cord: float, ax: plt.axis):
        """Plot icon at a specified location."""
        im = OffsetImage(icon, zoom=29 / ax.figure.dpi)
        im.image.axes = ax

        ab = AnnotationBbox(im, (x_cord, y_cord), frameon=False, pad=-1.0,)

        ax.add_artist(ab)

    # Set up graph
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.set_facecolor("lightblue")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%H:%M"))
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

    # Plot temperature over time
    ax.plot(timestamps, temperatures, linewidth=5)

    # Plot icons
    for icon_code, timestamp, temperature in zip(icon_codes, timestamps, temperatures):
        try:
            icon = load_icon(icon_code=icon_code)
            plot_icon(icon=icon, x_cord=timestamp, y_cord=temperature, ax=ax)
        except KeyError as e:
            print(f"No image found for icon code: {e}")

    return fig


app.layout = html.Div(
    children=[
        html.H1(children="Weather Forecast"),
        html.Div(children="""Hourly temperature and weather forecast."""),
        html.Img(id="forecast_graph", style={"height": "80%", "width": "80%"}),
        dcc.Interval(id="interval-component", interval=0.5 * 60 * 1000, n_intervals=0),
    ]
)


@app.callback(
    Output("forecast_graph", "src"), [Input("interval-component", "n_intervals")]
)
def run_app(n: float):
    """Wrapper function to run the app."""
    with open("config.json") as f:
        config = json.load(f)
    plt.close("all")
    df = get_weather_forecast_data(lat=config["lat"], lon=config["lon"])
    plot_temperature_graph_plus_icons(
        timestamps=df["timestamp"], temperatures=df["temp"], icon_codes=df["icon_code"],
    )
    buf = io.BytesIO()  # in-memory files
    plt.savefig(buf, format="png")  # save to the above file object
    data = base64.b64encode(buf.getbuffer()).decode("utf8")  # encode to html elements
    plt.close()
    return "data:image/png;base64,{}".format(data)


if __name__ == "__main__":
    app.run_server(debug=True)
