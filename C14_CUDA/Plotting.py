import matplotlib.pyplot as plt

# Read times
with open("gpu_time.txt", "r") as f:
    gpu_time = float(f.read())

with open("cpu_time.txt", "r") as f:
    cpu_time = float(f.read())

# Plot
labels = ['CPU', 'GPU']
times = [cpu_time, gpu_time]

plt.figure(figsize=(6, 4))
plt.bar(labels, times)
plt.ylabel("Execution Time (ms)")
plt.title("Fibonacci Calculation Time (N = 2^18)")
plt.grid(True, axis='y')
plt.show()
