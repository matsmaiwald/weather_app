import requests
import json
import pandas as pd

import yaml


def get_api_key(file_path: str) -> str:

    with open(file_path, "r") as stream:
        try:
            api_key = yaml.safe_load(stream)["api_key"]
        except yaml.YAMLError as exc:
            print(exc)

    return api_key


api_key = get_api_key("api_key.yaml")
url = f"https://api.openweathermap.org/data/2.5/onecall?lat=52.52437&lon=13.41053&&appid={api_key}&units=metric"

print(f"Sending a get request to the following url: {url}")

response_get = requests.get(url).text
response_dict = json.loads(response_get)
print(f"Received as response: {response_get}")

fcs = dict()
fcs["hourly"] = dict()
timestamps = []
temperatures = []
weather = []
for hourly_forecast in response_dict.get("hourly"):
    timestamps.append(pd.to_datetime(hourly_forecast.get("dt"), unit="s"))
    temperatures.append(hourly_forecast.get("temp"))
    weather.append(hourly_forecast.get("weather")[0].get("main"))
df = pd.DataFrame({"times": timestamps, "temp": temperatures, "weather": weather})

print(df)
