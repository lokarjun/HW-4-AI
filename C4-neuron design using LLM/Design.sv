module leaky_integrate_fire_neuron (
    input clk, // clock input
    input reset, // asynchronous reset
    input [7:0] current, // 8-bit current input
    input [7:0] THRESHOLD, // spiking threshold
    input [7:0] LEAK_RATE, // decrease per cycle
    input [7:0] REFRAC_PERIOD, // refractory period in cycles
    output reg spike // output spike signal
);

// Internal states
reg [7:0] membrane_potential = 8'd0;
reg [7:0] refrac_counter = 8'd0;
reg in_refrac = 0;

// On every clock cycle
always @(posedge clk or posedge reset) begin
    if (reset) begin
        membrane_potential <= 8'd0;
        refrac_counter <= 8'd0;
        in_refrac <= 0;
        spike <= 0;
    end 
    else begin
        spike <= 0; // Reset spike signal by default
        
        if (in_refrac) begin
            // If in refractory period, decrement counter
            refrac_counter <= refrac_counter - 1'b1;
            if (refrac_counter == 8'd0) 
                in_refrac <= 0; // Exit refractory period
        end 
        else begin
            // Apply leakage while preventing underflow
            if (membrane_potential < LEAK_RATE) 
                membrane_potential <= current; // Directly assign input current
            else 
                membrane_potential <= membrane_potential + current - LEAK_RATE;

            // Prevent overflow: if adding current causes overflow, clamp to threshold
            if (membrane_potential + current < membrane_potential) 
                membrane_potential <= THRESHOLD;

            // Check for spiking condition
            if (membrane_potential >= THRESHOLD) begin
                membrane_potential <= 8'd0; // Reset potential
                spike <= 1; // Generate spike
                in_refrac <= 1; // Enter refractory period
                refrac_counter <= REFRAC_PERIOD; // Set refractory counter
            end
        end
    end
end

endmodule


module spiking_neural_network (
    input clk, reset,
    input [7:0] input_current [2:0], // Input currents for 3 input neurons
    input [7:0] synapse_weights_input_hidden [2:0][1:0], // 3x2 weights (Input → Hidden)
    input [7:0] synapse_weights_hidden_output [1:0], // 2 weights (Hidden → Output)
    input [7:0] threshold, leak_rate, refrac_period, // Common parameters
    output wire output_spike // Final output neuron spike
);

    wire hidden_spikes [1:0];
    wire [7:0] hidden_currents [1:0];
    wire [7:0] output_current;

    // Instantiate hidden layer neurons (2 neurons)
    generate
        genvar h;
        for (h = 0; h < 2; h = h + 1) begin : hidden_layer
            reg [7:0] sum_input;
            integer i;

            always @(*) begin
                sum_input = 8'd0;
                for (i = 0; i < 3; i = i + 1) begin
                    sum_input = sum_input + (input_current[i] * synapse_weights_input_hidden[i][h]);
                end
            end

            leaky_integrate_fire_neuron hidden_neuron (
                .clk(clk),
                .reset(reset),
                .current(sum_input),
                .THRESHOLD(threshold),
                .LEAK_RATE(leak_rate),
                .REFRAC_PERIOD(refrac_period),
                .spike(hidden_spikes[h])
            );
        end
    endgenerate

    // Compute output layer input current from hidden layer spikes
    reg [7:0] sum_hidden;
    integer j;
    always @(*) begin
        sum_hidden = 8'd0;
        for (j = 0; j < 2; j = j + 1) begin
            sum_hidden = sum_hidden + (hidden_spikes[j] * synapse_weights_hidden_output[j]);
        end
    end

    // Instantiate output neuron
    leaky_integrate_fire_neuron output_neuron (
        .clk(clk),
        .reset(reset),
        .current(sum_hidden),
        .THRESHOLD(threshold),
        .LEAK_RATE(leak_rate),
        .REFRAC_PERIOD(refrac_period),
        .spike(output_spike)
    );

endmodule

module network_register_file (
    input clk,
    input reset,
    input write_enable,
    input [4:0] addr,           // Up to 32 registers
    input [7:0] write_data,
    output reg [7:0] threshold,
    output reg [7:0] leak_rate,
    output reg [7:0] refrac_period,
    output reg [7:0] weights_input_hidden [2:0][1:0],
    output reg [7:0] weights_hidden_output [1:0]
);

    integer i, j; // <--- moved outside the always block

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            threshold <= 8'd100;
            leak_rate <= 8'd1;
            refrac_period <= 8'd10;
            
            for (i = 0; i < 3; i = i + 1)
                for (j = 0; j < 2; j = j + 1)
                    weights_input_hidden[i][j] <= 8'd1;
            
            for (j = 0; j < 2; j = j + 1)
                weights_hidden_output[j] <= 8'd1;
        end else if (write_enable) begin
            case (addr)
                5'd0: threshold <= write_data;
                5'd1: leak_rate <= write_data;
                5'd2: refrac_period <= write_data;

                // Input to Hidden weights
                5'd3: weights_input_hidden[0][0] <= write_data;
                5'd4: weights_input_hidden[1][0] <= write_data;
                5'd5: weights_input_hidden[2][0] <= write_data;
                5'd6: weights_input_hidden[0][1] <= write_data;
                5'd7: weights_input_hidden[1][1] <= write_data;
                5'd8: weights_input_hidden[2][1] <= write_data;

                // Hidden to Output weights
                5'd9:  weights_hidden_output[0] <= write_data;
                5'd10: weights_hidden_output[1] <= write_data;

                default: ; // Do nothing
            endcase
        end
    end
endmodule


module spi_slave_interface (
    input clk,          // System clock
    input rst,          // Asynchronous reset
    input sclk,         // SPI Clock
    input cs,           // Active-low chip select
    input mosi,         // Master-out slave-in
    output reg miso,    // Master-in slave-out

    output reg write_en,
    output reg [4:0] addr,
    output reg [7:0] data_out
);

    reg [15:0] shift_reg = 16'b0; // First 8 bits: command, Next 8 bits: data
    reg [3:0] bit_cnt = 0;

    enum logic [1:0] {
        IDLE,
        RECEIVE,
        DONE
    } state = IDLE;

    always @(posedge sclk or posedge rst) begin
        if (rst) begin
            shift_reg <= 0;
            bit_cnt <= 0;
            state <= IDLE;
            write_en <= 0;
        end
        else begin
            if (!cs) begin
                case (state)
                    IDLE: begin
                        bit_cnt <= 0;
                        write_en <= 0;
                        state <= RECEIVE;
                    end
                    RECEIVE: begin
                        shift_reg <= {shift_reg[14:0], mosi}; // Shift in
                        bit_cnt <= bit_cnt + 1;
                        if (bit_cnt == 15) state <= DONE;
                    end
                    DONE: begin
                        write_en <= shift_reg[15]; // MSB: 1 = write, 0 = read (future support)
                        addr <= shift_reg[14:10];  // 5-bit address
                        data_out <= shift_reg[7:0]; // 8-bit data
                        state <= IDLE;
                    end
                endcase
            end else begin
                // Reset shift logic on CS high
                state <= IDLE;
                bit_cnt <= 0;
                write_en <= 0;
            end
        end
    end

    // For now, keep MISO low (extend this for read-back logic if needed)
    always @(posedge clk) begin
        miso <= 0;
    end

endmodule

module top_module (
    input clk,          // System clock
    input rst,          // Asynchronous reset

    // SPI interface signals
    input sclk,         // SPI clock
    input cs,           // SPI chip select (active low)
    input mosi,         // SPI data in
    output miso,        // SPI data out

    // Neural input interface
    input [7:0] input_current_0,
    input [7:0] input_current_1,
    input [7:0] input_current_2,

    output output_spike // Final output from network
);

    // SPI interface wires
    wire spi_write_en;
    wire [4:0] spi_addr;
    wire [7:0] spi_data_out;

    // Register file outputs (connected to network)
    wire [7:0] threshold;
    wire [7:0] leak_rate;
    wire [7:0] refrac_period;
    wire [7:0] weights_input_hidden [2:0][1:0];
    wire [7:0] weights_hidden_output [1:0];

    //--------------------------------------------
    // Instantiate SPI Interface
    //--------------------------------------------
    spi_slave_interface spi_if (
        .clk(clk),
        .rst(rst),
        .sclk(sclk),
        .cs(cs),
        .mosi(mosi),
        .miso(miso),
        .write_en(spi_write_en),
        .addr(spi_addr),
        .data_out(spi_data_out)
    );

    //--------------------------------------------
    // Instantiate Programmable Register File
    //--------------------------------------------
    network_register_file reg_file (
        .clk(clk),
        .reset(rst),
        .write_enable(spi_write_en),
        .addr(spi_addr),
        .write_data(spi_data_out),
        .threshold(threshold),
        .leak_rate(leak_rate),
        .refrac_period(refrac_period),
        .weights_input_hidden(weights_input_hidden),
        .weights_hidden_output(weights_hidden_output)
    );

    //--------------------------------------------
    // Instantiate Spiking Neural Network
    //--------------------------------------------
    wire [7:0] input_currents [2:0];
    assign input_currents[0] = input_current_0;
    assign input_currents[1] = input_current_1;
    assign input_currents[2] = input_current_2;

    spiking_neural_network snn (
        .clk(clk),
        .reset(rst),
        .input_current(input_currents),
        .synapse_weights_input_hidden(weights_input_hidden),
        .synapse_weights_hidden_output(weights_hidden_output),
        .threshold(threshold),
        .leak_rate(leak_rate),
        .refrac_period(refrac_period),
        .output_spike(output_spike)
    );

endmodule


