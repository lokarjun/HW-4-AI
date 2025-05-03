
# Challenge 10: Identifying and Accelerating Computational Bottlenecks in Q-Learning

## Overview

This project focuses on identifying computational bottlenecks in a Python-based Q-learning agent for a simplified **FrozenLake**-style grid environment. Using profiling tools and LLM analysis, we pinpoint the most performance-critical sections of the code and propose a **hardware accelerator** using SystemVerilog to address the bottleneck.

## Objectives

1. Analyze and profile the FrozenLake Q-learning agent.
2. Use an LLM to detect performance bottlenecks in the code.
3. Evaluate whether the suggestions make sense.
4. Implement a hardware module in **SystemVerilog** to accelerate the worst-performing section of the algorithm.

## Files

- `Code.py` — Python implementation of the Q-learning agent, instrumented with `cProfile`.
- `Profiler_Output.txt` — Profiler log showing execution times and bottlenecks.
- `Findings.docx` — Summary of bottleneck analysis and rationale for proposed hardware acceleration.
- `SV_Code.sv` — SystemVerilog module implementing a parallel Q-value max selector.

## Environment

- Python 3.x
- NumPy
- Matplotlib
- cProfile (standard Python profiler)

To install dependencies:

```bash
pip install numpy matplotlib
```

## How to Run

Profile and run the Q-learning agent using:

```bash
python Code.py
```

This will:
- Train the agent on a 5x5 FrozenLake grid.
- Output the Q-table and plot cumulative rewards.
- Print profiler results indicating time spent per function.

## Bottleneck Analysis

According to both manual profiling and LLM assistance, the main computational bottlenecks are:

- **Linear search over Q-values**: Selecting the best action at every step by looping over four possible actions.
- **Redundant deep copies** of the Q-table (`dict.copy()` called ~93,000 times).
- **Reward and end-state evaluation** happening multiple times per step.

The most critical issue is the repeated search over Q-values to find the best action. This was identified as the **main target for hardware acceleration**.

## Hardware Acceleration

A hardware module was implemented in **SystemVerilog** that:

- Takes in four 16-bit Q-values.
- Compares them in parallel using combinational logic.
- Outputs the **maximum Q-value** and its corresponding **action index** (2-bit encoded).

This **Q-value Max Selector Module** enables near-instantaneous decision-making in environments where real-time performance is critical (e.g., embedded agents).

## Key Learnings

- Profiling is essential to uncover non-obvious bottlenecks.
- LLMs can accurately assist in identifying optimization opportunities.
- Hardware acceleration of even simple components (like max selectors) can greatly improve performance in AI workloads.
- Modular Verilog code can be tightly integrated with Python-based RL agents in co-design systems.


