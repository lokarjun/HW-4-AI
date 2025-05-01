import torch
import torch.nn as nn
import torch.optim as optim
import time
import matplotlib.pyplot as plt

# Define the neural network architecture with variable depth and width
class FeedForwardNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(FeedForwardNN, self).__init__()
        layers = []
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(nn.Sigmoid())
        
        for _ in range(num_layers - 1):
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(nn.Sigmoid())
        
        layers.append(nn.Linear(hidden_size, output_size))
        layers.append(nn.Sigmoid())
        
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

# Collect times for various configurations
configurations = [(10, 2), (50, 3), (100, 4), (200, 5)]  # (hidden_size, num_layers)
cuda_times = []
pytorch_times = []

# Run benchmark for each configuration
for hidden_size, num_layers in configurations:
    # PyTorch Model
    model = FeedForwardNN(4, hidden_size, num_layers, 1)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    inputs = torch.randn(1, 4).to(device)

    start_time = time.time()
    model(inputs)  # Perform forward pass
    elapsed_time = time.time() - start_time
    pytorch_times.append(elapsed_time)
    
    # CUDA Model (Compile and run CUDA code with varying layers and neurons)
    # For simplicity, we assume CUDA code execution time is benchmarked outside the loop
    # Collect the CUDA execution time for each configuration manually or run the CUDA code separately.
    # Example:
    cuda_time = 0.0005  # This is just a placeholder for actual CUDA execution times.
    cuda_times.append(cuda_time)

# Plot results
hidden_sizes = [cfg[0] for cfg in configurations]
plt.plot(hidden_sizes, pytorch_times, label='PyTorch', marker='o')
plt.plot(hidden_sizes, cuda_times, label='CUDA', marker='x')
plt.xlabel('Hidden Layer Size')
plt.ylabel('Execution Time (ms)')
plt.title('Comparison of Execution Times (PyTorch vs CUDA)')
plt.legend()
plt.grid(True)
plt.show()
