/***
 * To comile the main.cpp, use the following cmd
 * clang++ -std=c++17 -O3 -pthread main.cpp -o main -I/opt/homebrew/Cellar/nlohmann-json/3.11.3/include
 * 
 * To run the main.cpp, use the following cmd
 * ./main
*/


#include <condition_variable>
#include <fstream>
#include <iostream>
#include <mutex>
#include <nlohmann/json.hpp>
#include <thread>

#include "constants.h"
#include "core.h"
#include "progress_bar.h"
#include "utils.h"


nlohmann::json read_json(std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open file: " + filepath);
    }

    nlohmann::json json_data;
    file >> json_data;
    return json_data;
}


std::vector<double> get_close_price(nlohmann::json& data) {
    std::vector<double> close;
    for (auto& candle : data["data"]["candles"])
        close.push_back(candle[4].get<double>());
    return close;
}


int calc_cointegration(std::string& filepath_1, std::string& filepath_2) {
    nlohmann::json data_1 = read_json(filepath_1);
    nlohmann::json data_2 = read_json(filepath_2);

    std::vector<double> close_1 = get_close_price(data_1);
    std::vector<double> close_2 = get_close_price(data_2);

    int data_size = std::min(close_1.size(), close_2.size());
    close_1.erase(close_1.begin(), close_1.begin() + (close_1.size() - data_size));
    close_2.erase(close_2.begin(), close_2.begin() + (close_2.size() - data_size));

    double hedge_ratio = Core::calc_hedge_ratio(close_1, close_2);
    std::vector<double> spread = Core::calc_spread(close_1, close_2, hedge_ratio);
    std::vector<double> z_score = Core::calc_z_score(spread);
    int crossover_count = Core::calc_valid_crossover_count(spread, z_score, Constants::FEE);

    // Forcefully free the memory
    nlohmann::json().swap(data_1);
    nlohmann::json().swap(data_2);
    std::vector<double>().swap(close_1);
    std::vector<double>().swap(close_2);
    std::vector<double>().swap(spread);
    std::vector<double>().swap(z_score);

    return crossover_count;
}


int main(void) {
    std::unordered_map<std::string, std::string> instrument_filepath_map = Utils::get_instrument_filepath_map();
    std::vector<std::vector<std::string>> cointegration_result;

    int total_instruments_count = instrument_filepath_map.size();
    int current_instrument_num = 0;

    std::string desc = "Instrument: " + std::to_string(current_instrument_num) + "/" + std::to_string(total_instruments_count);
    ProgressBar progress_bar(total_instruments_count, desc);

    std::mutex mtx;
    std::condition_variable cv;
    int active_threads = 0;

    auto find_cointegration = [&instrument_filepath_map, &cointegration_result, &mtx, &progress_bar, &current_instrument_num, &total_instruments_count, &active_threads, &cv](std::string instrument_1, std::string filepath_1) {
        for (auto& [instrument_2, filepath_2]: instrument_filepath_map) {
            if (instrument_1 != instrument_2) {
                int crossover_count = calc_cointegration(filepath_1, filepath_2);
                std::lock_guard<std::mutex> lock(mtx);
                cointegration_result.push_back({instrument_1, instrument_2, std::to_string(crossover_count), filepath_1, filepath_2});
            }
        }
        std::lock_guard<std::mutex> lock(mtx);
        std::string desc = "Instrument: " + std::to_string(++current_instrument_num) + "/" + std::to_string(total_instruments_count);
        progress_bar.update(desc);
        --active_threads;
        cv.notify_one();
    };
    
    std::vector<std::thread> threads;
    for (auto& [instrument_1, filepath_1]: instrument_filepath_map) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [&active_threads]{ return active_threads < Constants::MAX_THREADS; });

        ++active_threads;
        threads.emplace_back(find_cointegration, instrument_1, filepath_1);
    }
    progress_bar.done();

    for (auto& thread: threads) {
        if (thread.joinable()) {
            thread.join();
        }
    }

    sort(cointegration_result.begin(), cointegration_result.end(), [](std::vector<std::string>& a, std::vector<std::string>& b){
        return std::stoi(a[2]) > std::stoi(b[2]);
    });
    std::vector<std::string> header = {"Instrument 1", "Instrument 2", "Crossover Count", "Filepath 1", "Filepath 2"};
    cointegration_result.insert(cointegration_result.begin(), header);

    Utils::write_csv(Constants::OUTPUT_FILEPATH, cointegration_result);
}
