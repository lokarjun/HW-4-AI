# Challenge #4: LLM-Assisted Design of a Programmable Spiking Neuron Array ASIC

## Overview

This project explores the use of Large Language Models (LLMs), specifically ChatGPT, to assist in the digital hardware design of a programmable spiking neuron array. Inspired by the Johns Hopkins paper ["Designing Silicon Brains using LLM"](https://arxiv.org/abs/2402.10920), the project demonstrates the ability of conversational AI to generate, refine, and structure Verilog modules for a neuromorphic system.

## Learning Goals

- Experiment with LLM-assisted chip design
- Understand the challenges of “vibe coding” in hardware
- Install and test an end-to-end hardware design flow
- Compare generated designs with research literature
- Propose improvements and variations (e.g., using RLU or Hodgkin-Huxley neuron models)

## Project Files

| File Name           | Description |
|---------------------|-------------|
| `Design.sv`         | SystemVerilog module implementing the complete neural network (LIF-based spiking neurons, layers, and connectivity). |
| `TB.sv`             | Testbench to simulate the SPI configuration and neuron behavior. |
| `Documentation.docx`| Project report including design architecture, module descriptions, and development process using ChatGPT. |
| `Prompts.docx`      | List of natural language prompts used during the iterative ChatGPT-based design process. |
| `2402.10920v1.pdf`  | Original Johns Hopkins paper describing the methodology used to generate a spiking neuron ASIC with LLMs. |

## Project Components

### 1. Spiking LIF Neuron
- Verilog module implementing a **Leaky Integrate-and-Fire** (LIF) neuron.
- Supports multibit input current.
- Incorporates programmable threshold, leak rate, and refractory period.

### 2. Two-Layer Spiking Neural Network (SNN)
- Fully connected network of neurons.
- Programmable synaptic weights.
- Input spikes transformed into weighted input currents.

### 3. Programmable Register File
- Stores neuron parameters and synaptic weights.
- Externally programmable via SPI interface.

### 4. SPI Interface
- SPI slave for loading configuration values.
- Address-based decoding for register file updates.

### 5. Top-Level Module
- Integrates SPI, Register File, and SNN into a cohesive programmable system.

### 6. Testbench
- Stimulates the SPI and input data.
- Validates the spiking behavior of the neural network.

## Development Approach

All Verilog modules were co-developed interactively with ChatGPT using natural language prompts. Errors such as syntax issues, unsupported SystemVerilog features, and logic flaws were iteratively fixed through prompt refinement and manual debugging.

### Prompts Used
Some examples:
- "Can you write a verilog module for a spiking leaky integrate and fire neuron?"
- "Create a new module that instantiates a network of neurons with 2 layers in a fully connected fashion."
- "I think there is an issue with the 2D array while connecting neurons. Please rectify it."
- "Create an SPI interface to communicate with the network module above."

The full set is available in `Prompts.docx`.

## Findings

- ChatGPT accelerates module prototyping, but requires expert oversight.
- Generated code often mixes Verilog and SystemVerilog syntax, which must be corrected.
- LLMs show potential as design assistants, especially for early-stage and repetitive tasks.

## Future Work

- Swap LIF neurons with RLU or Hodgkin-Huxley models.
- Add learning or plasticity features.
- Fabricate design using **OpenLane** and **Tiny Tapeout** workflows.

## References

- [Designing Silicon Brains using LLM](https://arxiv.org/abs/2402.10920)
- [TinyTapeout Project](https://tinytapeout.com/)
- [OpenLane ASIC Flow](https://www.zerotoasiccourse.com/terminology/openlane)

---

