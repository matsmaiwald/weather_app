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
import json


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

font_options = {"font.size": 16}

plt.rcParams.update(font_options)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(
    Output("forecast_graph", "src"), [Input("interval-component", "n_intervals")]
)
def run_app(n):

    with open("config.json") as f:
        config = json.load(f)
    plt.close("all")
    df = get_weather_data(lat=config["lat"], lon=config["lon"])
    plot_graph_plus_icons(
        x=df["timestamp"], y=df["temp"], icon_codes=df["icon_code"],
    )
    buf = io.BytesIO()  # in-memory files
    plt.savefig(buf, format="png")  # save to the above file object
    data = base64.b64encode(buf.getbuffer()).decode("utf8")  # encode to html elements
    plt.close()
    return "data:image/png;base64,{}".format(data)


def plot_graph_plus_icons(
    x: pd.Series, y: pd.Series, icon_codes: pd.Series,
):
    def load_icon(icon_code: str):
        return plt.imread(f"./images/{icon_code}.png")

    def plot_icons(icon_code: str, x_cord: float, y_cord: float, ax):
        try:
            im = OffsetImage(load_icon(icon_code=icon_code), zoom=29 / ax.figure.dpi)
            im.image.axes = ax

            ab = AnnotationBbox(im, (x_cord, y_cord), frameon=False, pad=-1.0,)

            ax.add_artist(ab)
        except KeyError as e:
            print(f"No image found for icon code: {e}")

    # Set up graph
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.set_facecolor("lightblue")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%H:%M"))
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

    # Plot temperature
    ax.plot(x, y, linewidth=5)

    # Plot icons
    for xi, yi, zi in zip(x, y, icon_codes):
        plot_icons(icon_code=zi, x_cord=xi, y_cord=yi, ax=ax)

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
