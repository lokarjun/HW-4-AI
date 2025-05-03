
# Challenge 7: Visualizing Perceptron Learning

## Overview

In this challenge, we implement and **visualize** the learning process of a perceptron that models a binary logic function (NAND) using a sigmoid activation function. The goal is to help users understand how the perceptron updates its weights and decision boundary during training — all illustrated step-by-step as an animation in a 2D space.

## Objectives

- Visualize the 2D decision boundary ("line") of a perceptron as it learns.
- Animate the training process by updating the weight vector over epochs.
- Understand how decision boundaries evolve over time using the perceptron rule.

## Files

- `Python_Code_Visualization1.py`: Python script implementing the animated training visualization.
- `fixed_nand_animation.gif`: Output animation that shows the evolution of the decision boundary while training on the NAND gate dataset.

## Prerequisites

- Python 3.x
- NumPy
- Matplotlib
- Pillow (for saving GIFs)

To install dependencies:

```bash
pip install numpy matplotlib pillow
```

## How to Run

To generate the animated GIF of the perceptron training:

```bash
python Python_Code_Visualization1.py
```

This will:
- Train a perceptron on NAND gate data.
- Generate an animation (`fixed_nand_animation.gif`) that shows how the separating line updates over time.

## Output Description

The animated plot will display:
- The four NAND data points in a 2D space (colored red/blue).
- A dashed black line that represents the perceptron’s decision boundary.
- As training progresses, the decision line moves in response to weight updates based on training error.

## Key Concepts

- **Sigmoid Activation**: Used for continuous output and smooth gradients.
- **Weight Update Rule**: Based on the gradient of sigmoid and prediction error.
- **Animation**: Uses `matplotlib.animation.FuncAnimation` to record line updates.

## Challenge Learnings

- Gained hands-on experience visualizing learning in neural networks.
- Observed how weight adjustments influence the model’s classification boundary.
- Understood the limitation of single-layer perceptrons on non-linear problems in a tangible way.


