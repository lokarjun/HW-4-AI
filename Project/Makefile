TOPLEVEL_LANG = verilog
SIM = modelsim

# Name of your top-level SystemVerilog module
TOPLEVEL = chacha20_core

# Name of your cocotb testbench file (without .py extension)
MODULE = test_chacha20

# Path to your sources (quoted to handle spaces in directory names)
VERILOG_SOURCES = "$(shell pwd)/chacha20_core.sv"

# Optional: set Python interpreter if needed
# PYTHON = python3

# Include cocotb makefiles
COCOTB_MAKE := $(shell cocotb-config --makefiles)
include "$(COCOTB_MAKE)/Makefile.sim"
