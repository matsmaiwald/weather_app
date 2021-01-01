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
        x=df["timestamp"], y=df["temp"], symbol_keys=df["icon_code"],
    )
    buf = io.BytesIO()  # in-memory files
    plt.savefig(buf, format="png")  # save to the above file object
    data = base64.b64encode(buf.getbuffer()).decode("utf8")  # encode to html elements
    plt.close()
    return "data:image/png;base64,{}".format(data)


def plot_graph_plus_symbols(
    x: pd.Series, y: pd.Series, symbol_keys: pd.Series,
):
    fig, ax = plt.subplots(figsize=(12, 7))
    # Plot temperature
    ax.plot(x, y, linewidth=5)
    ax.set_facecolor("lightblue")

    # Plot symbol
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%H:%M"))

    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

    for xi, yi, zi in zip(x, y, symbol_keys):
        try:
            im = OffsetImage(plt.imread(f"./images/{zi}.png"), zoom=30 / ax.figure.dpi)
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
