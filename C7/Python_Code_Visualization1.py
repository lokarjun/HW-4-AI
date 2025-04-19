import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Activation and derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    s = sigmoid(x)
    return s * (1 - s)

# Perceptron class
class Perceptron:
    def __init__(self, learning_rate=0.5):
        self.w = np.random.randn(2)
        self.b = np.random.randn()
        self.lr = learning_rate
        self.history = []

    def forward(self, x):
        self.z = np.dot(self.w, x) + self.b
        return sigmoid(self.z)

    def train(self, X, y, epochs=50):
        for _ in range(epochs):
            for xi, target in zip(X, y):
                output = self.forward(xi)
                error = target - output
                grad = sigmoid_deriv(self.z) * error
                self.w += self.lr * grad * xi
                self.b += self.lr * grad
                self.history.append((self.w.copy(), self.b))

    def predict(self, x):
        return 1 if self.forward(x) >= 0.5 else 0

# Data
nand_data = np.array([[0,0], [0,1], [1,0], [1,1]])
nand_labels = np.array([1, 1, 1, 0])

# Train
p_nand = Perceptron()
p_nand.train(nand_data, nand_labels)

# Results
print("NAND Results:")
for x in nand_data:
    print(f"{x} -> {p_nand.predict(x)}")

# Visualization
fig, ax = plt.subplots()
scatter = ax.scatter(nand_data[:, 0], nand_data[:, 1], c=nand_labels, cmap='coolwarm', s=100, edgecolors='k')
line, = ax.plot([], [], 'k--', lw=2)
ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-0.5, 1.5)

def update(i):
    w, b = p_nand.history[i]
    x_vals = np.array(ax.get_xlim())
    if w[1] != 0:
        y_vals = -(w[0] * x_vals + b) / w[1]
    else:
        y_vals = np.zeros_like(x_vals)
    line.set_data(x_vals, y_vals)
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(p_nand.history), interval=200, blit=True)
ani.save("fixed_nand_animation.gif", writer='pillow', fps=5)
# plt.show()  # Uncomment if you want to see it live
