
# Memristor Simulation using the Biolek Model

## 📌 Overview
This project models and simulates a memristor based on the Biolek model. The simulation is implemented in Python and demonstrates the characteristic **pinched hysteresis loop** in the I-V curve—a hallmark of memristive behavior. This work is aligned with Challenge #28 for modeling emerging neuromorphic devices.

## 📄 Files in This Repository
| File              | Description |
|-------------------|-------------|
| `code.py`         | Python implementation of the Biolek memristor model |
| `Output_Graph.png`| Generated I-V curve showing the pinched hysteresis loop |
| `Findings.docx`   | Report summarizing the simulation setup, parameters, results, and observations |

## 🔬 Key Features
- Biolek window function to avoid boundary lock in dopant drift
- Support for sinusoidal voltage input simulation
- Time-step based state update of internal variable
- Visualization of I-V characteristics using `matplotlib`

## 📈 Result
The `Output_Graph.png` confirms the correct behavior of the memristor model. The plot shows a pinched hysteresis loop—a nonlinear I-V relationship—validating the memory-dependent behavior of the simulated device.

## 🚀 How to Run
1. Make sure you have Python 3 installed.
2. Install required library:
   ```bash
   pip install matplotlib numpy
   ```
3. Run the simulation:
   ```bash
   python code.py
   ```

## 📚 Reference
Biolek, D., Biolek, Z., & Biolková, V. (2009). **SPICE Model of Memristor with Nonlinear Dopant Drift**. Radioengineering, 18(2), 210–214.  
[PDF Link](https://www.radioeng.cz/fulltexts/2009/09_02_210_214.pdf)
