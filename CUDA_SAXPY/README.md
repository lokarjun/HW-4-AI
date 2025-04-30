# Challenge #13: CUDA SAXPY Benchmarking

Google Collab Link - https://colab.research.google.com/drive/1vd__hiEtBtgNc3en1ONEcAtwTgLw-I01?usp=sharing

## 🚀 Objective
The goal of this challenge was to explore and benchmark the performance of the SAXPY operation (`y = a*x + y`) using CUDA on increasing input sizes. This included profiling kernel execution, measuring memory transfer times, and visualizing the results to understand how GPU efficiency scales with problem size.

## 🎯 Learning Goals
- Set up a working CUDA development environment.
- Modify and extend existing CUDA sample code.
- Benchmark performance across increasing matrix sizes.
- Visualize performance trends and understand GPU utilization patterns.
- Use profiling techniques (like `cudaEvent`) to separate memory and compute timing.

## 🛠 Environment
- **Platform**: Google Colab
- **GPU**: T4 GPU
- **Compiler**: `nvcc` for `.cu` files
- **Visualization**: Python + Matplotlib

## 📊 Methodology
- Used raw CUDA C++ SAXPY code from [NVIDIA's blog](https://developer.nvidia.com/blog/easy-introduction-cuda-c-and-c).
- Modified the kernel driver to benchmark for matrix sizes from `2^15` to `2^25`.
- Measured:
  - Total execution time (including memory transfers)
  - Pure kernel execution time (via `cudaEvent`)
- Results were written to a CSV file and plotted using Python.

## 📈 Observations
- Execution time for smaller inputs was dominated by overhead (e.g., kernel launch).
- Larger inputs showed near-constant execution due to parallelism scaling.
- Logarithmic plotting was essential to reveal performance trends.
- Kernel-only timing was significantly smaller than total timing for smaller input sizes.

## 🤖 How GPT Helped
GPT-4 assisted in:
- Debugging CuPy/Numba installation issues in Colab.
- Suggesting a fallback to `.cu` file + `nvcc` compilation.
- Adding CSV logging and `printf()` for benchmarking output.
- Writing a Python plotting script with fixes for log-scale visualization and annotations.
- Structuring final documentation and insights.

## 📂 Files Included
- `saxpy.cu`: Modified CUDA kernel code
- `saxpy_exec`: Compiled CUDA binary (created in Colab)
- `Execution_output`: Benchmark results
- `plot.py`: Python script for visualizing timing data

## 📌 Conclusion
This challenge provided hands-on experience with CUDA development, profiling, and performance analysis. It also highlighted the impact of problem size on GPU efficiency and the importance of separating memory transfer vs. kernel execution when benchmarking.

---

