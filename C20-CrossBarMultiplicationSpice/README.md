# Challenge #20: Resistive Crossbar Matrix-Vector Multiplication

## 📌 Objective

The objective of this challenge was to implement and simulate a 4×4 resistive crossbar matrix for analog matrix-vector multiplication using SPICE. The circuit design emulates a dot product between a 4×1 input voltage vector and a 4×4 resistor-based weight matrix. The result is observed in the form of output currents from each column node.

---

## ⚙️ Implementation Details

- A 4×4 resistive crossbar was created using SPICE netlist format.
- Each row receives a voltage input representing a vector element.
- Each crosspoint in the matrix includes a fixed resistor encoding weight.
- Each output column is connected to ground via a 1-ohm resistor to measure output current.
- Simulations were performed using **Ngspice** within **Google Colab**.
- Python (`subprocess`) was used to call the SPICE simulation and parse the output.

---

## 🧪 Results

The node voltages at each column were extracted and used to compute current (since \( R = 1\,\Omega \), \( I = V \)). This yielded the matrix-vector multiplication result.

Example output:
```
col1 → 1.245640 V → 1.245640 A  
col2 → 0.996512 V → 0.996512 A  
col3 → 1.245640 V → 1.245640 A  
col4 → 1.494024 V → 1.494024 A  
```

---

## 🐞 Challenges Faced

- `.print v(colX)` did not work reliably due to node resolution timing.
- This was resolved by switching to `.control` blocks with `op` and `print all` to ensure node voltages were printed in batch mode.

---

## ✅ Achievements

- Successfully simulated a resistive crossbar circuit in SPICE.
- Computed matrix-vector multiplication results by analyzing voltage drop across known resistors.
- Integrated Ngspice with Python in Google Colab for cloud-based simulation and data extraction.

---

## 🔗 Google Colab Notebook

https://colab.research.google.com/drive/17HuCBglGQlNK5bTqgHoXPlr4d6YAIYU9?usp=sharing

---

## 📁 Files Included

- `Findings`: Documenatation of the findings
- `README.md`: This file

---

## 🧠 Learnings

This challenge demonstrated how analog computation such as matrix-vector multiplication can be modeled using SPICE and simulated interactively with Python. It also highlighted how to troubleshoot node visibility issues in SPICE output and parse simulation data programmatically.

