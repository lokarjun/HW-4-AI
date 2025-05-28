import cProfile
import pstats
import io
import time
import random
import string
from contextlib import redirect_stdout
import sys
import os

# Increase integer limit for large text handling
sys.set_int_max_str_digits(100_000_000)

# Monkey-patch input() to automate inputs
_inputs = []

def mock_input(prompt=None):
    if _inputs:
        return _inputs.pop(0)
    raise ValueError("No more inputs provided!")

# Attach monkey-patched input
import builtins
original_input = builtins.input
builtins.input = mock_input

# Import your ChaCha20 main function
from ChaCha20 import main

def load_text_from_file(filepath):
    """Load pre-generated text from file"""
    with open(filepath, 'r') as f:
        return f.read()

def prepare_inputs_for_option(option):
    """Prepare input sequence for given option from file"""
    key = ''.join(random.choices('0123456789abcdef', k=64))
    counter = ''.join(random.choices('0123456789abcdef', k=8))
    nonce = ''.join(random.choices('0123456789abcdef', k=24))

    if option == '1':
        text = load_text_from_file("inputs/plain_text.txt")
    elif option == '2':
        text = load_text_from_file("inputs/ascii_text.txt")
    elif option == '3':
        text = load_text_from_file("inputs/hex_text.txt")
    else:
        raise ValueError(f"Invalid option: {option}")

    return [option, key, counter, nonce, text, '0']

def run_test_for_option(option):
    """Run the encryption test for a specific option"""
    global _inputs
    _inputs = prepare_inputs_for_option(option)

    f = io.StringIO()
    with redirect_stdout(f):
        main()

def benchmark_core_options():
    """Benchmark core options [1], [2], [3] for pre-generated inputs"""
    options = ['1', '2', '3']

    profiler = cProfile.Profile()
    profiler.enable()

    for option in options:
        print(f"\nTesting Option [{option}] using pre-generated input")
        run_test_for_option(option)

    profiler.disable()

    # Show top 20 functions by cumulative time
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(20)

if __name__ == "__main__":
    benchmark_core_options()
