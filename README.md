
# Hardware for AI and ML — ECE 410/510

This repository contains my complete weekly challenges and project work for the **Hardware for AI and Machine Learning** course (Spring 2025).

## 📚 **Course Overview**
This course explores how modern hardware architectures support AI and ML workloads. Topics covered include:
- Hardware-software co-design
- GPU programming for AI/ML
- Deep neural networks on GPUs
- Systolic arrays
- In-memory computation (trade-offs and advantages)
- Neuromorphic computing (TrueNorth, Loihi, Akida)
- Benchmarking and performance analysis

## ✅ **Contents**

### 🔬 **Weekly Challenges**
I completed **18 weekly challenges**, with some challenges merged into the comprehensive project to avoid redundancy. Each challenge folder contains code, results, and documentation:
- **C1**: Beyond CMOS
- **C2**: Intrinsic and designed computation
- **C3**: Physical systems solving differential equations
- **C4**: Neuron design using LLM
- **C6**: Perceptron learning NAND
- **C7**: Perceptron learning visualisation
- **C8**: Multi-layer feed-forward perceptron (XOR gate)
- **C10**: Computational Bottlenecks in Q-Learning (Frozen Lake)
- **C11**: CPU vs GPU acceleration
- **C13**: CUDA SAXPY
- **C14**: CUDA environment and performance scaling
- **C16**: CUDA vs PyTorch comparison
- **C17**: Systolic array bubble sort
- **C19**: Binary Leaky Integrate-and-Fire neuron in SystemVerilog
- **C20**: Crossbar Multiplication in SPICE
- **C22**: Research paper on neuromorphic computing
- **C26**: BrainChip Akida IP and TENN architecture
- **C28**: Memristor modeling and simulation in Python

### 📈 **Project**
**ChaCha20 Hardware Accelerator**
- Designed, verified (using Cocotb), benchmarked for various message sizes
- Achieved ~5× speedup compared to software implementation
- Completed physical synthesis using OpenLane with good performance results
- Demonstrates end-to-end hardware-software co-design and full toolchain usage


## 🔑 **Languages & Tools**
- **Python** — Algorithm prototyping, modeling, and simulation
- **SystemVerilog** — RTL design and verification
- **CUDA** — GPU-accelerated kernels and performance benchmarking
- **C++** — Supporting implementations and performance tests
- **SPICE** — Crossbar and analog component simulation

## 📂 **Repository Structure**
Each folder is organized by challenge number and topic for easy navigation. The `Project` folder contains the final integrated hardware accelerator design, verification scripts, benchmarks, and synthesis artifacts.

## 📜 **License**
This repository is for academic and demonstration purposes only.
