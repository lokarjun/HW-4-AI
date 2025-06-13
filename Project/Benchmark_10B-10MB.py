"""
Benchmark_10B-10MB.py

This script benchmarks the pure Python ChaCha20 implementation for a wide range of
message sizes, from 10 bytes up to 10 MB. It logs execution times for each size,
providing fine-grained insight into algorithm scaling. This helped identify 2 MB
as a representative test size for hardware acceleration.
"""


import cProfile
import pstats
import io
import time
import random
import string
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import sys
sys.set_int_max_str_digits(100_000_000)  # Updated to support 10MB+


# Monkey-patch input() to automate inputs
_inputs = []

def mock_input(prompt=None):
    if _inputs:
        return _inputs.pop(0)
    raise ValueError("No more inputs provided!")

# Attach mock input
import builtins
original_input = builtins.input
builtins.input = mock_input

# Import your ChaCha20 main function
from ChaCha20 import main

def random_text(length=10):
    """Generate random text of specified byte length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def prepare_inputs_for_option(option, message_size):
    """Prepare a sequence of inputs based on option and message size"""
    if option in ['1', '2', '3']:
        key = ''.join(random.choices('0123456789abcdef', k=64))
        counter = ''.join(random.choices('0123456789abcdef', k=8))
        nonce = ''.join(random.choices('0123456789abcdef', k=24))

        if option == '1':  # Cipher Message (plain text)
            text = random_text(message_size)
        elif option == '2':  # Cipher ASCII
            ascii_code = ''.join([str(ord(c)).zfill(3) for c in random_text(message_size)])
            text = ascii_code
        elif option == '3':  # Cipher Hexadecimal
            text = ''.join(random.choices('0123456789abcdef', k=2 * message_size))  # 2 hex per byte

        return [option, key, counter, nonce, text, '0']
    else:
        return ['0']

def run_test_for_message_size(message_size):
    """Run the test for a given message size"""
    global _inputs
    _inputs = prepare_inputs_for_option('1', message_size)  # Testing option 1 (Cipher Message)

    f = io.StringIO()
    with redirect_stdout(f):
        main()

def benchmark():
    """Benchmark for different message sizes"""
    message_sizes = [10, 1000, 1_000_000, 10_000_000]  # bytes
    times = []

    for size in message_sizes:
        print(f"\nTesting for message size: {size} bytes")

        start_time = time.time()
        run_test_for_message_size(size)
        end_time = time.time()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)

        print(f"Time taken: {elapsed_time:.4f} seconds")

    return message_sizes, times

def plot_results(message_sizes, times):
    """Plot benchmark results"""
    plt.figure(figsize=(8,6))
    plt.plot(message_sizes, times, marker='o')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('ChaCha20 Software Execution Time vs Message Size')
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig('chacha20_benchmark_plot.png')
    plt.show()

if __name__ == "__main__":
    message_sizes, times = benchmark()
    plot_results(message_sizes, times)
