
# Challenge #17: Sorting on a Systolic Array


Google Collab Link - https://colab.research.google.com/drive/1R5FG48EZ1xIYfiZZZHABQUroRIsAz3YO?usp=sharing

## 🧠 Overview

This challenge explores how to implement the Bubble Sort algorithm using a **systolic array** architecture and evaluate its performance as the input size grows. The systolic array simulates parallel, hardware-style execution in software using Python.

---

## 🎯 Learning Goals

- Understand how to implement Bubble Sort using a 1D systolic array.
- Simulate systolic data movement and local computation in software.
- Evaluate performance as a function of problem size.
- Visualize execution time for increasing dataset sizes (10, 100, 1000, 10000).

---

## ⚙️ Design Summary

- A **1D systolic array** was used, with each element of the array mapped to a **Processing Element (PE)**.
- Each PE holds a value and compares/sorts with its neighbor in each step.
- Alternate "even" and "odd" passes simulate the rhythmic data movement across the systolic array.
- The software mimics this using alternating compare-and-swap logic across the array.

---

## 🚀 How to Run the Code

1. Clone the repository or download the Python script:
   ```bash
   git clone <your-repo-url>
   cd challenge17_systolic_sort
   ```

2. Install required packages:
   ```bash
   pip install matplotlib
   ```

3. Run the script:
   ```bash
   python systolic_bubble_sort.py
   ```

4. The script will:
   - Simulate systolic bubble sort.
   - Measure execution time for input sizes: 10, 100, 1000, and 10000.
   - Plot the execution times using `matplotlib`.

---

## 📈 Visualization

A plot will be generated showing execution time (Y-axis) vs. input size (X-axis). Due to the `O(n²)` nature of Bubble Sort, expect a steep curve, especially from 1000 to 10000 inputs.

---

## 🧩 Observations

- Performance degrades quickly with larger datasets.
- Bubble Sort is inefficient for large inputs, especially in a sequential software simulation.
- Systolic arrays offer insight into hardware-accelerated sorting but aren't suited for large-scale, non-parallel workloads unless deeply optimized.

---

## 🤖 GPT's Role

- Helped clarify systolic array architecture suitable for Bubble Sort.
- Provided a Python simulation using object-oriented programming.
- Assisted with plotting and visualizing performance metrics.
- Guided decisions about CPU vs. TPU/GPU use for this simulation.

---

## 📎 Files

- `Systolic_arr.py`: Main simulation and timing code.
- `README.md`: This documentation.

---

## 📬 Contact

For questions or suggestions, feel free to reach out via GitHub Issues or contact Lokarjun Ramesh.
