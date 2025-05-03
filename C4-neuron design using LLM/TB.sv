`timescale 1ns / 1ps

module top_module_tb;

    reg clk, rst;
    reg sclk, cs, mosi;
    wire miso;
    reg [7:0] input_current_0, input_current_1, input_current_2;
    wire output_spike;

    // Instantiate the top module
    top_module uut (
        .clk(clk),
        .rst(rst),
        .sclk(sclk),
        .cs(cs),
        .mosi(mosi),
        .miso(miso),
        .input_current_0(input_current_0),
        .input_current_1(input_current_1),
        .input_current_2(input_current_2),
        .output_spike(output_spike)
    );

    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // 100MHz clock
    end

    // SPI Clock generation
    initial begin
        sclk = 0;
        forever #20 sclk = ~sclk; // 25MHz SPI clock
    end

    // SPI Send Task (sends 16-bit command: [WRITE=1][ADDR=5b][DATA=8b])
    task spi_send;
        input [15:0] spi_packet;
        integer i;
        begin
            cs = 0;
            for (i = 15; i >= 0; i = i - 1) begin
                @(negedge sclk);
                mosi = spi_packet[i];
            end
            @(negedge sclk);
            cs = 1;
            mosi = 0;
            #100; // Wait for reg file to update
        end
    endtask

    initial begin
        // Reset the system
        rst = 1;
        cs = 1;
        mosi = 0;
        input_current_0 = 0;
        input_current_1 = 0;
        input_current_2 = 0;

        #50;
        rst = 0;

        // --------------------------
        // SPI WRITE: Setup parameters
        // --------------------------
        // Format: [WRITE=1][ADDR][DATA]
        // Let's assume:
        //   - threshold addr = 0, leak_rate = 1, refrac_period = 2
        //   - weights_input_hidden[0][0] = addr 3
        //   - weights_input_hidden[0][1] = addr 4
        //   - weights_hidden_output[0] = addr 15

        spi_send(16'b1_00000_00010000); // threshold = 16
        spi_send(16'b1_00001_00000001); // leak_rate = 1
        spi_send(16'b1_00010_00000100); // refrac_period = 4
        spi_send(16'b1_00011_00000010); // weight_0_0 = 2
        spi_send(16'b1_00100_00000010); // weight_0_1 = 2
        spi_send(16'b1_01111_00001000); // output_weight_0 = 8

        // --------------------------
        // Apply Input Currents
        // --------------------------
        #100;
        input_current_0 = 8'd5;
        input_current_1 = 8'd5;
        input_current_2 = 8'd5;

        // Observe for a few clock cycles
        #1000;

        // Change input and observe again
        input_current_0 = 8'd10;
        input_current_1 = 8'd0;
        input_current_2 = 8'd0;
        #1000;

        $finish;
    end
  
  initial begin
 // $monitor("Time: %0t | Output Spike: %b | Hidden0: %b | Hidden1: %b", $time, dut.output_spike, dut.snn.hidden_spikes[0], dut.snn.hidden_spikes[1]);
  $dumpfile("snn.vcd");
  $dumpvars(0);
end

endmodule
