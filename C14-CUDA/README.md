# Challenge 14: Parallel Fibonacci Computation Using CUDA

## 🚀 Challenge Overview

**Challenge 14** focuses on computing the **Fibonacci sequence** for a given number `N` (e.g., 2^20) using:
- A **sequential CPU implementation**
- A **parallel CUDA GPU kernel**

This challenge introduces students to **parallel computation with CUDA**, performance measurement, and comparison with traditional CPU-based methods.

---

## 📚 What is the Fibonacci Sequence?

The Fibonacci sequence is defined as:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for all n ≥ 2

Example sequence:  
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

---

## 🧠 Learning Objectives

- Understand how to implement **basic numerical algorithms** (like Fibonacci) in both CPU and GPU environments.
- Learn to write **CUDA kernels** for parallel computation.
- Measure and compare **performance** using timing utilities (`chrono` for CPU, `cudaEvent` for GPU).
- Generate and interpret **execution time plots** for CPU vs GPU.

---

## 📁 Project Structure

```
├── CPU.cpp           # CPU-only C++ implementation
├── CUDA.cu            # CUDA C++ GPU implementation
├── cpu_op.txt            # Output file containing CPU execution time
├── gpu_op.txt            # Output file containing GPU execution time
├── plotting.py         # Python script to visualize performance comparison
├── README.md               # This file
```

---

## 🛠️ How to Run

1. Compile the programs (`g++` and `nvcc`).
2. Execute both CPU and GPU binaries.
3. Observe timing output in respective `.txt` files.
4. Use `plot_results.py` to generate a performance comparison graph.
https://colab.research.google.com/drive/1fhUo7SbhT9fFWJsdhuglvyYB0eAddIw9?usp=sharing
I have included a link to my google collab where you can run the code and see output.
---

## 📊 What We Observed

| Metric           | CPU              | GPU              |
|------------------|------------------|------------------|
| Parallelism      | ❌ Sequential     | ✅ Parallel       |
| Memory Use       | Low              | Higher (device memory) |
| Execution Time   | Slower           | Faster (for large N)   |
| Overhead         | None             | Launch + Copy Overhead |
| Efficiency       | Good for small N | Best for large N       |

### 📌 Conclusion:
- GPU is **much faster** for **large N** due to parallel execution.
- CPU is **simpler and faster** for **small N** due to lower overhead.
- Choosing **the right architecture for the workload** is essential in high-performance computing.

---

## 🔄 Possible Extensions

- Add support for dynamic `N` input
- Compare multiple `N` values and graph trends
- Explore optimization using shared memory
- Investigate recursive vs iterative strategies

---

## ✅ Outcome

By completing this challenge, we gained insights into:
- Writing and running CUDA programs
- Comparing sequential and parallel performance
- Profiling execution time on CPU vs GPU

This builds foundational skills for hardware acceleration and parallel programming.