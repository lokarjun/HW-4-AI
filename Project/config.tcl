# config.tcl (for OpenLane)

# Design identification
set ::env(DESIGN_NAME) "chacha20_core"

# Source Verilog file path — relative or absolute
set ::env(VERILOG_FILES) [list "$::env(DESIGN_DIR)/chacha20core.sv"]

# Clock signal definition
set ::env(CLOCK_PORT) "clk"
set ::env(CLOCK_PERIOD) "10.0"

# Optional: synthesis and floorplan parameters
set ::env(SYNTH_TOP) "chacha20_core"
set ::env(FP_CORE_UTIL) "30"
set ::env(PL_TARGET_DENSITY) "0.5"
set ::env(DIE_AREA) "0 0 100 100"
