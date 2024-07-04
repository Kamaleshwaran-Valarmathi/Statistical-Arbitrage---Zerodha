#pragma once

#include <string>


namespace Constants {
    const std::string INPUT_FOLDER_PATH = "../../resources/random_data/"; // TEST
    // const std::string INPUT_FOLDER_PATH = "../resources/historic_data/"; // PROD
    const std::string OUTPUT_FILEPATH = "../../resources/cointegration_result.csv";

    const int MAX_THREADS = int(std::thread::hardware_concurrency());
    const double FEE = 0.01; // TEST
    const int WINDOW_SIZE = 21;
}
