import cProfile
import pstats
import io
import time
import random
import string
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import sys

# Increase integer limit for large text conversion
sys.set_int_max_str_digits(100_000_000)

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

        if option == '1':
            text = random_text(message_size)
        elif option == '2':
            ascii_code = ''.join([str(ord(c)).zfill(3) for c in random_text(message_size)])
            text = ascii_code
        elif option == '3':
            text = ''.join(random.choices('0123456789abcdef', k=2 * message_size))

        return [option, key, counter, nonce, text, '0']
    else:
        return ['0']

def run_test_for_message_size(message_size):
    """Run the test for a given message size"""
    global _inputs
    _inputs = prepare_inputs_for_option('1', message_size)  # Option 1: Cipher Message

    f = io.StringIO()
    with redirect_stdout(f):
        main()

def benchmark():
    """Benchmark for different message sizes"""
    # Testing from 1MB to 10MB in steps
    message_sizes = [
        1_000_000,   # 1 MB
        2_000_000,   # 2 MB
        3_000_000,   # 3 MB
        4_000_000,   # 4 MB
        5_000_000,   # 5 MB
        6_000_000,   # 6 MB
        7_000_000,   # 7 MB
        8_000_000,   # 8 MB
        9_000_000,   # 9 MB
        10_000_000   # 10 MB
    ]

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
    plt.figure(figsize=(10, 7))
    plt.plot([s / 1_000_000 for s in message_sizes], times, marker='o')
    plt.xlabel('Message Size (MB)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('ChaCha20 Software Execution Time (1MB to 10MB)')
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig('chacha20_benchmark_large_plot.png')
    plt.show()

if __name__ == "__main__":
    message_sizes, times = benchmark()
    plot_results(message_sizes, times)
