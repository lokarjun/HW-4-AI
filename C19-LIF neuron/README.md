
# Challenge 19: Binary Leaky Integrate-and-Fire (LIF) Neuron

This project is a hardware implementation of a simplified **Binary Leaky Integrate-and-Fire (LIF) Neuron** using SystemVerilog. It models the behavior of a spiking neuron by integrating inputs over time, applying a decay (leak), and firing a binary output spike when a threshold is reached.

---

## 📚 Project Description

### Binary LIF Neuron Model:
- **State:** `S(t)` ∈ {0, 1} — spike or no spike
- **Potential update rule:**  
  `P(t) = λ * P(t-1) + I(t)`  
  where `λ` is the leak factor (0 < λ < 1), `I(t)` is the binary input
- **Threshold condition:**  
  `S(t) = 1` if `P(t) ≥ θ`, otherwise `S(t) = 0`
- **Reset:**  
  After a spike, the potential `P(t)` resets

---

## 📁 Files

| File Name              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `Design.sv`            | SystemVerilog implementation of the binary LIF neuron                      |
| `TB.sv`                | Testbench covering 4 scenarios (below threshold, gradual spike, leakage, strong input) |
| `Findings`             | Summary of learning outcomes, design challenges, and LLM-guided debugging  |
| `Transcript_output.txt`| Console log output of the simulation showing potential and spike activity  |

---

## 🧪 How to Simulate

To run the simulation:
1. Use ModelSim, QuestaSim, or any other SystemVerilog simulator
2. Compile the design and testbench:
   ```bash
   vlog Design.sv TB.sv
   vsim lif_neuron_tb
   run -all
   ```
3. Observe the waveform (`.vcd`) or console outputs (`Transcript_output.txt`)

---

## ✅ Test Scenarios

The testbench validates the neuron behavior across these conditions:
1. **Constant low input** — No spike should occur.
2. **Gradual accumulation** — Repeated inputs should cause a spike once the threshold is crossed.
3. **Leakage** — In the absence of input, potential should decay toward zero.
4. **Strong input** — Immediate spike should occur if input is large enough.

---

## 🔍 Key Learnings

- Implemented a digital model of spiking neurons using fixed-point arithmetic
- Tuned the leak factor, input increments, and threshold for realistic spiking behavior
- Debugged design and timing issues using waveform traces and LLM-guided reasoning
- Used a large language model (LLM) to clarify behavioral bugs, correct assignment timing, and design an effective testbench

---

## 📌 Notes

- Fixed-point format: 8.8 (8 integer bits, 8 fractional bits)
- Leak factor (`λ`) and threshold (`θ`) are parameterized for easy tuning
- All values are updated and compared at the rising edge of the clock

---

## 🚀 Author

Lokarjun Ramesh – Master's in Electrical and Computer Engineering, PSU  
Challenge #19 – Hardware for AI/ML coursework

---
