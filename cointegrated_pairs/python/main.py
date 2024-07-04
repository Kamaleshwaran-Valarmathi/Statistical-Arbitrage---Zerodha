"""
To execute the main.py, use the following cmd
python3 main.py
"""


from tqdm import tqdm

from constants import FEE, OUTPUT_FILEPATH
from core import calc_hedge_ratio, calc_spread, calc_valid_crossover_count, calc_z_score
from utils import get_close_price, get_instrument_filepath_map, read_json, write_csv


def calc_cointegration(filepath_1, filepath_2, fee, visualization_flag):
    data_1 = read_json(filepath_1)
    data_2 = read_json(filepath_2)
    
    close_1 = get_close_price(data_1)
    close_2 = get_close_price(data_2)
    
    # Ensuring both close_prices have the same number of elements
    data_size = min(len(close_1), len(close_2))
    close_1 = close_1[-data_size:]
    close_2 = close_2[-data_size:]
    
    hedge_ratio = calc_hedge_ratio(close_1, close_2)
    spread = calc_spread(close_1, close_2, hedge_ratio)
    z_score = calc_z_score(spread)
    crossover_count = calc_valid_crossover_count(spread, z_score, fee)

    return [ data_1, data_2, spread, z_score, crossover_count ] if visualization_flag else crossover_count


instrument_filepath_map = get_instrument_filepath_map()
cointegration_result = list()

progress_bar_outer = tqdm(instrument_filepath_map.items(), desc="Outer Loop", total=len(instrument_filepath_map), position=0)
for instrument_1, filepath_1 in instrument_filepath_map.items():
    progress_bar_outer.set_description(f"Outer Loop: {instrument_1}")
    
    progress_bar_inner = tqdm(instrument_filepath_map.items(), desc="Inner Loop", total=len(instrument_filepath_map), position=1, leave=False)
    for instrument_2, filepath_2 in instrument_filepath_map.items():
        progress_bar_inner.set_description(f"Inner Loop: {instrument_2}")
        
        if instrument_1 != instrument_2:
            crossover_count = calc_cointegration(filepath_1, filepath_2, FEE, False)
            cointegration_result.append([instrument_1, instrument_2, crossover_count, filepath_1, filepath_2])

        progress_bar_inner.update(1)
    progress_bar_inner.close()

    progress_bar_outer.update(1)
progress_bar_outer.close()

cointegration_result = sorted(cointegration_result, key=lambda x: x[2], reverse=True)
header = ['Instrument 1', 'Instrument 2', 'Crossover Count', 'Filepath 1', 'Filepath 2']
cointegration_result.insert(0, header)

write_csv(OUTPUT_FILEPATH, cointegration_result)
