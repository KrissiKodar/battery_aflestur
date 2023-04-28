import serial
from serial.tools import list_ports
from serial import Serial
import sys
import time
import pickle
import pandas as pd
import struct

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pyodbc

##########################################################

DELAY = 0.02


class battery_gauge:
    def __init__(self, ser):
        # wait for Arduino to be ready
        # self.wait_and_print()
        self.ser = ser
    
    # for startup
    def wait_for_connection(self):
        self.wait_and_print()
        
    def identify_device(self):
        # identify device
        which_battery = self.read_block(0x21) # read device name
        which_battery = which_battery[1:]
        which_battery = ''.join(chr(int(i, 16)) for i in which_battery)
        print("which_battery: ", which_battery)

        return which_battery
    
    def serial_number(self):
        serial_number = self.read_word(0x1c) # read device serial number
        serial_number = self.bytes_to_hex(serial_number)
        print("serial_number: ", serial_number)
        return serial_number

    def bytes_to_hex(self, data):
        return " ".join([hex(b)[2:].zfill(2) for b in data])

    # same as bytes to hex but put them in a list
    def bytes_to_hex_list(self, data):
        return [hex(b)[2:].zfill(2) for b in data]

    # function that only waits and prints out recieved bytes
    # it should wait until at least 1 byte is available
    # for startup
    def wait_and_print(self):
        print()
        while True:
            time.sleep(0.2)
            if self.ser.in_waiting > 0:
                #print(f'read {self.ser.in_waiting} bytes')
                data = self.ser.read(self.ser.in_waiting)
                #print(self.bytes_to_hex_list(data))
                break
        print()

    # for startup
    def wait_and_get_data(self):
        while True:
            time.sleep(DELAY+0.08)
            if self.ser.in_waiting > 0:
                #print(f'read {self.ser.in_waiting} bytes')
                data = self.ser.read(self.ser.in_waiting)
                #print(bytes_to_hex(data))
                # put data in 2 nd index of list of dict
                data_read = self.bytes_to_hex_list(data)
                #remove first 5 bytes from the list and also the last byte
                data_read = data_read[6:-1]
                break
        return data_read

    def send_command(self, command):
        # take sum everything except the first byte and add it to the end of the command
        command.append(sum(command[1:]) % 256)
        #print("sending command: ", bytes_to_hex(command))
        self.ser.write(command)
        #wait_and_print()
        return self.wait_and_get_data()

    def write_word(self, address, data):
        # write 2 bytes to the given address
        write_word = [0x3D, 0x00, 0x05, 0x05, 0x02, address, data[1], data[0]]
        return self.send_command(write_word)
    
    def write_block(self, address, data):
        write_block = [0x3D, 0x00, 0x05, 0x05, 0x03, address, data[1], data[0]] # ath svissast
        return self.send_command(write_block)

    
    def read_word(self, address):
        # read 2 bytes from the given address
        read_word = [0x3D, 0x00, 0x03, 0x04, 0x02, address]
        return self.send_command(read_word)

    def read_block(self, address):
        read_block = [0x3D, 0x00, 0x03, 0x04, 0x03, address]
        return self.send_command(read_block)

    def read_SBS_from_battery(self, registers):
        for key, value in registers.items():
            if value[0] == 'word':
                value[2] = self.read_word(value[1])
            elif value[0] == 'block':
                value[2] = self.read_block(value[1])
        self.order_bytes(registers)
    
    def order_bytes(self, registers):
        for key, value in registers.items():
            if value[0] == 'block':
                if value[-1] == 'flags':
                    # if list not empty
                    if value[2]:
                        if value[2][0] == '03':
                            # remove first index of list
                            value[2].pop(0)
                            # reverse the last 2 indexes of the list
                            value[2][-2:] = value[2][-1], value[2][-2]
                        elif value[2][0] == '04': 
                            # remove first index of list
                            value[2].pop(0)
                            # revere the last 2 indexes of the list
                            value[2][-2:] = value[2][-1], value[2][-2]
                            # reverse the first 2 indexes of the list
                            value[2][:2] = value[2][1], value[2][0]

    def read_SBS_from_battery_new(self, df):
        
        # df is dataframe
        # for all values in column "SBS_CMD"
        SBS_list = []
        for i in df.loc[:, "SBS_CMD"]:
            sbs_command = int(i, 16)
            # if column "SIZE_IN_BYTES" is bigger than 2 do block read
            if int(df.loc[df["SBS_CMD"] == i, "SIZE_IN_BYTES"].values[0]) > 2:
                # do block, read and put result in column "MEASURED_VALUE"
                BlockRead = self.read_block(sbs_command)
                # print address and value
                #print("0x{:02x} : {}".format(sbs_command, BlockRead))
                SBS_list.append(BlockRead)
            else:
                # do word read and put result in column "MEASURED_VALUE"
                WordRead = self.read_word(sbs_command)
                #print("0x{:02x} : {}".format(sbs_command, WordRead))
                SBS_list.append(WordRead)
        return SBS_list


    def bytes_to_hex(self, data): # must be even number of bytes >= 2
        # make letters in data upper case
        for i in range(len(data)):
            k = data[i]
            data[i] = k.upper()	
        ret = '0x'
        # append each byte to ret
        for i in range(len(data)):	
            ret += data[i]	
        return ret

    def to_signed_int_SBS(self, bytes):
        num = int(bytes[0] + bytes[1], 16)
        if num >= 2**15:
            num -= 2**16
        return num

    def to_signed_byte(self, byte):
        num = int(byte, 16)
        if num >= 2**7:
            num -= 2**8
        return num   

    def unsigned_word_to_date(self, word):
        # make word 16 bits long
        word = word & 0xFFFF
        # convert word to binary string
        binary = bin(word)[2:].zfill(16)
        # get year
        year = int(binary[:7], 2) + 1980
        # get month
        month = int(binary[7:11], 2)
        # get day
        day = int(binary[11:], 2)
        date_string = f'{day}.{month}.{year}'
        return date_string


    def SBS_update_dataframe(self, df):
    # if SIZE_IN_BYTES > 2 then remove first item from MEASURED_VALUE list
        for index, row in df.iterrows():
            if int(row["SIZE_IN_BYTES"]) > 2:
                value = row["MEASURED_VALUE"]
                # remove first item from list
                value.pop(0)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = value

        for index, row in df.iterrows():
            # if "SIZE_IN_BYTES" > 3 and "UNIT" is not "ASCII" and "NAME"
            if int(row["SIZE_IN_BYTES"]) > 3 and row["UNIT"] != "ASCII":
                value = row["MEASURED_VALUE"]
                # flip order of list elements, first flip first two elements, then the next two, etc.
                if len(value) % 2 == 0:
                    for i in range(0, len(value), 2):
                        value[i], value[i+1] = value[i+1], value[i]
                value = self.bytes_to_hex(value)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = value


        for index, row in df.iterrows():
            # if FORMAT is "integer" and "SIZE_IN_BYTES" is 2
            if row["FORMAT"] == 'integer' and int(row["SIZE_IN_BYTES"]) == 2:
                value = row["MEASURED_VALUE"]
                value = self.to_signed_int_SBS(value)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = value
            # if FORMAT is "integer" and "SIZE_IN_BYTES" is 1
            if row["FORMAT"] == 'integer' and int(row["SIZE_IN_BYTES"]) == 1:
                value = row["MEASURED_VALUE"]
                value = self.to_signed_byte(value)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = value
            # if FORMAT is "unsigned int" and "SIZE_IN_BYTES" is 2
            if row["FORMAT"] == 'unsigned int' and int(row["SIZE_IN_BYTES"]) == 2:
                value = row["MEASURED_VALUE"]
                value = int(value[0]+value[1],16)
                # if NAME is ManufacturerDate then convert to date
                if row["NAME"] == "ManufacturerDate" or row["NAME"] == "ManufactureDate":
                    value = self.unsigned_word_to_date(value)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = value
            # FORMAT is "unsigned int" and "SIZE_IN_BYTES" is 1
            if row["FORMAT"] == 'unsigned int' and int(row["SIZE_IN_BYTES"]) == 1:
                value = row["MEASURED_VALUE"]
                value = int(value[1],16)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = value

            # if FORMAT is hex and "SIZE_IN_BYTES" is 2 or 1
            if row["FORMAT"] == 'hex' and (int(row["SIZE_IN_BYTES"]) == 2 or int(row["SIZE_IN_BYTES"]) == 1):
                value = row["MEASURED_VALUE"]
                value = self.bytes_to_hex(value)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = value
            
            # if FORMAT is "string" and UNIT is "ASCII"
            if row["FORMAT"] == 'string' and row["UNIT"] == "ASCII":
                value = row["MEASURED_VALUE"]
                string_from_reg = ''.join(chr(int(i, 16)) for i in value)
                # update MEASURED_VALUE
                df.at[index, "MEASURED_VALUE"] = string_from_reg
# BQ40z50-r2
class BQ4050(battery_gauge):
# init function
    def __init__(self, ser, data_df= None, data_SBS = None):
        super().__init__(ser)
        
        self.data_df = data_df
        self.data_SBS = data_SBS
        self.measured_values = []
        
    ################################################################################
    # specific functions for dataflash, because the byte order is flipped relative
    # to the SBS reading (for the BQ4050, little endian)
    def to_signed_int_dataflash(self, bytes):
        num = int(bytes[1] + bytes[0], 16)
        if num >= 2**15:
            num -= 2**16
        return num

    def to_unsigned_int_dataflash(self, bytes):
        return int(bytes[1] + bytes[0], 16)
    
    def bytes_to_hex_dataflash(self, data): # must be even number of bytes >= 2
        # flip first and second byte then flip third and fourth byte and so on
        if len(data) > 1:
            for i in range(0, len(data), 2):	
                data[i], data[i+1] = data[i+1], data[i]
        # make letters in data upper case
        for i in range(len(data)):
            k = data[i]
            data[i] = k.upper()	
        ret = '0x'
        # append each byte to ret
        for i in range(len(data)):	
            ret += data[i]	
        return ret

    # not correct I think
    def bytes_to_float(self, data):
        for i in range(0, len(data), 2):	
                data[i], data[i+1] = data[i+1], data[i]
        int_list = [int(i, 16) for i in data]
        bin_str = struct.pack('4B', *int_list)
        float_num = struct.unpack('f', bin_str)[0]
        return float_num
    
    def to_signed_byte(self, byte):
        num = int(byte, 16)
        if num >= 2**7:
            num -= 2**8
        return num             

    def read_basic_SBS_new(self):
        from_reads_SBS = super().read_SBS_from_battery_new(self.data_SBS)
        self.data_SBS["MEASURED_VALUE"] = from_reads_SBS
        super().SBS_update_dataframe(self.data_SBS)

    def read_from_4050(self, class_, subclass_):
        test = self.data_df.loc[(self.data_df["CLASS"] == class_) & (self.data_df["SUBCLASS"] == subclass_)]
        # print out all rows up to the rows where there is more than 32 bytes between any two rows (Address column)
        k = 0
        for i in range(1,len(test)):
            if test["ADDRESS"].iloc[i] - test["ADDRESS"].iloc[i-1] > 32:
                #print(test.iloc[k:i])"UNITS"
                max_address = test["ADDRESS"].iloc[i-1]
                min_address = test["ADDRESS"].iloc[k]
                type_max_address = test.loc[test["ADDRESS"] == max_address, "TYPE"].values[0]	
                num_bytes = max_address + int(type_max_address[1:]) - min_address
                if num_bytes % 32 == 0:
                    num_reads = num_bytes // 32
                else:
                    num_reads = num_bytes // 32 + 1
                #print("Num_bytes: ", num_bytes)
                #print("Num_reads: ", num_reads)
                
                # convert min address to hex like this 0x4600 -> [0x46, 0x00]
                address_read = [min_address >> 8, min_address & 0xFF]
                
                super().write_block(0x44, address_read)
                time.sleep(DELAY)
                
                temp_data = []
                for j in range(num_reads):
                    temp = super().read_block(0x44)

                    temp_data.extend(temp[3:])
                # read
                # for each row in test[k:i]
                
                for j in range(k,i):
                    offset = test["ADDRESS"].iloc[j] - min_address
                    #print("offset: ", offset)
                    # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
                    type_size = int(test["TYPE"].iloc[j][1:])	
                    #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
                    self.measured_values.append(temp_data[offset:offset+type_size])
                k = i

        max_address = test["ADDRESS"].iloc[len(test)-1]
        min_address = test["ADDRESS"].iloc[k]
        # convert min address to hex like this 0x4600 -> [0x46, 0x00]
        address_read = [min_address >> 8, min_address & 0xFF]
        super().write_block(0x44, address_read)
        time.sleep(DELAY)
        type_max_address = test.loc[test["ADDRESS"] == max_address, "TYPE"].values[0]
        num_bytes = max_address + int(type_max_address[1:]) - min_address	
        if num_bytes % 32 == 0:
            num_reads = num_bytes // 32
        else:
            num_reads = num_bytes // 32 + 1
        temp_data = []
        for j in range(num_reads):
            temp = super().read_block(0x44)
            temp_data.extend(temp[3:])
        #print(temp_data)
        for j in range(k,len(test)):
            offset = test["ADDRESS"].iloc[j] - min_address
            #print("offset: ", offset)
            # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
            type_size = int(test["TYPE"].iloc[j][1:])	
            #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
            self.measured_values.append(temp_data[offset:offset+type_size])
        return 

    def read_all_dataflash(self):
        # print all sublaclasses (one of each) to see how many different subclasses there are
        all_classes = self.data_df["CLASS"].unique()
        all_subclasses = self.data_df["SUBCLASS"].unique()
        
        for i in all_classes:
            for j in self.data_df.loc[self.data_df["CLASS"] == i]["SUBCLASS"].unique():
                self.read_from_4050(i,j)

        # place mesured values in data_df column "MEASURED_VALUE"
        #print("len(self.measured_values): ", len(self.measured_values))
        #print("shape of data_df: ", self.data_df.shape)
        # place MEASURED_VALUEs in data_df (column "MEASURED_VALUE")
        self.data_df["MEASURED_VALUE"] = self.measured_values
        # if type is I2, convert to int
        for i in range(len(self.data_df)):	
            if self.data_df["TYPE"].iloc[i] == "I2":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_signed_int_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "U2":
                value = self.to_unsigned_int_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
                if self.data_df["NAME"].iloc[i] == "Manufacture Date":
                    value = super().unsigned_word_to_date(value)
                self.data_df["MEASURED_VALUE"].iloc[i] = value
            elif self.data_df["TYPE"].iloc[i] == "H1" or self.data_df["TYPE"].iloc[i] == "H2" or self.data_df["TYPE"].iloc[i] == "H4":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.bytes_to_hex_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "F4":
                # byte to floating point conversion
                value = (self.data_df["MEASURED_VALUE"].iloc[i])[::-1]
                value = ''.join(value)
                value = struct.unpack('!f', bytes.fromhex(value))[0]
                self.data_df["MEASURED_VALUE"].iloc[i] = value	
            # elif first letter of Type is S (string)
            elif self.data_df["TYPE"].iloc[i][0] == "S":
                string_from_reg = ''.join(chr(int(i, 16)) for i in self.data_df["MEASURED_VALUE"].iloc[i])
                self.data_df["MEASURED_VALUE"].iloc[i] = string_from_reg
            elif self.data_df["TYPE"].iloc[i] == "U1":
                self.data_df["MEASURED_VALUE"].iloc[i] = int(self.data_df["MEASURED_VALUE"].iloc[i][0], 16)
            elif self.data_df["TYPE"].iloc[i] == "I1":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_signed_byte(self.data_df["MEASURED_VALUE"].iloc[i][0])
        return

# bq3060
class BQ3060(battery_gauge):
# init function
    def __init__(self, ser, data_df= None, data_SBS = None):
        super().__init__(ser)

        self.data_df = data_df
        self.data_SBS = data_SBS
        self.measured_values = []

         
    def to_signed_int(self, bytes):
        num = int(bytes[0] + bytes[1], 16)
        if num >= 2**15:
            num -= 2**16
        return num

    def to_unsigned_int(self, bytes):
        return int(bytes[0] + bytes[1], 16)


    def bytes_to_hex(self, data): # must be even number of bytes >= 2

            # make letters in data upper case
            for i in range(len(data)):
                k = data[i]
                data[i] = k.upper()	
            ret = '0x'
            # append each byte to ret
            for i in range(len(data)):	
                ret += data[i]	
            return ret
    
    def bytes_to_float_dataflash(self, data):
        int_list = [int(i, 16) for i in data]
        bin_str = struct.pack('4B', *int_list)
        float_num = struct.unpack('>f', bin_str)[0]
        return float_num
    
    def to_signed_byte(self, byte):
        num = int(byte, 16)
        if num >= 2**7:
            num -= 2**8
        return num
    
    def read_basic_SBS_new(self):
        from_reads_SBS = super().read_SBS_from_battery_new(self.data_SBS)
        self.data_SBS["MEASURED_VALUE"] = from_reads_SBS
        super().SBS_update_dataframe(self.data_SBS)

    # read dataflash from bq3060
    def read_from_3060(self, class_, subclass_):
        test = self.data_df.loc[(self.data_df["CLASS"] == class_) & (self.data_df['SUBCLASS ID'] == subclass_)]
        # subclass ID: number of bytes according to the datasheet for BQ3060
        # bugs = {82: 10, 107: 3, 59: 8, 65: 1}
        two_reads = [34,48,85,106]
        
        
        time.sleep(DELAY)
        super().write_word(0x77, [int(subclass_), 0x00])
        time.sleep(DELAY)

        time.sleep(DELAY)
        DC1 = super().read_block(0x78)
        time.sleep(DELAY)
        # remove first 1 bytes (which is just the length of the data)
        DC1 = DC1[1:]



        if int(subclass_) in two_reads:
            time.sleep(DELAY)
            DC2 = super().read_block(0x79)
            time.sleep(DELAY)
            DC2 = DC2[1:]
            DC1.extend(DC2)
        
        for j in range(len(test)):
            offset = int(test["OFFSET"].iloc[j])
            type_size = int(test["TYPE"].iloc[j][1:])	
            self.measured_values.append(DC1[offset:offset+type_size])
        return
            
    def read_all_dataflash(self):

        # print all sublaclasses (one of each) to see how many different subclasses there are
        all_classes = self.data_df["CLASS"].unique()
        all_subclasses = self.data_df["SUBCLASS ID"].unique()
        for i in all_classes:
            for j in self.data_df.loc[self.data_df["CLASS"] == i]["SUBCLASS ID"].unique():
                #print("i: ", i, "j: ", j)
                self.read_from_3060(i,j)

        self.data_df["MEASURED_VALUE"] = self.measured_values
        for i in range(len(self.data_df)):	
            if self.data_df["TYPE"].iloc[i] == "I2":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_signed_int(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "U2":
                value = self.to_unsigned_int(self.data_df["MEASURED_VALUE"].iloc[i])
                if self.data_df["NAME"].iloc[i] == "Manuf Date":
                    print("\n\n\n")
                    print("before: ", value)
                    print("\n\n\n")
                    value = super().unsigned_word_to_date(value)
                    print("\n\n\n")
                    print("date_string: ", value)
                    print("\n\n\n")
                self.data_df["MEASURED_VALUE"].iloc[i] = value
            elif self.data_df["TYPE"].iloc[i] == "H1" or self.data_df["TYPE"].iloc[i] == "H2" or self.data_df["TYPE"].iloc[i] == "H4":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.bytes_to_hex(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "F4":
                # add byte to floating point conversion later
                #print("F4")
                #print(self.data_df["MEASURED_VALUE"].iloc[i])
                pass	
            # elif first letter of DATA TYPE is S (string)
            elif self.data_df["TYPE"].iloc[i][0] == "S":
                string_from_reg = ''.join(chr(int(i, 16)) for i in self.data_df["MEASURED_VALUE"].iloc[i])
                self.data_df["MEASURED_VALUE"].iloc[i] = string_from_reg
            elif self.data_df["TYPE"].iloc[i] == "U1":
                self.data_df["MEASURED_VALUE"].iloc[i] = int(self.data_df["MEASURED_VALUE"].iloc[i][0], 16)
            elif self.data_df["TYPE"].iloc[i] == "I1":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_signed_byte(self.data_df["MEASURED_VALUE"].iloc[i][0])
        return

class BQ78350(battery_gauge):
# init function
    def __init__(self, ser, data_df= None, data_SBS = None):
        super().__init__(ser)
        
        self.data_df = data_df
        self.data_SBS = data_SBS
        self.measured_values = []
    
    # sealing/unsealing functions
    def read_unseal_key(self):
        security_key_address = 0x0035
        address_read = [security_key_address >> 8, security_key_address & 0xFF]
        super().write_block(0x44, address_read)
        time.sleep(DELAY)
        temp = super().read_block(0x44)
        print("temp raw: ", temp)
        temp = temp[3:]
        print("temp after (security key??): ", temp)

    def read_unseal_key2(self):
        security_key_address = 0x0035
        address_read = [security_key_address >> 8, security_key_address & 0xFF]
        super().write_word(0x00, address_read)
        time.sleep(DELAY)
        temp = super().read_block(0x23)
        print("temp raw: ", temp)
        temp = temp[1:]
        print("temp after (security key??): ", temp)

    def unseal_battery(self):
        print("Attempting to unseal battery...")
        # the unseal key is 0x3672 0x0414
        # for now we have to send 0x0414 flipped --> 0x1404 first to 0x00
        # and then send 0x3672 flipped --> 0x7236 to 0x00 next

        # first unseal
        #unseal_key_first_word = 0x3672
        unseal_key_first_word = 0x1404
        #unseal_key_first_word = 0x7236 # unseal_key_first_word_flipped
        unseal_key_first_word_send  = [unseal_key_first_word >> 8, unseal_key_first_word & 0xFF]
        super().write_word(0x00, unseal_key_first_word_send)
        time.sleep(DELAY)
        # unseal_key_second_word = 0x0414
        unseal_key_second_word = 0x7236
        #unseal_key_second_word = 0x1404 # unseal_key_second_word_flipped
        unseal_key_second_word_send  = [unseal_key_second_word >> 8, unseal_key_second_word & 0xFF]
        super().write_word(0x00, unseal_key_second_word_send)
        time.sleep(DELAY+2)
        print("Attempting to go to full access mode...")
        # then full access (FA)
        FA_key_first_word = 0xFFFF
        FA_key_first_word_send  = [FA_key_first_word >> 8, FA_key_first_word & 0xFF]
        super().write_word(0x00, FA_key_first_word_send)
        time.sleep(DELAY)
        FA_key_second_word = 0xFFFF
        FA_key_second_word_send  = [FA_key_second_word >> 8, FA_key_second_word & 0xFF]
        super().write_word(0x00, FA_key_second_word_send)
        time.sleep(DELAY) 

    def seal_battery(self):
        print("Attempting to seal battery...")
        #seal_word = 0x0030
        seal_word = 0x3000 # seal_word_flipped (because of how I set up the write word function
        seal_word_send  = [seal_word >> 8, seal_word & 0xFF]
        super().write_word(0x00, seal_word_send )
        time.sleep(DELAY)
        
        


    ################################################################################
    # specific functions for dataflash, because the byte order is flipped relative
    # to the SBS reading (for the BQ78350, little endian)
    def to_signed_int_dataflash(self, bytes):
        num = int(bytes[0] + bytes[1], 16)
        if num >= 2**15:
            num -= 2**16
        return num
    
    def to_signed_long_dataflash(self, byte_list):
        bytes_obj = bytes.fromhex(''.join(byte_list)) # Convert hex strings to bytes object
        num = int.from_bytes(bytes_obj, 'big') # Convert bytes object to int
        return num
    

    def to_unsigned_int_dataflash(self, bytes):
        return int(bytes[0] + bytes[1], 16)
    
    def to_unsigned_long_dataflash(self, byte_list):
        bytes_obj = bytes.fromhex(''.join(byte_list)) # Convert hex strings to bytes object
        num = int.from_bytes(bytes_obj, 'big') # Convert bytes object to int
        return num
    
    def bytes_to_hex_dataflash(self, data): # must be even number of bytes >= 2
        # flip first and second byte then flip third and fourth byte and so on
        #print("data before: ", data)
        #if len(data) > 1:
        #    for i in range(0, len(data), 2):	
        #        data[i], data[i+1] = data[i+1], data[i]
        #    #print("data after: ", data)
        # make letters in data upper case
        for i in range(len(data)):
            k = data[i]
            data[i] = k.upper()	
        ret = '0x'
        # append each byte to ret
        for i in range(len(data)):	
            ret += data[i]	
        return ret

    # not correct I think
    def bytes_to_float(self, data):
        for i in range(0, len(data), 2):	
                data[i], data[i+1] = data[i+1], data[i]
        int_list = [int(i, 16) for i in data]
        bin_str = struct.pack('4B', *int_list)
        float_num = struct.unpack('f', bin_str)[0]
        return float_num
    
    def to_signed_byte(self, byte):
        num = int(byte, 16)
        if num >= 2**7:
            num -= 2**8
        return num             

    def read_basic_SBS_new(self):
        from_reads_SBS = super().read_SBS_from_battery_new(self.data_SBS)
        self.data_SBS["MEASURED_VALUE"] = from_reads_SBS
        super().SBS_update_dataframe(self.data_SBS)

    def read_from_78350(self, class_, subclass_):
        test = self.data_df.loc[(self.data_df["CLASS"] == class_) & (self.data_df["SUBCLASS"] == subclass_)]
        # print out all rows up to the rows where there is more than 32 bytes between any two rows (Address column)
        k = 0
        for i in range(1,len(test)):
            if test["ADDRESS"].iloc[i] - test["ADDRESS"].iloc[i-1] > 32:
                #print(test.iloc[k:i])
                max_address = test["ADDRESS"].iloc[i-1]
                min_address = test["ADDRESS"].iloc[k]
                type_max_address = test.loc[test["ADDRESS"] == max_address, "TYPE"].values[0]	
                num_bytes = max_address + int(type_max_address[1:]) - min_address
                if num_bytes % 32 == 0:
                    num_reads = num_bytes // 32
                else:
                    num_reads = num_bytes // 32 + 1
                #print("Num_bytes: ", num_bytes)
                #print("Num_reads: ", num_reads)
                
                # convert min address to hex like this 0x4600 -> [0x46, 0x00]
                address_read = [min_address >> 8, min_address & 0xFF]
                
                super().write_block(0x44, address_read)
                time.sleep(DELAY)
                
                temp_data = []
                for j in range(num_reads):
                    temp = super().read_block(0x44)

                    temp_data.extend(temp[3:])
                # read
                # for each row in test[k:i]
                
                for j in range(k,i):
                    offset = test["ADDRESS"].iloc[j] - min_address
                    #print("offset: ", offset)
                    # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
                    type_size = int(test["TYPE"].iloc[j][1:])	
                    #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
                    # print address, type, MEASURED_VALUE
                    #print(test["ADDRESS"].iloc[j], test["TYPE"].iloc[j], temp_data[offset:offset+type_size])
                    self.measured_values.append(temp_data[offset:offset+type_size])
                k = i

        max_address = test["ADDRESS"].iloc[len(test)-1]
        min_address = test["ADDRESS"].iloc[k]
        # convert min address to hex like this 0x4600 -> [0x46, 0x00]
        address_read = [min_address >> 8, min_address & 0xFF]
        super().write_block(0x44, address_read)
        time.sleep(DELAY)
        type_max_address = test.loc[test["ADDRESS"] == max_address, "TYPE"].values[0]
        num_bytes = max_address + int(type_max_address[1:]) - min_address	
        if num_bytes % 32 == 0:
            num_reads = num_bytes // 32
        else:
            num_reads = num_bytes // 32 + 1
        temp_data = []
        for j in range(num_reads):
            temp = super().read_block(0x44)
            temp_data.extend(temp[3:])
        #print(temp_data)
        for j in range(k,len(test)):
            offset = test["ADDRESS"].iloc[j] - min_address
            #print("offset: ", offset)
            # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
            type_size = int(test["TYPE"].iloc[j][1:])	
            #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
            self.measured_values.append(temp_data[offset:offset+type_size])
        return 

    def read_all_dataflash(self):
        # print all sublaclasses (one of each) to see how many different subclasses there are
        all_classes = self.data_df["CLASS"].unique()
        all_subclasses = self.data_df["SUBCLASS"].unique()
        
        for i in all_classes:
            #print("Class: ", i)
            for j in self.data_df.loc[self.data_df["CLASS"] == i]["SUBCLASS"].unique():
                #print("Subclass: ", j)
                self.read_from_78350(i,j)

        self.data_df["MEASURED_VALUE"] = self.measured_values
        # if type is I2, convert to int
        for i in range(len(self.data_df)):	
            if self.data_df["TYPE"].iloc[i] == "I2":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_signed_int_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "U2":
                value = self.to_unsigned_int_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
                if self.data_df["NAME"].iloc[i] == "Manufacture Date":
                    value = super().unsigned_word_to_date(value)
                self.data_df["MEASURED_VALUE"].iloc[i] = value
            elif self.data_df["TYPE"].iloc[i] == "U4":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_unsigned_long_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "I4":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_signed_long_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "H1" or self.data_df["TYPE"].iloc[i] == "H2" or self.data_df["TYPE"].iloc[i] == "H4":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.bytes_to_hex_dataflash(self.data_df["MEASURED_VALUE"].iloc[i])
            elif self.data_df["TYPE"].iloc[i] == "F4":
                # add byte to floating point conversion later
                #print("F4")
                #print(self.data_df["MEASURED_VALUE"].iloc[i])
                #self.data_df["MEASURED_VALUE"].iloc[i] = self.bytes_to_float(self.data_df["MEASURED_VALUE"].iloc[i])
                # do nothing
                pass	
            # elif first letter of Type is S (string)
            elif self.data_df["TYPE"].iloc[i][0] == "S":
                string_from_reg = ''.join(chr(int(i, 16)) for i in self.data_df["MEASURED_VALUE"].iloc[i])
                self.data_df["MEASURED_VALUE"].iloc[i] = string_from_reg
            elif self.data_df["TYPE"].iloc[i] == "U1":
                self.data_df["MEASURED_VALUE"].iloc[i] = int(self.data_df["MEASURED_VALUE"].iloc[i][0], 16)
            elif self.data_df["TYPE"].iloc[i] == "I1":
                self.data_df["MEASURED_VALUE"].iloc[i] = self.to_signed_byte(self.data_df["MEASURED_VALUE"].iloc[i][0])

        return


