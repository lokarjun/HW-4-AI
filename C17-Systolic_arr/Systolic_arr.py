import random
import time
import matplotlib.pyplot as plt

# Processing Element class
class ProcessingElement:
    def __init__(self, value):
        self.value = value

# Systolic bubble sort simulation
def systolic_bubble_sort(data):
    n = len(data)
    pes = [ProcessingElement(val) for val in data]

    for pass_num in range(n):
        start = 0 if pass_num % 2 == 0 else 1
        for i in range(start, n - 1, 2):
            if pes[i].value > pes[i + 1].value:
                pes[i].value, pes[i + 1].value = pes[i + 1].value, pes[i].value

    return [pe.value for pe in pes]

# Measure time for a given input size
def measure_sort_time(size):
    data = [random.randint(0, 10000) for _ in range(size)]
    start = time.time()
    systolic_bubble_sort(data)
    end = time.time()
    return end - start

# Sizes to test
input_sizes = [10, 100, 1000, 10000]
execution_times = []

# Collect execution times
for size in input_sizes:
    print(f"Sorting size {size}...")
    exec_time = measure_sort_time(size)
    execution_times.append(exec_time)

# Plot the results
plt.figure()
plt.plot(input_sizes, execution_times, marker='o')
plt.title("Systolic Bubble Sort Execution Time")
plt.xlabel("Input Size")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.show()
