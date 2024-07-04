from constants import WINDOW_SIZE
from utils import rolling_standard_deviation, simple_moving_average


def calc_hedge_ratio(close_1, close_2):
    numerator = 0
    denominator = 0
    for i in range(len(close_1)):
        numerator += (close_1[i] * close_2[i])
        denominator += (close_1[i] * close_1[i])
    hedge_ratio = numerator / denominator
    return hedge_ratio


def calc_spread(close_1, close_2, hedge_ratio):
    spread = list()
    for i in range(len(close_1)):
        cur_spread = (close_1[i] * hedge_ratio) - close_2[i]
        spread.append(cur_spread)
    return spread


def calc_valid_crossover_count(spread, z_score, fee):
    crossover_count = 0
    passed_threshold = False
    for i in range(1, len(spread)):
        if z_score[i] != None:
            if passed_threshold and abs(z_score[i]) >= 1:
                if spread[i-1] < 0 and spread[i] >= 0:
                    crossover_count += 1
                    passed_threshold = False
                elif spread[i-1] > 0 and spread[i] <= 0:
                    crossover_count += 1
                    passed_threshold = False
        if abs(spread[i]) > fee:
            passed_threshold = True
    return crossover_count


def calc_z_score(spread):
    mean = simple_moving_average(spread, WINDOW_SIZE)
    std_dev = rolling_standard_deviation(spread, WINDOW_SIZE)

    z_score = list()
    for i in range(len(mean)):
        if mean[i] == None:
            z_score.append(None)
        else:
            cur_z_score = (spread[i] - mean[i]) / std_dev[i]
            z_score.append(cur_z_score)
    return z_score
