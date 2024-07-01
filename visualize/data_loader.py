from datetime import datetime
from pytz import timezone
import json


# Load the data
instrument = 'Instrument_7'
file_path = f'../resources/random_data/{instrument}.json'
with open(file_path, "r") as json_file:
    data = json.load(json_file)

candlesticks = data["data"]["candles"]
dates = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S%z") for d in [c[0] for c in candlesticks]]

ist_tz = timezone('Asia/Kolkata')
dates_ist = [d.astimezone(ist_tz) for d in dates]

opens = [c[1] for c in candlesticks]
highs = [c[2] for c in candlesticks]
lows = [c[3] for c in candlesticks]
closes = [c[4] for c in candlesticks]
volumes = [c[5] for c in candlesticks]
