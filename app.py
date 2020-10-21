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
    Output("example-graph", "src"), [Input("interval-component", "n_intervals")]
)
def make_data(n):
    plt.close("all")
    df = get_weather_data()
    # fig = px.line(df, x="timestamp", y="temp")
    fig = plot_weather(x=df["timestamp"], y=df["temp"], z=df["weather"], images=images)
    buf = io.BytesIO()  # in-memory files
    plt.savefig(buf, format="png")  # save to the above file object
    data = base64.b64encode(buf.getbuffer()).decode("utf8")  # encode to html elements
    plt.close()
    return "data:image/png;base64,{}".format(data)
    # return mpl_to_plotly(fig)


def plot_weather(x, y, z, images, ax=None):
    fig, ax = plt.subplots(figsize=(12, 7))
    # Plot temperature
    ax.plot(x, y)

    # Plot symbol
    ax = ax or plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a\n%H:%M"))

    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

    for xi, yi, zi in zip(x, y, z):
        try:
            im = OffsetImage(images[zi], zoom=5 / ax.figure.dpi)
            im.image.axes = ax

            ab = AnnotationBbox(im, (xi, yi), frameon=False, pad=0.0,)

            ax.add_artist(ab)
        except KeyError:
            pass

    return fig


app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        html.Img(id="example-graph"),
        dcc.Interval(id="interval-component", interval=10 * 1000, n_intervals=0),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

