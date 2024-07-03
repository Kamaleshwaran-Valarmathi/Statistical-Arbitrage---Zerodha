import csv
import json
import math
import os

from constants import INPUT_FOLDER_PATH


def get_close_price(data):
    close = list()
    for candle in data['data']['candles']:
        close.append(candle[4])
    return close


def get_instrument_filepath_map():
    instrument_filepath_map = dict()
    for file in os.listdir(INPUT_FOLDER_PATH):
        if file.endswith('.json'):
            instrument = file.strip().split('.')[0]
            filepath = INPUT_FOLDER_PATH + file
            instrument_filepath_map[instrument] = filepath
    return instrument_filepath_map


def read_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


def rolling_standard_deviation(close_values, window_size):
    std_dev = list()
    for i in range(len(close_values)):
        if i < window_size - 1:
            std_dev.append(None)
        else:
            window = close_values[i-window_size+1 : i+1]
            mean = sum(window) / window_size
            variance = sum((x - mean) ** 2 for x in window) / window_size
            cur_std_dev = math.sqrt(variance)
            std_dev.append(cur_std_dev)
    return std_dev


def simple_moving_average(data, window_size):
    sma = list()
    for i in range(len(data)):
        if i < window_size - 1:
            sma.append(None)
        else:
            window = data[i-window_size+1 : i+1]
            cur_sma = sum(window) / window_size
            sma.append(cur_sma)
    return sma


def write_csv(filepath, data):
    with open(filepath, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in data:
            csv_writer.writerow(row)
