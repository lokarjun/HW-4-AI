
# Challenge 6: Perceptron Logic Gate Learning

## Overview

This project demonstrates how to implement a simple perceptron (a single-layer neural network) with two inputs and a sigmoid activation function, and train it using the perceptron learning rule to simulate basic binary logic gates — specifically **NAND** and **XOR**.

## Objectives

- Understand and implement a perceptron with a sigmoid activation.
- Train the perceptron to learn the NAND logic gate.
- Analyze its limitations when attempting to learn the XOR logic gate.

## Files

- `Python_Code.py` — Core implementation of the perceptron, including training and testing on NAND.
- `Documentation.docx` — Summary of findings and analysis on NAND vs XOR learning capabilities.

## Logic Functions

### NAND Gate
- **Training Data:** `[[0,0], [0,1], [1,0], [1,1]]`
- **Labels:** `[1, 1, 1, 0]`
- **Outcome:** Successful — The perceptron was able to learn the NAND function due to its linear separability.

### XOR Gate
- **Labels:** `[0, 1, 1, 0]`
- **Outcome:** Unsuccessful — The perceptron failed to learn the XOR function, highlighting its inability to solve non-linearly separable problems.

## Prerequisites

- Python 3.x
- NumPy

Install NumPy if you haven't already:
```bash
pip install numpy
```

## Running the Code

To train and test the perceptron on the NAND function:

```bash
python Python_Code.py
```

You will see the output predictions for all input combinations of the NAND gate.

## How It Works

- The perceptron uses a sigmoid activation function to compute outputs.
- Training is done using a simple perceptron learning rule, adjusting weights and bias based on error.
- After training, predictions are thresholded at 0.5 to classify outputs as binary.

## Limitations & Observations

- The perceptron learns the NAND function successfully, which is linearly separable.
- It fails on XOR, demonstrating the need for multi-layer perceptrons (MLPs) for non-linear functions.
- This experiment underscores the importance of network depth in solving complex classification problems.


