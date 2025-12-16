#include <stdio.h>
#include <time.h>

// Simple timing function for benchmarking
double get_elapsed_time() {
    static double start_time = 0;
    if (start_time == 0) {
        start_time = (double)clock() / CLOCKS_PER_SEC;
        return 0;
    } else {
        double current = (double)clock() / CLOCKS_PER_SEC;
        return current - start_time;
    }
}

void reset_timer() {
    // Reset by setting static var, but since static, hard. For simplicity, use global.
}