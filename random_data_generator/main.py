import json
from tqdm import tqdm

from utils import *


def generate_random_data(cur_price):
    random_data = {
        'status': 'success',
        'data': {
            'candles': []
        }
    }

    cur_date = start_date
    while is_less_than_or_equal_to_date(cur_date, end_date):
        if not is_weekend(cur_date):
            cur_time = start_time
            while is_less_than_or_equal_to_time(cur_time, end_time):
                cur_timestamp = f'{cur_date}T{cur_time}+0530'
                [ cur_open, cur_high, cur_low, cur_close ] = generate_next_ohlc(cur_price)
                cur_volume = generate_next_volume()
                cur_candle = [ cur_timestamp , cur_open, cur_high, cur_low, cur_close, cur_volume]
                random_data['data']['candles'].append(cur_candle)
                cur_price = cur_close
                cur_time = increment_time(cur_time, 1)
        cur_date = increment_date(cur_date, 1)

    return random_data


no_of_instruments = 100

start_date = '2022-06-30'
end_date = '2024-06-30'
start_time = '09:15:00'
end_time = '15:29:00'

timeframe = 1 # integer value in terms of minutes
assert 1 <= timeframe <= 60, "Timeframe must be between 1 and 60 (inclusive)"

for instrument_no in tqdm(range(1, no_of_instruments+1), desc='Instruments data generated'):
    start_price = get_next_price(random.uniform(100, 1000))
    random_data = generate_random_data(start_price)
    
    with open(f'../resources/random_data/Instrument_{instrument_no}.json', 'w') as output_file:
        json.dump(random_data, output_file)
