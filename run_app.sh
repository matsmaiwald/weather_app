#!/bin/bash

source ~/venvs/weather_app/bin/activate
python3 app.py &
chromium-browser http://127.0.0.1:8050/