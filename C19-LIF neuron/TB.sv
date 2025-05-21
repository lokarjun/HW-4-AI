`timescale 1ns/1ps

module lif_neuron_tb;

  // Parameters (must match the DUT)
  parameter int DATA_WIDTH = 16;
  parameter int FRACTION_BITS = 8;
  parameter logic [DATA_WIDTH-1:0] LAMBDA = 16'd251;     // ~0.98
  parameter logic [DATA_WIDTH-1:0] THRESHOLD = 16'd350;  // 1.0

  // DUT signals
  logic clk, rst_n;
  logic spike_in;
  logic spike_out;

  // Instantiate the DUT
  lif_neuron #(
    .DATA_WIDTH(DATA_WIDTH),
    .FRACTION_BITS(FRACTION_BITS),
    .LAMBDA(LAMBDA),
    .THRESHOLD(THRESHOLD)
  ) dut (
    .clk(clk),
    .rst_n(rst_n),
    .spike_in(spike_in),
    .spike_out(spike_out)
  );

  // Clock generation
  always #5 clk = ~clk;

  // Test sequence
  initial begin
    $display("Starting LIF Neuron Testbench...");
    clk = 0;
    rst_n = 0;
    spike_in = 0;

    #10 rst_n = 1;

    // === Test 1: Constant input below threshold ===
    $display("\nTest 1: Constant low input (should not spike)");
    repeat (10) begin
      spike_in = 0; // no input
      #10;
    end

    // === Test 2: Accumulating input until threshold ===
    $display("\nTest 2: Gradual accumulation to reach threshold");
    repeat (15) begin
      spike_in = 1;
      #10;
    end

    // === Test 3: No input, observe leakage ===
    $display("\nTest 3: Leakage without input");
    repeat (10) begin
      spike_in = 0;
      #10;
    end

    // === Test 4: Strong input (simulate multiple spikes in a row) ===
    $display("\nTest 4: Strong input causing immediate spiking");
    repeat (3) begin
      spike_in = 1;
      #10;
    end

    $display("\nSimulation complete.");
    $finish;
  end

  // Monitor
  always @(posedge clk) begin
    $display("T=%0t | Input=%b | Spike=%b", $time, spike_in, spike_out);
  end

endmodule
