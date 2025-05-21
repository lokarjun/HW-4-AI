module lif_neuron #(
    parameter int DATA_WIDTH = 16,
    parameter int FRACTION_BITS = 8,
    parameter logic [DATA_WIDTH-1:0] LAMBDA = 16'd251,     // λ ≈ 0.98
  parameter logic [DATA_WIDTH-1:0] THRESHOLD = 16'd350   // θ = 1.0
)(
    input  logic clk,
    input  logic rst_n,
    input  logic spike_in,
    output logic spike_out
);

    logic [DATA_WIDTH-1:0] potential, updated_potential;
    logic [DATA_WIDTH-1:0] decayed;
    logic spiking;

    always_comb begin
        // Decay the potential
        decayed = (potential * LAMBDA) >> FRACTION_BITS;

        // Add input if present
        updated_potential = decayed;
        if (spike_in)
            updated_potential = updated_potential + (1 << FRACTION_BITS);

        // Spike decision
        spiking = (updated_potential >= THRESHOLD);
    end

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            potential <= 0;
            spike_out <= 0;
        end else begin
            spike_out <= spiking;
            if (spiking)
                potential <= 0;
            else
                potential <= updated_potential;
        end

        // Move the debug print here to show meaningful values
        $display("T=%0t | Updated_P(t)=%0d | Decayed_P(t)=%0d | Input=%b | Spike=%b",
                 $time, updated_potential, decayed, spike_in, spiking);
    end

endmodule
