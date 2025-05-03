import numpy as np

# Sigmoid activation and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)

# XOR dataset
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])

# Network architecture
input_size = 2
hidden_size = 2
output_size = 1
lr = 0.1
epochs = 10000

# Weight initialization
np.random.seed(0)
W1 = np.random.randn(input_size, hidden_size)   # (2x2)
b1 = np.random.randn(hidden_size)               # (2,)
W2 = np.random.randn(hidden_size, output_size)  # (2x1)
b2 = np.random.randn(output_size)               # (1,)

# Training loop
for epoch in range(epochs):
    for i in range(len(X)):
        x = X[i]
        target = y[i]

        # ---- Forward Pass ----
        z1 = np.dot(x, W1) + b1       # Hidden layer input
        a1 = sigmoid(z1)              # Hidden layer output
        z2 = np.dot(a1, W2) + b2      # Output layer input
        a2 = sigmoid(z2)              # Final output

        # ---- Backpropagation ----
        error = target - a2           # Output error
        delta2 = error * sigmoid_deriv(z2)

        error1 = delta2.dot(W2.T)     # Hidden layer error
        delta1 = error1 * sigmoid_deriv(z1)

        # ---- Gradient Descent Update ----
        W2 += lr * np.outer(a1, delta2)
        b2 += lr * delta2
        W1 += lr * np.outer(x, delta1)
        b1 += lr * delta1

# Testing
print("XOR Predictions after training:")
for x in X:
    z1 = np.dot(x, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    a2 = sigmoid(z2)
    prediction = 1 if a2 >= 0.5 else 0
    print(f"{x} -> {prediction}")
