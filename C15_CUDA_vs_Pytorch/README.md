
# Challenge #16: Benchmarking SAXPY with PyTorch

Google Collab link - https://colab.research.google.com/drive/17fpNlgyAQcUHFgNEI1W2dXSeyR8uCZtN?usp=sharing

## Overview
This project compares the performance of a simple feed-forward neural network (FFNN) accelerated with **CUDA** vs **PyTorch**. The neural network is fully connected, with 4 inputs, 5 hidden neurons, and 1 output. The challenge involves coding both a **CUDA-accelerated** version and a **PyTorch** version of the network, benchmarking their execution times for different configurations of the network's width and depth, and comparing the results.

## Learning Goals
- **Code a CUDA-accelerated version** of a simple multi-layer feed-forward network.
- **Code the same network using PyTorch** for comparison.
- **Benchmark both implementations** and compare their performance.
- **Experiment with different network configurations** (changing depth and width) and compare execution times for each framework.

## Tasks
1. Code the **CUDA-accelerated** version of the FFNN.
2. Code the **PyTorch version** of the same network.
3. Benchmark both implementations and compare their performance.
4. **Increase the depth and width of the network** and compare execution times for various sizes.

## Findings
- **CUDA** showed strong performance when the network's size (depth and width) increased due to efficient matrix computation. However, **PyTorch** was more efficient for smaller configurations, where its overhead for GPU setup and data transfer became negligible.
- The performance of both models varies depending on the **size** of the network. CUDA's advantage becomes more prominent as the network becomes larger due to the parallel nature of its computation.
- **PyTorch**, while abstracting hardware management, is optimized for rapid development and testing and provides good results on smaller models.

## Problems Faced
- Initially, there was an issue with **empty CUDA times**, which caused errors during plotting. The issue was resolved by ensuring that CUDA execution times were correctly captured after each kernel run.
- The **dimensional mismatch** error when plotting the results was solved by ensuring that the `cuda_times` list was populated correctly with execution times.

## How LLMs Helped
- **Error Fixing**: I used large language models (LLMs) like ChatGPT to troubleshoot issues related to benchmarking, understanding CUDA memory management, and fixing plotting errors when `cuda_times` was empty.
- **Optimization Advice**: LLMs helped me understand the differences in performance between PyTorch and CUDA and guided me on when to use each framework depending on the network configuration.

## Conclusion
This challenge provided insights into:
- The complexities of **low-level CUDA programming** for neural network acceleration.
- The ease and flexibility of **high-level frameworks** like PyTorch, which abstract hardware management.
- The trade-offs between using a low-level framework like CUDA for large models and using a high-level framework like PyTorch for quick experimentation and smaller models.

### Technologies Used
- **CUDA** for GPU acceleration
- **PyTorch** for neural network implementation and benchmarking
- **Python** for benchmarking and plotting results using `matplotlib`

## Files
1. **cuda_benchmark.cpp**: The CUDA implementation for the benchmarked neural network.
2. **pytorch_benchmark.py**: The PyTorch implementation for the benchmarked neural network.
3. **Summary of the challenge**: Documentation for the challenge.

