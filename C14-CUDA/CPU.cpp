%%writefile fibonacci.cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>

#define N (1 << 18)

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    std::vector<unsigned long long> fib(N);
    fib[0] = 0;
    fib[1] = 1;

    for (int i = 2; i < N; ++i) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> duration_ms = end - start;

    // Save to file
    std::ofstream fout("cpu_time.txt");
    fout << duration_ms.count();
    fout.close();

    return 0;
}
