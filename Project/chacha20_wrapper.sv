/*
chacha20_wrapper.sv

Description:
- Top-level SystemVerilog wrapper around `chacha20core.sv`.
- Handles 32-bit streaming I/O to/from software via an FSM.
- Buffers input data into 512-bit blocks and feeds them sequentially to the core.
- Designed to address pin count limitations and optimize OpenLane synthesis/placement.

Role:
- Enables multi-block processing for large messages and efficient hardware-software co-design.
*/

module chacha20_wrapper (
    input  logic        clk,
    input  logic        rst,
    input  logic        start,           // Start signal for wrapper
    input  logic [31:0] data_in,         // Input stream (1 word at a time)
    output logic [31:0] data_out,        // Output stream (1 word at a time)
    output logic        done             // Done signal when output is complete
);

    typedef enum logic [1:0] {
        IDLE,
        LOAD,
        RUN,
        UNLOAD
    } state_t;

    state_t state, next_state;

    logic [3:0] word_index;
    logic       start_core;
    logic       core_done;

    logic [511:0] input_buffer;
    logic [511:0] output_buffer;

    // Internal wires for state_out
    logic [511:0] core_state_out;

    // Instantiate the ChaCha20 core
    chacha20_core u_core (
        .clk(clk),
        .rst(rst),
        .start(start_core),
        .state_in(input_buffer),
        .state_out(core_state_out),
        .done(core_done)
    );

    // FSM transition
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= IDLE;
        end else begin
            state <= next_state;
        end
    end

    // FSM next-state logic
    always_comb begin
        next_state = state;
        case (state)
            IDLE:    if (start) next_state = LOAD;
            LOAD:    if (word_index == 15) next_state = RUN;
            RUN:     if (core_done) next_state = UNLOAD;
            UNLOAD:  if (word_index == 15) next_state = IDLE;
        endcase
    end

    // Control logic and data path
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            input_buffer   <= 0;
            output_buffer  <= 0;
            word_index     <= 0;
            start_core     <= 0;
            done           <= 0;
            data_out       <= 0;
        end else begin
            case (state)
                IDLE: begin
                    word_index <= 0;
                    done       <= 0;
                end
                LOAD: begin
                    input_buffer[word_index*32 +: 32] <= data_in;
                    word_index <= word_index + 1;
                end
                RUN: begin
                    start_core <= 1;
                    if (core_done) begin
                        start_core <= 0;
                        output_buffer <= core_state_out;
                        word_index <= 0;
                    end
                end
                UNLOAD: begin
                    data_out <= output_buffer[word_index*32 +: 32];
                    word_index <= word_index + 1;
                    if (word_index == 15) begin
                        done <= 1;
                    end
                end
            endcase
        end
    end

endmodule
