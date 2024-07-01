from datetime import datetime, timedelta
import random


def is_less_than_or_equal_to_date(value, target):
    cur_date = datetime.strptime(value, '%Y-%m-%d').date()
    target_date = datetime.strptime(target, '%Y-%m-%d').date()
    return cur_date <= target_date


def is_less_than_or_equal_to_time(value, target):
    cur_time = datetime.strptime(value, '%H:%M:%S').time()
    target_time = datetime.strptime(target, '%H:%M:%S').time()
    return cur_time <= target_time


def increment_date(value, steps):
    cur_date = datetime.strptime(value, '%Y-%m-%d').date()
    delta = timedelta(days=steps)
    res_date = cur_date + delta
    return res_date.strftime('%Y-%m-%d')


def increment_time(value, steps):
    cur_time = datetime.strptime(value, '%H:%M:%S').time()
    delta = timedelta(minutes=steps)
    res_time = datetime.combine(datetime.min.date(), cur_time) + delta
    return res_time.strftime('%H:%M:%S')


def is_weekend(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = date_obj.weekday()
    return weekday in (5, 6)


def get_next_price(price):
    tick_value = 0.05
    min_value = 0.05 # tick value
    max_value = price * 0.005 # 0.5% of the current price
    random_value = random.uniform(min_value, max_value)
    random_value_rounded = round(random_value / tick_value) * tick_value
    
    is_negative = random.choice([True, False])
    if is_negative and (price - random_value_rounded < tick_value):
        is_negative = False
    
    res_price = (price - random_value_rounded) if is_negative else (price + random_value_rounded)
    return round(res_price, 2)


def generate_next_ohlc(price):
    random_prices = sorted([get_next_price(price) for _ in range(3)])
    open, high, low, close = price, random_prices[2], random_prices[0], random_prices[1]
    return [ open, high, low, close ]


def generate_next_volume():
    min_volume, max_volume = 210, 2_100_000
    cur_volume = random.randint(min_volume, max_volume)
    return cur_volume
