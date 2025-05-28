import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.result import TestFailure
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
import random

# Python version of quarter_round and block used for reference
from chacha20_reference import chacha_block

# Utility to convert list of 32-bit integers to 512-bit binary value
def list_to_binval(words):
    val = 0
    for w in reversed(words):
        val = (val << 32) | (w & 0xFFFFFFFF)
    return BinaryValue(val, n_bits=512, bigEndian=False)

# Utility to convert 512-bit binary value to list of 32-bit integers
def binval_to_list(binval):
    val = int(binval)
    return [(val >> (32 * i)) & 0xFFFFFFFF for i in range(16)]

@cocotb.test()
async def test_chacha20_core(dut):
    """
    Test the ChaCha20 hardware core against Python reference.
    """
    # Start clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    dut.rst.value = 1
    await Timer(20, units="ns")
    dut.rst.value = 0

    for _ in range(5):  # Run 5 tests with random inputs
        # Generate a random 512-bit state (16 x 32-bit words)
        state = [random.getrandbits(32) for _ in range(16)]
        dut.state_in.value = list_to_binval(state)

        # Assert start
        dut.start.value = 1
        await RisingEdge(dut.clk)
        dut.start.value = 0

        # Wait until done is high
        while True:
            await RisingEdge(dut.clk)
            if dut.done.value == 1:
                break

        # Get result from hardware
        hw_out = binval_to_list(dut.state_out.value)

        # Run Python reference to compute expected result
        expected_out = chacha_block(state)
        expected_key_stream = [(x + s) & 0xFFFFFFFF for x, s in zip(expected_out, state)]

        # Check match
        if hw_out != expected_key_stream:
            raise TestFailure(f"Mismatch:\nHW : {hw_out}\nSW : {expected_key_stream}")

    dut._log.info("All test cases passed!")
