#include "defines.h"

uint8_t buffer[buffer_length];
uint8_t scan_smbus_address_result[8];
uint8_t scan_smbus_address_result_ptr = 0;
uint8_t sb_address = 0x0b; // default smart battery address
uint8_t block_length = 0;
uint8_t current_timestamp[4];
bool reverse_read_word_byte_order = true;
bool reverse_write_word_byte_order = true;
uint8_t smbus_reg_start = 0x00;
uint8_t smbus_reg_end = 0xFF;
uint16_t design_voltage = 0;

// Packet related variables
uint8_t command_timeout = 100; // milliseconds
uint16_t command_purge_timeout = 200; // milliseconds, if a command isn't complete within this time then delete the usb receive buffer
uint8_t calculated_checksum = 0;
uint8_t ack[1] = { 0x00 }; // acknowledge payload array
uint8_t err[1] = { 0xFF }; // error payload array
uint8_t ret[1]; // general array to store arbitrary bytes

uint8_t read_byte(uint8_t reg);
uint8_t write_byte(uint8_t reg, uint8_t data);
uint16_t read_word(uint8_t reg, bool reverse = true);
uint8_t write_word(uint8_t reg, uint16_t data, bool reverse = true);
uint8_t read_block(uint8_t reg, uint8_t* block_buffer);
uint8_t write_block(uint8_t reg, uint8_t* block_buffer, uint8_t block_length);
void scan_smbus_address(void);
void smbus_reg_dump(void);
void read_rom_byte(void);
void read_rom_block(void);
void update_timestamp(uint8_t *target);
uint8_t calculate_checksum(uint8_t *buff, uint16_t index, uint16_t bufflen);
uint16_t free_ram(void);
void send_usb_packet(uint8_t command, uint8_t subdatacode, uint8_t *payloadbuff, uint16_t payloadbufflen);
void handle_usb_data(void);


uint8_t read_byte(uint8_t reg)
{
    i2c_start((sb_address << 1) | I2C_WRITE);
    i2c_write(reg);
    i2c_rep_start((sb_address << 1) | I2C_READ);

    uint8_t ret = i2c_read(true);

    i2c_stop();
    return ret;
}

uint8_t write_byte(uint8_t reg, uint8_t data)
{
    i2c_start((sb_address << 1) | I2C_WRITE);
    i2c_write(reg);

    uint8_t ret = i2c_write(data);

    i2c_stop();
    return ret; // number of bytes written
}

uint16_t read_word(uint8_t reg, bool reverse = true)
{
    i2c_start((sb_address << 1) | I2C_WRITE);
    i2c_write(reg);
    i2c_rep_start((sb_address << 1) | I2C_READ);

    uint8_t b1 = i2c_read(false);
    uint8_t b2 = i2c_read(true);
    i2c_stop();

    if (!reverse) return ((b1 << 8) | b2);
    else return ((b2 << 8) | b1);
}

uint8_t write_word(uint8_t reg, uint16_t data, bool reverse = true)
{
    i2c_start((sb_address << 1) | I2C_WRITE);
    i2c_write(reg);

    if (reverse)
    {
        i2c_write(data & 0xFF);
        i2c_write((data >> 8) & 0xFF);
    }
    else
    {
        i2c_write((data >> 8) & 0xFF);
        i2c_write(data & 0xFF);
    }

    i2c_stop();
    return 2;
}

uint8_t read_block(uint8_t reg, uint8_t* block_buffer)
{
    i2c_start((sb_address << 1) | I2C_WRITE);
    i2c_write(reg);
    i2c_rep_start((sb_address << 1) | I2C_READ);

    uint8_t read_length = i2c_read(false); // first byte is length
    block_buffer[0] = read_length;

    for (uint8_t i = 0; i < (read_length - 1); i++) // last byte needs to be nack'd
    {
        block_buffer[1 + i] = i2c_read(false);
    }

    block_buffer[read_length] = i2c_read(true); // this will nack the last byte and store it in i's num_bytes-1 address.
    i2c_stop();
    return (read_length + 1);
}

uint8_t get_block_length(uint8_t reg)
{
    i2c_start((sb_address << 1) | I2C_WRITE);
    i2c_write(reg);
    i2c_rep_start((sb_address << 1) | I2C_READ);

    uint8_t read_length = i2c_read(true); // first byte is length
    i2c_stop();
    return (read_length+1);
}

uint8_t write_block(uint8_t reg, uint8_t* block_buffer, uint8_t block_buffer_length)
{
    i2c_start((sb_address << 1) | I2C_WRITE);
    i2c_write(reg);
    i2c_write(block_buffer_length);

    for (uint8_t i = 0; i < block_buffer_length; i++)
    {
         i2c_write(block_buffer[i]);
    }

    i2c_stop();
    return block_buffer_length;
}

void scan_smbus_address(void)
{
    scan_smbus_address_result_ptr = 0;
    
    for (uint8_t i = 3; i < 120; i++)
    {
        bool ack = i2c_start((i << 1) | I2C_WRITE); 

        if (ack)
        {
            i2c_stop();
            scan_smbus_address_result[scan_smbus_address_result_ptr] = i;
            scan_smbus_address_result_ptr++;
            if (scan_smbus_address_result_ptr > 7) scan_smbus_address_result_ptr = 7;
        }

        i2c_stop();
    }

    if (scan_smbus_address_result_ptr > 0) send_usb_packet(status, sd_scan_smbus_address, scan_smbus_address_result, scan_smbus_address_result_ptr);
    else send_usb_packet(status, sd_scan_smbus_address, err, 1);
}

bool is_block_4050(int reg)
{   // ||(reg == LifetimeDataBlock1) 
    if ((reg == ManufacturerName) || (reg == DeviceName) || (reg == DeviceChemistry) || (reg == ManufacturerData) || (reg == SafetyAlert) || (reg == SafetyStatus) 
        || (reg == PFAlert) || (reg == PFStatus) || (reg == OperationStatus) || (reg == ChargingStatus) || (reg == GaugingStatus)|| (reg == ManufacturingStatus) || (reg == LifetimeDataBlock2) 
        || (reg == LifetimeDataBlock3) || (reg == LifetimeDataBlock4) || (reg == LifetimeDataBlock5) || (reg == ManufacturerInfo)
        || (reg == DAStatus1) || (reg == DAStatus2) || (reg == GaugeStatus1) || (reg == GaugeStatus2) || (reg == GaugeStatus3) 
        || (reg == CBStatus) || (reg == StateOfHealth2)
        || (reg == FilteredCapacity)) return true;
    else return false;
}

bool is_block_3060(int reg)
{   // ||(reg == LifetimeDataBlock1) 
    if ((reg == ManufacturerName) || (reg == DeviceName) || (reg == DeviceChemistry) || (reg == ManufacturerData))
    {
        return true;
    }
    else
    {
        return false;
    }
}

void smbus_reg_dump(void)
{

    uint16_t smbus_reg_dump_payload_length = 3*(smbus_reg_end - smbus_reg_start + 1) + 2;
    
    // if condition then is_block is is_block_3060
    // else is_block is is_block_4050
    bool (*is_block)(int);

    uint8_t check = read_block(0x21, buffer);
    if ((check-1) == 0x06) // if length of device name is 6 then it is 3060
    {
        is_block = &is_block_3060;
    }
    else
    {
        is_block = &is_block_4050;
    }
    

    
    for (uint16_t i = smbus_reg_start; i < (smbus_reg_end + 1); i++)
    {
        if (is_block(i)) smbus_reg_dump_payload_length += get_block_length(i) - 2 + 1; // add block length -2 fyrir offset + 1 fyrir lengdina
    }

    uint8_t smbus_reg_dump_payload[smbus_reg_dump_payload_length]; // max 770 bytes
    smbus_reg_dump_payload[0] = smbus_reg_start; // start register
    smbus_reg_dump_payload[1] = smbus_reg_end; // end register
    uint16_t data = 0;
    
    uint16_t position_counter = 0;
    
    for (uint16_t i = smbus_reg_start; i < (smbus_reg_end + 1); i++)
    {
        if (is_block(i)) // read and send block
        {
            uint8_t block_length = read_block(i, buffer);
            uint8_t response_length = block_length + 1;
            uint8_t response[response_length];
            response[0] = i;
            
            for (uint8_t j = 0; j < block_length; j++)
            {
                response[1 + j] = buffer[j];
            }
            smbus_reg_dump_payload[2 + (3*(i-smbus_reg_start)) + position_counter] = i; // register first
            //smbus_reg_dump_payload[3 + (3*(i-smbus_reg_start)) + position_counter] = response_length; // length of the block
            for (uint8_t k = 1; k < response_length; k++)
            {
                smbus_reg_dump_payload[3 + (3*(i-smbus_reg_start)) + position_counter + k - 1] = response[k]; // block data
            }
            position_counter += response_length - 3; //
        }
        else
        {
            data = read_word(i, reverse_read_word_byte_order);
            smbus_reg_dump_payload[2 + (3*(i-smbus_reg_start)) + position_counter] = i; // register first
            smbus_reg_dump_payload[3 + (3*(i-smbus_reg_start)) + position_counter] = (data >> 8) & 0xFF; // high byte of the word there
            smbus_reg_dump_payload[4 + (3*(i-smbus_reg_start)) + position_counter] = data & 0xFF; // low byte of the word there
        }
    }
    
    send_usb_packet(status, sd_smbus_reg_dump, smbus_reg_dump_payload, smbus_reg_dump_payload_length);
}

void read_rom_byte(void)
{
    uint16_t address = 0;
    uint8_t data = 0;
    uint8_t byte_buffer_size = 128; // gather data in 128 bytes chunk
    uint8_t byte_buffer[byte_buffer_size];
    uint8_t byte_buffer_ptr = 0;
    uint8_t byte_payload_size = byte_buffer_size + 2;
    uint8_t byte_payload[byte_payload_size];
    uint8_t counter = 0;
    bool done = false;
    
    while (!done)
    {
        wdt_reset(); // reset watchdog timer here so no autoreset occurs; this while-loop blocks the main loop for more than 4 seconds
        write_word(SetROMAddress, address); // set address to the next row

        counter = 0;
        while (counter < 50)
        {
            data = read_byte(PeekROMByte); // get memory value and save it to the buffer
            if (data != 0x17) break;
            counter++;
            delay(10);
        }
        
        byte_buffer[byte_buffer_ptr] = data; // get memory value and save it to the buffer
        byte_buffer_ptr++;

        if (byte_buffer_ptr == byte_buffer_size)
        {
            
            byte_payload[0] = ((address - (byte_buffer_size - 1)) >> 8) & 0xFF;
            byte_payload[1] = (address - (byte_buffer_size - 1)) & 0xFF;

            for (uint8_t i = 0; i < byte_buffer_size; i++)
            {
                byte_payload[2 + i] = byte_buffer[i];
            }
        
            byte_buffer_ptr = 0; // reset buffer pointer to the beginning
            send_usb_packet(read_data, sd_read_rom_byte, byte_payload, byte_payload_size);
        }

        address++;
        if (address == 0x0800) address = 0x4000; // skip the following values because they are repeating until 0x4000; unique data length is only 0x0800
        if (address == 0x4800) address = 0x8000; // skip this portion of the values because they are repeating until 0x8000; unique data length is only 0x0800
        if (address == 0x8800) done = true;
    }

    delay(100);
    send_usb_packet(ok_error, ok, ack, 1);
}

void read_rom_block(void)
{
    uint16_t address = 0;
    uint8_t block_size = 0x20;
    uint8_t block_buffer_size = block_size + 1; // +1 block size byte
    uint8_t block_buffer[block_buffer_size];
    uint8_t block_payload_length = block_size + 2; // +2 address bytes at the beginning + block without length byte
    uint8_t block_payload[block_payload_length];
    uint8_t counter = 0;
    bool done = false;
    
    while (!done)
    {
        wdt_reset(); // reset watchdog timer here so no autoreset occurs; this while-loop blocks the main loop for more than 4 seconds

        counter = 0;
        do
        {
            write_word(SetROMAddress, address);
            delay(20);
            counter++;
        }
        while ((read_byte(PeekROMBlock) != 0x20) && (counter < 50));

        read_block(PeekROMBlock, block_buffer);
        block_payload[0] = (address >> 8) & 0xFF;
        block_payload[1] = address & 0xFF;

        for (uint8_t i = 0; i < block_size; i++)
        {
            block_payload[2 + i] = block_buffer[1 + i]; // skip first length byte from the block_buffer
        }

        send_usb_packet(read_data, sd_read_rom_block, block_payload, block_payload_length);

        address += block_size;
        if (address == 0x0800) address = 0x4000; // skip the followin values because they are repeating until 0x4000; unique data length is only 0x0800
        if (address == 0x4800) address = 0x8000; // skip this portion of the values because they are repeating until 0x8000; unique data length is only 0x0800
        if (address == 0x8800) done = true;
    }

    delay(100);
    send_usb_packet(ok_error, ok, ack, 1);
}

void update_timestamp(uint8_t *target)
{
    uint32_t mcu_current_millis = millis();
    target[0] = (mcu_current_millis >> 24) & 0xFF;
    target[1] = (mcu_current_millis >> 16) & 0xFF;
    target[2] = (mcu_current_millis >> 8) & 0xFF;
    target[3] = mcu_current_millis & 0xFF;
}

uint8_t calculate_checksum(uint8_t *buff, uint16_t index, uint16_t bufflen)
{
    uint8_t a = 0;
    for (uint16_t i = index ; i < bufflen; i++)
    {
        a += buff[i]; // add bytes together
    }
    return a;
}

/*************************************************************************
Function: free_ram()
Purpose:  returns how many bytes exists between the end of the heap and 
          the last allocated memory on the stack, so it is effectively 
          how much the stack/heap can grow before they collide.
**************************************************************************/
uint16_t free_ram(void)
{
    extern int  __bss_end; 
    extern int  *__brkval; 
    uint16_t free_memory; 
    
    if((int)__brkval == 0)
    {
        free_memory = ((int)&free_memory) - ((int)&__bss_end); 
    }
    else 
    {
        free_memory = ((int)&free_memory) - ((int)__brkval); 
    }
    return free_memory; 

} // end of free_ram

/*************************************************************************
Function: send_usb_packet()
Purpose:  assemble and send data packet through serial link (UART0)
Inputs:   - one source byte,
          - one target byte,
          - one datacode command value byte, these three are used to calculate the DATA CODE byte
          - one SUB-DATA CODE byte,
          - name of the PAYLOAD array (it must be previously filled with data),
          - PAYLOAD length
Returns:  none
Note:     SYNC, LENGTH and CHECKSUM bytes are calculated automatically;
          Payload can be omitted if a (uint8_t*)0x00 value is used in conjunction with 0 length
**************************************************************************/
void send_usb_packet(uint8_t command, uint8_t subdatacode, uint8_t *payloadbuff, uint16_t payloadbufflen)
{
    // Calculate the length of the full packet:
    // PAYLOAD length + 1 SYNC byte + 2 LENGTH byte + 1 DATA CODE byte + 1 SUB-DATA CODE byte + 1 CHECKSUM byte
    uint16_t packet_length = payloadbufflen + 6;    
    bool payload_bytes = true;
    uint8_t datacode = 0;

    // Check if there's enough RAM to store the whole packet
    if (free_ram() < (packet_length + 50)) // require +50 free bytes to be safe
    {
        uint8_t error[7] = { 0x3D, 0x00, 0x03, 0x8F, 0xFD, 0xFF, 0x8E }; // prepare the "not enough MCU RAM" error message
        for (uint8_t i = 0; i < 7; i++)
        {
            Serial.write(error[i]);
        }
        return;
    }

    uint8_t packet[packet_length]; // create a temporary byte-array

    if (payloadbufflen <= 0) payload_bytes = false;
    else payload_bytes = true;

    // Assemble datacode from input parameter
    datacode = command;
    sbi(datacode, 7); // set highest bit to indicate the packet is coming from the device

    // Start assembling the packet by manually filling the first few slots
    packet[0] = 0x3D; // add SYNC byte
    packet[1] = ((packet_length - 4) >> 8) & 0xFF; // add LENGTH high byte
    packet[2] = (packet_length - 4) & 0xFF; // add LENGTH low byte
    packet[3] = datacode; // add DATA CODE byte
    packet[4] = subdatacode; // add SUB-DATA CODE byte
    
    // If there are payload bytes add them too after subdatacode
    if (payload_bytes)
    {
        for (uint16_t i = 0; i < payloadbufflen; i++)
        {
            packet[5 + i] = payloadbuff[i]; // Add message bytes to the PAYLOAD bytes
        }
    }

    // Calculate checksum
    calculated_checksum = calculate_checksum(packet, 1, packet_length - 1);

    // Place checksum byte
    packet[packet_length - 1] = calculated_checksum;

    // Send the prepared packet through serial link
    for (uint16_t i = 0; i < packet_length; i++)
    {
        Serial.write(packet[i]);
    }
    
} // end of send_usb_packet


/*************************************************************************
Function: handle_usb_data()
Purpose:  handle USB commands coming from an external computer
Note:     [ SYNC | LENGTH | DATACODE | SUBDATACODE | <?PAYLOAD?> | CHECKSUM ]
**************************************************************************/
void handle_usb_data(void)
{
    if (Serial.available() > 0) // proceed only if the receive buffer contains at least 1 byte
    {
        uint8_t sync = Serial.read(); // read the next available byte in the USB receive buffer, it's supposed to be the first byte of a message

        if (sync == 0x3D)
        {
            uint8_t length_hb, length_lb, datacode, subdatacode, checksum;
            bool payload_bytes = false;
            uint16_t bytes_to_read = 0;
            uint16_t payload_length = 0;
            uint8_t calculated_checksum = 0;
    
            uint32_t command_timeout_start = 0;
            bool command_timeout_reached = false;
    
            // Wait for the length bytes to arrive (2 bytes)
            command_timeout_start = millis(); // save current time
            while ((Serial.available() < 2) && !command_timeout_reached)
            {
                if (millis() - command_timeout_start > command_purge_timeout) command_timeout_reached = true;
            }
            if (command_timeout_reached)
            {
                send_usb_packet(ok_error, error_packet_timeout_occured, err, 1);
                return;
            }
    
            length_hb = Serial.read(); // read length high byte
            length_lb = Serial.read(); // read length low byte
    
            // Calculate how much more bytes should we read by combining the two length bytes into a word.
            bytes_to_read = (length_hb << 8) + length_lb + 1; // +1 CHECKSUM byte
            
            // Calculate the exact size of the payload.
            payload_length = bytes_to_read - 3; // in this case we have to be careful not to count data code byte, sub-data code byte and checksum byte
    
            // Do not let this variable sink below zero.
            if (payload_length < 0) payload_length = 0; // !!!
    
            // Maximum packet length is 1024 bytes; can't accept larger packets 
            // and can't accept packet without datacode and subdatacode.
            if ((payload_length > 1018) || ((bytes_to_read - 1) < 2))
            {
                send_usb_packet(ok_error, error_length_invalid_value, err, 1);
                return; // exit, let the loop call this function again
            }
    
            // Wait here until all of the expected bytes are received or timeout occurs.
            command_timeout_start = millis();
            while ((Serial.available() < bytes_to_read) && !command_timeout_reached) 
            {
                if (millis() - command_timeout_start > command_timeout) command_timeout_reached = true;
            }
            if (command_timeout_reached)
            {
                send_usb_packet(ok_error, error_packet_timeout_occured, err, 1);
                return; // exit, let the loop call this function again
            }
    
            // There's at least one full command in the buffer now.
            // Go ahead and read one DATA CODE byte (next in the row).
            datacode = Serial.read();
    
            // Read one SUB-DATA CODE byte that's following.
            subdatacode = Serial.read();
    
            // Make some space for the payload bytes (even if there is none).
            uint8_t cmd_payload[payload_length];
    
            // If the payload length is greater than zero then read those bytes too.
            if (payload_length > 0)
            {
                // Read all the PAYLOAD bytes
                for (uint16_t i = 0; i < payload_length; i++)
                {
                    cmd_payload[i] = Serial.read();
                }
                // And set flag so the rest of the code knows.
                payload_bytes = true;
            }
            // Set flag if there are no PAYLOAD bytes available.
            else payload_bytes = false;
    
            // Read last CHECKSUM byte.
            checksum = Serial.read();
    
            // Verify the received packet by calculating what the checksum byte should be.
            calculated_checksum = length_hb + length_lb + datacode + subdatacode; // add the first few bytes together manually
    
            // Add payload bytes here together if present
            if (payload_bytes)
            {
                for (uint16_t j = 0; j < payload_length; j++)
                {
                    calculated_checksum += cmd_payload[j];
                }
            }

            // Compare calculated checksum to the received CHECKSUM byte
            if (calculated_checksum != checksum) // if they are not the same
            {
                send_usb_packet(ok_error, error_checksum_invalid_value, err, 1);
                return; // exit, let the loop call this function again
            }

            // Extract command value from the low nibble (lower 4 bits).
            uint8_t command = datacode & 0x0F;

            // Source is ignored, the packet must come from an external computer through USB
            switch (command) // evaluate command
            {
                case reset: // 0x00 - reset device request
                {
                    send_usb_packet(reset, 0x00, ack, 1); // confirm action
                    while (true); // enter into an infinite loop; watchdog timer doesn't get reset this way so it restarts the program eventually
                    break; // not necessary but every case needs a break
                }
                case handshake: // 0x01 - handshake request coming from an external computer
                {
                    uint8_t handshake_payload[6] = {0x53, 0x42, 0x48, 0x41, 0x43, 0x4B}; // SBHACK
                    send_usb_packet(handshake, 0x00, handshake_payload, 6);
                    break;
                }
                case status: // 0x02 - status report request
                {
                    switch (subdatacode)
                    {
                        case sd_timestamp: // 0x01 - timestamp
                        {
                            update_timestamp(current_timestamp); // this function updates the global byte array "current_timestamp" with the current time
                            send_usb_packet(status, sd_timestamp, current_timestamp, 4);
                            break;
                        }
                        case sd_scan_smbus_address: // 0x02 - scan SMBus
                        {
                            scan_smbus_address();
                            break;
                        }
                        case sd_smbus_reg_dump: // 0x03 - smbus dump
                        {
                            if (!payload_bytes || (payload_length < 2))
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            smbus_reg_start = cmd_payload[0];
                            smbus_reg_end = cmd_payload[1];
                            smbus_reg_dump();
                            break;
                        }
                        default:
                        {
                            send_usb_packet(ok_error, error_subdatacode_invalid_value, err, 1);
                        }
                    }
                    break;
                }
                case settings: // 0x03 - settings
                {
                    switch (subdatacode)
                    {
                        case sd_current_settings: // 0x01 - current settings
                        {
                            uint8_t ret[3] = { 0x00, 0x00, 0x00 };
                            if (reverse_read_word_byte_order) sbi(ret[0], 0);
                            if (reverse_write_word_byte_order) sbi(ret[0], 1);
                            ret[1] = (design_voltage >> 8) & 0xFF;
                            ret[2] = design_voltage & 0xFF;
                            
                            send_usb_packet(settings, sd_current_settings, ret, 3);
                            break;
                        }
                        case sd_set_sb_address: // 0x02 - set smart battery address
                        {
                            if (!payload_bytes)
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            sb_address = cmd_payload[0];
                            
                            send_usb_packet(settings, sd_set_sb_address, cmd_payload, 1);
                            break;
                        }
                        case sd_word_byte_order: // 0x03 - read/write word byte-order
                        {
                            if (!payload_bytes)
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            if (cmd_payload[0] & 0x01) reverse_read_word_byte_order = true;
                            else reverse_read_word_byte_order = false;
                            if (cmd_payload[0] & 0x02) reverse_write_word_byte_order = true;
                            else reverse_write_word_byte_order = false;

                            send_usb_packet(settings, sd_word_byte_order, cmd_payload, 1);
                            break;
                        }
                        default:
                        {
                            send_usb_packet(ok_error, error_subdatacode_invalid_value, err, 1);
                        }
                    }
                    break;
                }
                case read_data: // 0x04 - read data
                {
                    switch (subdatacode) // evaluate SUB-DATA CODE byte
                    {
                        case sd_read_byte: // 0x01 - read byte
                        {
                            if (!payload_bytes)
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            uint8_t response[2];
                            response[0] = cmd_payload[0];
                            response[1] = read_byte(cmd_payload[0]);
                            
                            send_usb_packet(read_data, sd_read_byte, response, 2);
                            break;
                        }
                        case sd_read_word: // 0x02 - read word
                        {
                            if (!payload_bytes)
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            uint8_t response[3];
                            uint16_t temp = read_word(cmd_payload[0], reverse_read_word_byte_order);
                            response[0] = cmd_payload[0];
                            response[1] = (temp >> 8) & 0xff;
                            response[2] = temp & 0xff;
                            
                            send_usb_packet(read_data, sd_read_word, response, 3);
                            break;
                        }
                        case sd_read_block: // 0x03 - read block
                        {
                            if (!payload_bytes)
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            uint8_t block_length = read_block(cmd_payload[0], buffer);
                            uint8_t response_length = block_length + 1;
                            uint8_t response[response_length];
                            response[0] = cmd_payload[0];
                            
                            for (uint8_t i = 0; i < block_length; i++)
                            {
                                response[1 + i] = buffer[i];
                            }
                            
                            send_usb_packet(read_data, sd_read_block, response, response_length);
                            break;
                        }
                        case sd_read_rom_byte: // 0x04 - read rom byte
                        {
                            read_rom_byte();
                            break;
                        }
                        case sd_read_rom_block: // 0x05 - read rom block
                        {
                            read_rom_block();
                            break;
                        }
                        default: // other values are not used
                        {
                            send_usb_packet(ok_error, error_subdatacode_invalid_value, err, 1);
                            break;
                        }
                    }
                    break;
                }
                case write_data: // 0x05 - write data
                {
                    switch (subdatacode) // evaluate SUB-DATA CODE byte
                    {
                        case sd_write_byte: // 0x01 - write byte
                        {
                            if (!payload_bytes || (payload_length < 2))
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            uint8_t result[3];
                            result[0] = cmd_payload[0];
                            result[1] = cmd_payload[1];
                            result[2] = write_byte(cmd_payload[0], cmd_payload[1]);
                            
                            send_usb_packet(write_data, sd_write_byte, result, 3);
                            break;
                        }
                        case sd_write_word: // 0x02 - write word
                        {
                            if (!payload_bytes || (payload_length < 3))
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            uint8_t result[4];
                            result[0] = cmd_payload[0];
                            result[1] = cmd_payload[1];
                            result[2] = cmd_payload[2];
                            result[3] = write_word(cmd_payload[0], (cmd_payload[1] << 8) | cmd_payload[2], reverse_write_word_byte_order);
                            
                            send_usb_packet(write_data, sd_write_word, result, 4);
                            break;
                        }
                        case sd_write_block: // 0x03 - write block
                        {
                            if (!payload_bytes || (payload_length < 2))
                            {
                                send_usb_packet(ok_error, error_payload_invalid_values, err, 1);
                                break;
                            }

                            uint8_t result_length = payload_length + 1;
                            uint8_t result[result_length];
                            uint8_t temp_block_length = payload_length - 1;
                            uint8_t temp_block[temp_block_length];
                            
                            for (uint8_t i = 0; i < result_length - 1; i++)
                            {
                                result[i] = cmd_payload[i];
                            }

                            for (uint8_t i = 0; i < temp_block_length; i++)
                            {
                                temp_block[i] = cmd_payload[i + 1];
                            }
                            
                            result[result_length - 1] = write_block(cmd_payload[0], temp_block, temp_block_length);
                            
                            send_usb_packet(write_data, sd_write_block, result, result_length);
                            break;
                        }
                        default: // other values are not used
                        {
                            send_usb_packet(ok_error, error_subdatacode_invalid_value, err, 1);
                            break;
                        }
                    }
                    break;
                }
                default: // other values are not used
                {
                    send_usb_packet(ok_error, error_datacode_invalid_command, err, 1);
                    break;
                }
            }
        }
        else // if it's not a sync byte
        {
            Serial.read(); // remove this byte from buffer and try again in the next loop
        }
    }
    else
    {
        // what TODO if nothing is in the serial receive buffer
    }
}

void setup()
{
    i2c_init();
    Serial.begin(250000);
    wdt_enable(WDTO_4S); // reset program if it hangs for more than 4 seconds
    send_usb_packet(reset, 0x01, ack, 1); // device ready
}

void loop()
{
    wdt_reset(); // reset watchdog timer to 0 seconds so no accidental restart occurs
    handle_usb_data();
}