import matplotlib.pyplot as plt

labels = [f"2^{i}" for i in range(15, 26)]
times = [0.007889, 0.000003, 0.000002, 0.000002, 0.000003,
         0.000002, 0.000002, 0.000003, 0.000004, 0.000005, 0.000006]

plt.figure(figsize=(12, 6))
plt.bar(labels, times)
plt.yscale('log')  # ✅ Use logarithmic scale
plt.xlabel("Input Size (N)")
plt.ylabel("Execution Time (log scale, seconds)")
plt.title("CUDA SAXPY Execution Time (Log Scale)")
plt.grid(True, which="both", linestyle='--')
plt.show()