%%writefile fibonacci.cu
#include <stdio.h>
#include <cuda.h>
#include <chrono>
#include <fstream>

#define N (1 << 18)

__global__ void fibonacci(unsigned long long *fib) {
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    if (i == 0) fib[0] = 0;
    else if (i == 1) fib[1] = 1;
    else if (i < N) {
        unsigned long long a = 0, b = 1, c;
        for (int j = 2; j <= i; j++) {
            c = a + b;
            a = b;
            b = c;
        }
        fib[i] = b;
    }
}

int main() {
    auto wall_start = std::chrono::high_resolution_clock::now();

    unsigned long long *d_fib, *h_fib;
    size_t size = N * sizeof(unsigned long long);

    h_fib = (unsigned long long *)malloc(size);
    cudaMalloc(&d_fib, size);

    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    fibonacci<<<blocksPerGrid, threadsPerBlock>>>(d_fib);

    cudaMemcpy(h_fib, d_fib, size, cudaMemcpyDeviceToHost);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float kernel_time = 0;
    cudaEventElapsedTime(&kernel_time, start, stop);

    cudaFree(d_fib);
    free(h_fib);

    auto wall_end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> total_time = wall_end - wall_start;

    // Save total time to file
    std::ofstream fout("gpu_time.txt");
    fout << total_time.count();
    fout.close();

    return 0;
}
