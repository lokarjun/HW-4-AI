/*
chacha20core.sv

Description:
- SystemVerilog RTL implementation of the **ChaCha20 encryption core block**.
- Implements the quarter-round and block-level operations.
- Operates on a 512-bit internal state (16 x 32-bit words).
- Verified via Cocotb and used for hardware acceleration in chiplet architecture.

Role:
- Main hardware block performing the actual encryption rounds.
*/


module chacha20_core (
    input  logic         clk,
    input  logic         rst,
    input  logic         start,
    input  logic [511:0] state_in,   // 16 x 32-bit words (64 bytes)
    output logic         done,
    output logic [511:0] state_out   // 16 x 32-bit words
);

    // Internal state
    logic [31:0] x [0:15];
    logic [31:0] input_words [0:15];
    logic [3:0]  round_cnt;
    logic        busy;

    // Rotate left
    function automatic [31:0] rotl(input [31:0] a, input [4:0] n);
        rotl = (a << n) | (a >> (32 - n));
    endfunction

    // Quarter round
    task automatic quarter_round(
        inout logic [31:0] a,
        inout logic [31:0] b,
        inout logic [31:0] c,
        inout logic [31:0] d
    );
        a = a + b; d ^= a; d = rotl(d, 16);
        c = c + d; b ^= c; b = rotl(b, 12);
        a = a + b; d ^= a; d = rotl(d, 8);
        c = c + d; b ^= c; b = rotl(b, 7);
    endtask

    // FSM and round logic
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            round_cnt <= 0;
            busy      <= 0;
            done      <= 0;
        end else begin
            // Begin new block
            if (start && !busy) begin
                for (int i = 0; i < 16; i++) begin
                    x[i]           = state_in[i*32 +: 32];
                    input_words[i] = state_in[i*32 +: 32];
                end
                round_cnt <= 0;
                busy      <= 1;
                done      <= 0;
            end

            // Execute rounds
            else if (busy) begin
                // Column round
                quarter_round(x[0], x[4], x[8],  x[12]);
                quarter_round(x[1], x[5], x[9],  x[13]);
                quarter_round(x[2], x[6], x[10], x[14]);
                quarter_round(x[3], x[7], x[11], x[15]);

                // Diagonal round
                quarter_round(x[0], x[5], x[10], x[15]);
                quarter_round(x[1], x[6], x[11], x[12]);
                quarter_round(x[2], x[7], x[8],  x[13]);
                quarter_round(x[3], x[4], x[9],  x[14]);

                round_cnt <= round_cnt + 1;

                if (round_cnt == 9) begin  // After 10 rounds
                    for (int i = 0; i < 16; i++) begin
                        state_out[i*32 +: 32] <= x[i] + input_words[i];
                    end
                    busy <= 0;
                    done <= 1;
                end
            end

            // Clear done after one cycle
            else if (done) begin
                done <= 0;
            end
        end
    end

endmodule
