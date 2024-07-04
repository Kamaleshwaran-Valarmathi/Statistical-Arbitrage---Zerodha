#pragma once

#include <vector>

#include "constants.h"
#include "utils.h"


class Core {
public:
    static double calc_hedge_ratio(std::vector<double>& close_1, std::vector<double>& close_2) {
        double numerator = 0.0;
        double denominator = 0.0;
        for (int i = 0; i < close_1.size(); ++i) {
            numerator += (close_1[i] * close_2[i]);
            denominator += (close_1[i] * close_1[i]);
        }
        double hedge_ratio = numerator / denominator;
        return hedge_ratio;
    }


    static std::vector<double> calc_spread(std::vector<double>& close_1, std::vector<double>& close_2, double hedge_ratio) {
        std::vector<double> spread;
        for (int i = 0; i < close_1.size(); ++i) {
            double cur_spread = (close_1[i] * hedge_ratio) - close_2[i];
            spread.push_back(cur_spread);
        }
        return spread;
    }


    static int calc_valid_crossover_count(std::vector<double>& spread, std::vector<double>& z_score, double fee) {
        int crossover_count = 0;
        bool passed_threshold = false;
        for (int i = 1; i < spread.size(); ++i) {
            if (!std::isnan(z_score[i])) {
                if (passed_threshold && std::abs(z_score[i]) >= 1.0) {
                    if (spread[i-1] < 0 && spread[i] >= 0) {
                        ++crossover_count;
                        passed_threshold = false;
                    } else if (spread[i-1] > 0 && spread[i] <= 0) {
                        ++crossover_count;
                        passed_threshold = false;
                    }
                }
            }
            if (std::abs(spread[i]) > fee)
                passed_threshold = true;
        }
        return crossover_count;
    }


    static std::vector<double> calc_z_score(std::vector<double>& spread) {
        std::vector<double> mean = Utils::simple_moving_average(spread, Constants::WINDOW_SIZE);
        std::vector<double> std_dev = Utils::rolling_standard_deviation(spread, Constants::WINDOW_SIZE);

        std::vector<double> z_score(spread.size(), 0.0);
        for (int i = 0; i < spread.size(); ++i) {
            if (!std::isnan(mean[i]) && std_dev[i] != 0.0) {
                z_score[i] = (spread[i] - mean[i]) / std_dev[i];
            } else {
                z_score[i] = NAN;
            }
        }

        // Forcefully free the memory
        std::vector<double>().swap(mean);
        std::vector<double>().swap(std_dev);
        
        return z_score;
    }
};
