#pragma once

#include <chrono>
#include <iomanip>
#include <iostream>
#include <string>


class ProgressBar {
public:
    ProgressBar(int total, const std::string& desc = "", int width = 100) 
        : total(total), width(width), start_time(std::chrono::steady_clock::now()) {
        print_progress(desc);
    }

    void update(const std::string& desc = "") {
        ++current;
        print_progress(desc);
    }

    void done() {
        std::cout << std::endl;
    }

private:
    int current = 0;
    int total;
    int width;
    std::chrono::steady_clock::time_point start_time;

    void print_progress(const std::string& desc = "") {
        float progress = static_cast<float>(current) / total;
        int bar_width = static_cast<int>(progress * width);

        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - start_time).count();

        std::string elapsed_time_str = format_duration(elapsed);

        std::cout << "\r" << desc << " [";
        for (int i = 0; i < bar_width; ++i) {
            std::cout << "=";
        }
        for (int i = bar_width; i < width; ++i) {
            std::cout << " ";
        }
        std::cout << "] " << static_cast<int>(progress * 100.0) << "%";
        std::cout << " - Elapsed Time: " << elapsed_time_str;
        std::cout.flush();
    }

    std::string format_duration(int total_seconds) {
        int hours = total_seconds / 3600;
        int minutes = (total_seconds % 3600) / 60;
        int seconds = total_seconds % 60;

        std::ostringstream oss;
        oss << std::setw(2) << std::setfill('0') << hours << ":"
            << std::setw(2) << std::setfill('0') << minutes << ":"
            << std::setw(2) << std::setfill('0') << seconds;

        return oss.str();
    }
};





// #pragma once

// #include <iostream>
// #include <string>


// class ProgressBar {
// public:
//     ProgressBar(int total, const std::string& desc = "", int width = 100) 
//         : total(total), width(width) {
//         print_progress(desc);
//     }

//     void update(const std::string& desc = "") {
//         ++current;
//         print_progress(desc);
//     }

//     void done() {
//         std::cout << std::endl;
//     }

// private:
//     int current = 0;
//     int total;
//     int width;

//     void print_progress(const std::string& desc = "") {
//         float progress = static_cast<float>(current) / total;
//         int bar_width = static_cast<int>(progress * width);

//         std::cout << "\r" << desc << " [";
//         for (int i = 0; i < bar_width; ++i) {
//             std::cout << "=";
//         }
//         for (int i = bar_width; i < width; ++i) {
//             std::cout << " ";
//         }
//         std::cout << "] " << static_cast<int>(progress * 100.0) << "%";
//         std::cout.flush();
//     }
// };
