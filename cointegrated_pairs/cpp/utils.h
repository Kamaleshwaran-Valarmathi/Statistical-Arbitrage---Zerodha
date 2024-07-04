#pragma once

#include <dirent.h>
#include <fstream>
#include <string>
#include <unordered_map>
#include <vector>

#include "constants.h"


class Utils {
public:
    static std::unordered_map<std::string, std::string> get_instrument_filepath_map() {
        std::unordered_map<std::string, std::string> instrument_filepath_map;
        DIR* dir = opendir(Constants::INPUT_FOLDER_PATH.c_str());
        if (dir == NULL)
            perror("Could not open directory");
        
        struct dirent* ent;
        while ((ent = readdir(dir)) != NULL) {
            std::string file_name = ent->d_name;
            if (file_name.find(".json") != std::string::npos) {
                std::string instrument = file_name.substr(0, file_name.find('.'));
                std::string filepath = Constants::INPUT_FOLDER_PATH + file_name;
                instrument_filepath_map[instrument] = filepath;
            }
        }
        closedir(dir);
        return instrument_filepath_map;
    }


    static std::vector<double> rolling_standard_deviation(std::vector<double>& data, int window_size) {
        std::vector<double> std_dev;
        double window_sum = 0.0;
        for (int i = 0; i < data.size(); ++i) {
            window_sum += data[i];
            if (i < window_size - 1) {
                std_dev.push_back(NAN);
            } else {
                double mean = window_sum / window_size;
                double variance = 0.0;
                for (int j = i - window_size + 1; j <= i; ++j)
                    variance += pow(data[j] - mean, 2);
                variance /= window_size;
                
                double cur_std_dev = sqrt(variance);
                std_dev.push_back(cur_std_dev);
                window_sum -= data[i - window_size + 1];
            }
        }
        return std_dev;
    }


    static std::vector<double> simple_moving_average(std::vector<double>& data, int window_size) {
        std::vector<double> sma;
        double window_sum = 0.0;
        for (int i = 0; i < data.size(); ++i) {
            window_sum += data[i];
            if (i < window_size - 1) {
                sma.push_back(NAN);
            } else {
                double cur_sma = window_sum / window_size;
                sma.push_back(cur_sma);
                window_sum -= data[i - window_size + 1];
            }
        }
        return sma;
    }


    static void write_csv(const std::string& filepath, std::vector<std::vector<std::string>>& data) {
        std::ofstream file(filepath);
        for (auto& row : data) {
            for (int i = 0; i < row.size(); ++i) {
                file << row[i];
                if (i < row.size() - 1)
                    file << ",";
            }
            file << "\n";
        }
    }
};
