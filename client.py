import requests
import json
import pandas as pd
import io
import urllib.request

import yaml


def _get_api_key(file_path: str) -> str:

    with open(file_path, "r") as stream:
        try:
            api_key = yaml.safe_load(stream)["api_key"]
        except yaml.YAMLError as exc:
            print(exc)

    return api_key


def _get_response_dict(url: str) -> dict:

    print(f"Sending a get request to the following url: {url}")

    response_get = requests.get(url).text
    response_dict = json.loads(response_get)

    return response_dict


def _process_weather_data(weather_data: dict) -> pd.DataFrame:

    fcs = dict()
    fcs["hourly"] = dict()
    timestamps = []
    temperatures = []
    icon_codes = []
    for hourly_forecast in weather_data.get("hourly"):
        timestamps.append(pd.to_datetime(hourly_forecast.get("dt"), unit="s"))
        temperatures.append(hourly_forecast.get("temp"))
        icon_codes.append(hourly_forecast.get("weather")[0].get("icon"))

    df = pd.DataFrame(
        {"timestamp": timestamps, "temp": temperatures, "icon_code": icon_codes}
    )
    df["icon_code"].apply(_download_icon_from_code)
    return df


def _download_image_from_url(url: str, download_name: str, download_dir: str = "./"):

    img_data = requests.get(url).content
    with open(f"{download_dir}{download_name}.png", "wb") as f:
        f.write(img_data)


def _get_icon_url(icon_code: str):
    url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    return url


def _download_icon_from_code(icon_code: str):
    url = _get_icon_url(icon_code=icon_code)
    _download_image_from_url(
        url, download_name=icon_code, download_dir="./images/",
    )


def get_weather_data() -> pd.DataFrame:

    api_key = _get_api_key("api_key.yaml")
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat=52.52437&lon=13.41053&&appid={api_key}&units=metric"
    weather_data_raw = _get_response_dict(url=url)
    df = _process_weather_data(weather_data=weather_data_raw)
    return df


if __name__ == "__main__":
    # df = get_weather_data()
    # print(df)
    _download_icon_from_code(icon_code="10d")
