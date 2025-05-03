
# Challenge 8: Solving XOR with a Multi-Layer Perceptron (MLP)

## Overview

This challenge demonstrates the implementation of a simple feedforward neural network to solve the **XOR** logical function — a classic example of a non-linearly separable problem that a single-layer perceptron cannot solve. We train a Multi-Layer Perceptron (MLP) with backpropagation using the XOR truth table.

## Objectives

- Understand why a single-layer perceptron fails to model XOR.
- Implement a Multi-Layer Perceptron (MLP) with:
  - 2 input neurons
  - 2 hidden neurons
  - 1 output neuron
- Train the MLP using the backpropagation algorithm.
- Verify that the network learns the correct XOR output.

## Files

- `Python_Code1.py` — Main implementation of the 2-2-1 MLP for XOR.
- `Documentation.docx` — A summary explaining the theory and outcome of the challenge.

## XOR Function

| Input A | Input B | Output |
|---------|---------|--------|
|   0     |    0    |   0    |
|   0     |    1    |   1    |
|   1     |    0    |   1    |
|   1     |    1    |   0    |

## Prerequisites

- Python 3.x
- NumPy

Install NumPy if you haven't already:

```bash
pip install numpy
```

## How to Run

Simply run the following command:

```bash
python Python_Code1.py
```

You will see printed predictions for all XOR input combinations after training.

## How It Works

1. **Network Architecture**
   - Input layer with 2 neurons.
   - Hidden layer with 2 neurons using sigmoid activation.
   - Output layer with 1 neuron using sigmoid activation.

2. **Forward Pass**
   - Input is passed through the hidden layer and then to the output layer.

3. **Backpropagation**
   - Calculates gradients of error with respect to weights and biases.
   - Applies gradient descent to update all parameters.

4. **Training**
   - The network is trained over 10,000 epochs.
   - Weights and biases are updated after each training example.

## Key Learnings

- The XOR function is not linearly separable — a single-layer perceptron cannot learn it.
- Adding a hidden layer allows the model to transform the input space and correctly separate outputs.
- This challenge illustrates the foundational principle behind deep learning — depth enables modeling of complex non-linear functions.

