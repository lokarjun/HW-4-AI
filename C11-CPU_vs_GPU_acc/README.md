# Challenge #11: GPU Acceleration of Q-Learning (FrozenLake)

This project is part of Challenge #11 in a GPU acceleration learning series. The task involves optimizing a Python-based Q-learning agent for the FrozenLake grid environment by porting it to a CUDA-based GPU implementation and benchmarking the performance difference.

Google collab link - https://colab.research.google.com/drive/1-DYilLFrlyibDPobUvCz_Ew-KaNZa3Bq?usp=sharing

## 🔍 Objective

- Convert the Python version of Q-learning into a GPU-accelerated version using CUDA.
- Run both versions for increasing episode sizes (1000, 5000, 10000).
- Measure execution times for each and compare the performance using a log-scale bar chart.

## 🧠 Learning Goals

- Understand limitations of sequential RL algorithms when ported to parallel architectures.
- Learn how to use CUDA to implement and benchmark kernels.
- Practice measuring performance realistically, including overheads.
- Visualize execution times and interpret results critically.

## 🗂 Files Included

- `Pure_Python.py` – Original CPU Python implementation with benchmark logging.
- `Gpu_acc.cu` – CUDA version of the Q-learning algorithm for GPU execution.
- `plot` –  plot that shows execution time comparisons on a logarithmic scale.


## 📊 Sample Benchmark Output

| Episodes | CPU Time (s) | GPU Time (s) |
|----------|--------------|--------------|
| 1000     | 0.0156       | 0.000014     |
| 5000     | 0.0530       | 0.000009     |
| 10000    | 0.0748       | 0.000008     |

> ⚠️ Note: GPU times reflect only kernel execution. They do not include memory allocation or transfer overhead. CPU version includes Python interpreter overhead.

## 📌 Insights

- The GPU implementation shows significant numerical speed-up, but the gain is partly due to interpreter overhead in Python.
- The Q-learning logic is inherently sequential and control-heavy, which limits GPU parallelism.
- Proper benchmarking must include all overheads to yield fair comparisons.
- True GPU acceleration benefits are better realized in batch-parallel RL setups or vectorized environments.

## ✅ Conclusion

This challenge demonstrated how even control-heavy RL algorithms can be mapped to GPU kernels and benchmarked effectively. However, it also highlighted the importance of realistic performance measurement and a deeper understanding of architectural trade-offs in hardware acceleration.