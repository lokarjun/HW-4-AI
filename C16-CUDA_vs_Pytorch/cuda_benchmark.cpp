%%writefile cuda_benchmark.cu
#include <iostream>
#include <cmath>
#include <cuda_runtime.h>
#include <vector>
#include <ctime>

#define N_INPUTS 4
#define N_OUTPUT 1

// CUDA Kernel to compute forward pass of neural network
__global__ void feedforward(float *inputs, float *weights_input_hidden, float *weights_hidden_output, 
                             float *bias_hidden, float *bias_output, float *output, int N_HIDDEN) {
    int idx = threadIdx.x;

    // Compute hidden layer outputs
    float *hidden_output = new float[N_HIDDEN];
    if (idx < N_HIDDEN) {
        hidden_output[idx] = 0.0f;
        for (int i = 0; i < N_INPUTS; i++) {
            hidden_output[idx] += inputs[i] * weights_input_hidden[i * N_HIDDEN + idx];
        }
        hidden_output[idx] += bias_hidden[idx];
        hidden_output[idx] = 1.0f / (1.0f + exp(-hidden_output[idx])); // Sigmoid activation
    }

    __syncthreads(); // Synchronize threads before calculating the output

    // Compute output layer
    if (idx == 0) {
        *output = 0.0f;
        for (int i = 0; i < N_HIDDEN; i++) {
            *output += hidden_output[i] * weights_hidden_output[i];
        }
        *output += *bias_output;
        *output = 1.0f / (1.0f + exp(-(*output))); // Sigmoid activation
    }
}

int main() {
    int N_HIDDEN = 100; // Number of neurons in hidden layer (width)
    int N_LAYERS = 3; // Number of hidden layers (depth)

    float inputs[N_INPUTS] = {1.0f, 0.5f, -1.5f, 0.8f};
    
    // Initialize weights and biases
    std::vector<float> weights_input_hidden(N_INPUTS * N_HIDDEN);
    std::vector<float> weights_hidden_output(N_HIDDEN);
    std::vector<float> bias_hidden(N_HIDDEN);
    float bias_output = 0.2f;

    // Initialize the weights and biases with some values
    for (int i = 0; i < N_INPUTS * N_HIDDEN; i++) {
        weights_input_hidden[i] = 0.1f * i;
    }
    for (int i = 0; i < N_HIDDEN; i++) {
        weights_hidden_output[i] = 0.2f * i;
        bias_hidden[i] = 0.1f * i;
    }

    float *d_inputs, *d_weights_input_hidden, *d_weights_hidden_output, *d_bias_hidden, *d_bias_output, *d_output;
    float output;

    // Allocate memory on device
    cudaMalloc((void**)&d_inputs, N_INPUTS * sizeof(float));
    cudaMalloc((void**)&d_weights_input_hidden, N_INPUTS * N_HIDDEN * sizeof(float));
    cudaMalloc((void**)&d_weights_hidden_output, N_HIDDEN * sizeof(float));
    cudaMalloc((void**)&d_bias_hidden, N_HIDDEN * sizeof(float));
    cudaMalloc((void**)&d_bias_output, sizeof(float));
    cudaMalloc((void**)&d_output, sizeof(float));

    // Copy data to device
    cudaMemcpy(d_inputs, inputs, N_INPUTS * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_weights_input_hidden, weights_input_hidden.data(), N_INPUTS * N_HIDDEN * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_weights_hidden_output, weights_hidden_output.data(), N_HIDDEN * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_bias_hidden, bias_hidden.data(), N_HIDDEN * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_bias_output, &bias_output, sizeof(float), cudaMemcpyHostToDevice);

    // Create CUDA events to measure time
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    // Record start time
    cudaEventRecord(start);

    // Launch the kernel with 1 block and N_HIDDEN threads
    feedforward<<<1, N_HIDDEN>>>(d_inputs, d_weights_input_hidden, d_weights_hidden_output, d_bias_hidden, d_bias_output, d_output, N_HIDDEN);

    // Record stop time
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    // Copy the output back to host
    cudaMemcpy(&output, d_output, sizeof(float), cudaMemcpyDeviceToHost);

    // Calculate elapsed time
    float elapsedTime;
    cudaEventElapsedTime(&elapsedTime, start, stop);

    std::cout << "Time taken for the forward pass (in milliseconds): " << elapsedTime << " ms" << std::endl;

    // Free device memory and events
    cudaFree(d_inputs);
    cudaFree(d_weights_input_hidden);
    cudaFree(d_weights_hidden_output);
    cudaFree(d_bias_hidden);
    cudaFree(d_bias_output);
    cudaFree(d_output);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    return 0;
}
