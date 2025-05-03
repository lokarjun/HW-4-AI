module q_value_max_selector (
    input  logic [4:0] state_i,         // row index (0–4)
    input  logic [4:0] state_j,         // col index (0–4)
    input  logic signed [15:0] q_values [3:0], // Q-values for 4 actions
    output logic [1:0] best_action,     // 2-bit action (0–3)
    output logic signed [15:0] max_q    // Best Q-value
);

    // Temporary variables for max comparison
    logic signed [15:0] max_temp;
    logic [1:0] action_temp;

    always_comb begin
        // Initialize with action 0
        max_temp    = q_values[0];
        action_temp = 2'd0;

        // Compare with action 1
        if (q_values[1] > max_temp) begin
            max_temp    = q_values[1];
            action_temp = 2'd1;
        end

        // Compare with action 2
        if (q_values[2] > max_temp) begin
            max_temp    = q_values[2];
            action_temp = 2'd2;
        end

        // Compare with action 3
        if (q_values[3] > max_temp) begin
            max_temp    = q_values[3];
            action_temp = 2'd3;
        end

        // Assign final output
        best_action = action_temp;
        max_q       = max_temp;
    end

endmodule
