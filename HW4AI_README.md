
# 📐 Hardware for AI — Complete Course Repository

This repository captures my work for **ECE 410/510: Hardware for AI**, combining **weekly hands-on design challenges** and a comprehensive **final project** focused on a hardware-software co-design of the **ChaCha20 stream cipher accelerator**.

## 📁 Repository Structure

- **Weekly Challenges (C1–C28)**  
  Each folder documents an individual challenge tackling topics like:
  - Beyond-CMOS architectures
  - Systolic arrays
  - Crossbar multiplication
  - Perceptron training
  - LIF neurons and memristors
  - CPU vs. GPU vs. PyTorch acceleration
  - SPI throughput benchmarking
  - Many other hardware design experiments

  Each challenge includes well-commented code, test results, and quick documentation.

- **Final Project: ChaCha20 Hardware Accelerator**
  A hardware-software co-design using:
  - Python for the reference cipher and SPI interface
  - SystemVerilog for the hardware core and wrapper
  - Cocotb for co-simulation
  - OpenLane for ASIC synthesis and performance metrics

  The project demonstrates benchmarking, profiling, hardware acceleration, and practical trade-offs for deploying cryptographic workloads as chiplets.

## 📐 Chiplet Architecture

Below is a conceptual diagram showing how the ChaCha20 accelerator integrates into a larger AI/ML chiplet system:

```
┌─────────────────────────────┐
│  Software SPI Driver        │
│  (Python interface)         │
├─────────────────────────────┤
│  ChaCha20 Core Accelerator  │
│  (SystemVerilog IP)         │
├─────────────────────────────┤
│  Wrapper for I/O Management │
└─────────────────────────────┘
```

## ✅ How to Use

1. **Clone this repository:**
   ```bash
   git clone https://github.com/lokarjun/HW-4-AI.git
   cd HW-4-AI
   ```

2. **Run Weekly Challenges:**  
   Each challenge folder contains its own README or Makefile.

3. **Run Final Project:**  
   - Benchmark the Python cipher
   - Run Cocotb co-simulation with the hardware core
   - Synthesize with OpenLane and analyze power, area, and frequency

   Detailed instructions are in the `Project` folder.

## 📊 Highlights

| Metric | Value |
| ------ | ----- |
| Python-only execution (2MB) | ~52.8 seconds |
| Hardware-accelerated execution (2MB) | ~10 seconds (including SPI transfer) |
| Synthesis max frequency | ~100 MHz |
| Die Area | 172,005 µm² |
| Total Power | ~0.027 mW |
| Transistor Count | Inferred from standard cell count and utilization |

## 🤝 Credits

- Based on starter codes, course material, and open-source Python ChaCha20 implementations.
- ChatGPT assisted in brainstorming, commenting, and documentation.

## 📜 License

This repo is for educational purposes for the **Hardware for AI** course at Portland State University.

---
