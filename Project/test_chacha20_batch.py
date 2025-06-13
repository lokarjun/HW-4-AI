"""
test_chacha20_batch.py

Description:
- Extended **Cocotb testbench** for **batch testing** and benchmarking.
- Reads pre-generated 2MB input from JSON and drives the hardware core repeatedly.
- Logs total hardware execution time for multi-block workloads.

Role:
- Measures end-to-end hardware core performance in a co-simulation scenario.
"""

import json
import time
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

BLOCK_SIZE_BYTES = 64  # Each ChaCha20 block is 64 bytes

@cocotb.test()
async def test_chacha20_batch(dut):
    # Start a clock with 10ns period
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    start_time = time.time()

    with open("chacha20_input_manifest.json", "r") as f:
        data = json.load(f)

    for entry in data["tests"]:
        message_type = entry["option"]
        key = entry["key"]
        counter_base = int(entry["counter"], 16)
        nonce = entry["nonce"]
        text_file = entry["text_file"]

        # Load 2MB of message content from the file
        with open(text_file, "r") as tf:
            full_text = tf.read()

        # Break the message into 64-byte (512-bit) blocks
        block_count = len(full_text) // BLOCK_SIZE_BYTES
        for block_index in range(block_count):
            text_block = full_text[block_index * BLOCK_SIZE_BYTES : (block_index + 1) * BLOCK_SIZE_BYTES]

            # Increment counter for each block
            counter_int = counter_base + block_index
            counter_hex = f"{counter_int:08x}"

            # Write JSON for this block
            with open("hw_input.txt", "w") as f:
                f.write(json.dumps({
                    "option": message_type,
                    "key": key,
                    "counter": counter_hex,
                    "nonce": nonce,
                    "text": text_block
                }))

            # Trigger hardware encryption
            dut.start.value = 0
            await RisingEdge(dut.clk)
            dut.start.value = 1
            await RisingEdge(dut.clk)
            dut.start.value = 0

            # Wait until done
            while not dut.done.value:
                await RisingEdge(dut.clk)

           # dut._log.info(f"Block {block_index+1}/{block_count} encrypted for option {message_type}")

    end_time = time.time()
    dut._log.info("Total execution time for all options (2MB each): {:.4f} seconds".format(end_time - start_time))
