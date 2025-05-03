%%writefile saxpy.cu
#include <stdio.h>
#include <cuda_runtime.h>
#include <chrono>
#include <fstream>

__global__
void saxpy(int n, float a, float *x, float *y)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = a * x[i] + y[i];
}

int main() {
    int sizes[] = {15,16,17,18,19,20,21,22,23,24,25};
    std::ofstream fout("saxpy_times.csv");

    for (int s = 0; s < 11; ++s) {
        int N = 1 << sizes[s];
        float *x, *y, *d_x, *d_y;

        cudaMallocHost(&x, N * sizeof(float));
        cudaMallocHost(&y, N * sizeof(float));

        for (int i = 0; i < N; i++) {
            x[i] = 1.0f;
            y[i] = 2.0f;
        }

        cudaMalloc(&d_x, N * sizeof(float));
        cudaMalloc(&d_y, N * sizeof(float));

        cudaMemcpy(d_x, x, N * sizeof(float), cudaMemcpyHostToDevice);
        cudaMemcpy(d_y, y, N * sizeof(float), cudaMemcpyHostToDevice);

        int threadsPerBlock = 256;
        int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;

        cudaDeviceSynchronize();
        auto start = std::chrono::high_resolution_clock::now();

        saxpy<<<blocksPerGrid, threadsPerBlock>>>(N, 2.0f, d_x, d_y);

        cudaDeviceSynchronize();
        auto end = std::chrono::high_resolution_clock::now();

        std::chrono::duration<double> elapsed = end - start;

        printf("2^%d: %f seconds\n", sizes[s], elapsed.count());  // 👈 Console output
        fout << "2^" << sizes[s] << "," << elapsed.count() << std::endl;

        cudaFree(d_x);
        cudaFree(d_y);
        cudaFreeHost(x);
        cudaFreeHost(y);
    }

    fout.close();
    return 0;
}
