import pandas as pd
import warnings

warnings.filterwarnings('ignore')

def read_from_4050(class_, subclass_, data_df, add_read):
    test = data_df.loc[(data_df["CLASS"] == class_) & (data_df["SUBCLASS"] == subclass_)]
    # print out all rows up to the rows where there is more than 32 bytes between any two rows (Address column)
    k = 0
    top = 0 #test["ADDRESS"].iloc[k]
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
            
            #print(f"WRITE BLOCK 0x44 TO ADDRESS 0x{min_address:x}")

            #super().write_block(0x44, address_read)
            #time.sleep(DELAY)
            
            temp_data = []
            #print(f"NUM READS: {num_reads}")
            for j in range(num_reads):
                #print("READ BLOCK 0x44")
                #temp = super().read_block(0x44)
                pass

                #temp_data.extend(temp[3:])
            # read
            # for each row in test[k:i]
            
            for j in range(k,i):
                offset = test["ADDRESS"].iloc[j] - min_address
                #print("offset: ", offset)
                # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
                type_size = int(test["TYPE"].iloc[j][1:])
                actual_address = test["ADDRESS"].iloc[j]
                new_row  = {'CLASS': class_, 'SUBCLASS': subclass_, 'ADDRESS': f"0x{actual_address:x}", 'NAME': test["NAME"].iloc[j], 'CURRENT_ADDRESS': f"0x{min_address:x}", 'NUM_READS': num_reads, 'OFFSET': offset, 'TYPE_SIZE': type_size, 'TYPE': test["TYPE"].iloc[j]}
                add_read = add_read.append(new_row, ignore_index=True)
                #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
                #measured_values.append(temp_data[offset:offset+type_size])
            k = i

    max_address = test["ADDRESS"].iloc[len(test)-1]
    min_address = test["ADDRESS"].iloc[k]
    # convert min address to hex like this 0x4600 -> [0x46, 0x00]
    address_read = [min_address >> 8, min_address & 0xFF]
    #print(f"WRITE BLOCK 0x44 TO ADDRESS 0x{min_address:x}")
    #super().write_block(0x44, address_read)
    #time.sleep(DELAY)
    type_max_address = test.loc[test["ADDRESS"] == max_address, "TYPE"].values[0]
    num_bytes = max_address + int(type_max_address[1:]) - min_address	
    if num_bytes % 32 == 0:
        num_reads = num_bytes // 32
    else:
        num_reads = num_bytes // 32 + 1
    temp_data = []
    #print(f"NUM READS: {num_reads}")
    for j in range(num_reads):
        #print("READ BLOCK 0x44")
        #temp = super().read_block(0x44)
        #temp_data.extend(temp[3:])
        pass
    #print(temp_data)
    for j in range(k,len(test)):
        offset = test["ADDRESS"].iloc[j] - min_address
        #print("offset: ", offset)
        # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
        type_size = int(test["TYPE"].iloc[j][1:])	
        actual_address = test["ADDRESS"].iloc[j]
        new_row  = {'CLASS': class_, 'SUBCLASS': subclass_, 'ADDRESS': f"0x{actual_address:x}", 'NAME': test["NAME"].iloc[j], 'CURRENT_ADDRESS': f"0x{min_address:x}", 'NUM_READS': num_reads, 'OFFSET': offset, 'TYPE_SIZE': type_size, 'TYPE': test["TYPE"].iloc[j]}
        add_read = add_read.append(new_row, ignore_index=True)
        #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
        #measured_values.append(temp_data[offset:offset+type_size])
    return add_read

def read_all_dataflash(data_df, add_read):
    # print all sublaclasses (one of each) to see how many different subclasses there are
    all_classes = data_df["CLASS"].unique()
    all_subclasses = data_df["SUBCLASS"].unique()
    
    for i in all_classes:
        #print(f"----------------- NEW CLASS: {i} -----------------")
        for j in data_df.loc[data_df["CLASS"] == i]["SUBCLASS"].unique():
            #print(f"----------------- NEW SUBCLASS: {j} -----------------")
            add_read = read_from_4050(i,j, data_df, add_read)
        #print(f"--------------------------------------------------")
    return add_read

def check_go(class_, subclass_, data_df, add_reads):
    test = data_df.loc[(data_df["CLASS"] == class_) & (data_df["SUBCLASS"] == subclass_)]
    # take the top address and subtract it from all other addresses
    # for all rows in test
    # subract test["ADDRESS"].iloc[0] from test["ADDRESS"].iloc[i]
    top = test["ADDRESS"].iloc[0]
    last_address = 0
    
    new_row = {'CLASS': class_, 'SUBCLASS': subclass_, 'ADDRESS': f"0x{top:x}"}
    add_reads = add_reads.append(new_row, ignore_index=True)
    for i in range(0,len(test)):
        actual_address = test["ADDRESS"].iloc[i]
        print(f"Actual address: 0x{actual_address:x}")
        d_address = test["ADDRESS"].iloc[i] - top
        print(f"N in subclass: {d_address}")
        diff = d_address-last_address
        print(f"diff: {diff }")
        if diff > 32:
            new_row = {'CLASS': class_, 'SUBCLASS': subclass_, 'ADDRESS': f"0x{actual_address:x}"}
            add_reads = add_reads.append(new_row, ignore_index=True)
        last_address = d_address
    return add_reads

def check(data_df, add_reads):
    # print all sublaclasses (one of each) to see how many different subclasses there are
    all_classes = data_df["CLASS"].unique()
    all_subclasses = data_df["SUBCLASS"].unique()
    m = 0
    for i in all_classes:
        print(f"----------------- NEW CLASS: {i} -----------------")
        for j in data_df.loc[data_df["CLASS"] == i]["SUBCLASS"].unique():
            print(f"----------------- NEW SUBCLASS: {j} -----------------")
            add_reads = check_go(i,j, data_df, add_reads)
            m += 1
        if m > 8:
            break
        print(f"--------------------------------------------------")
    return add_reads

if __name__ == "__main__":
    # Replace 'file_name.pkl' with the name of your pkl file
    df = pd.read_pickle('pkl_files\BQ4050_df.pkl')
    # Create an empty DataFrame
    #address_reads = pd.DataFrame(columns=['CLASS', 'SUBCLASS', 'ADDRESS'])
    address_reads = pd.DataFrame(columns=['CLASS', 'SUBCLASS', 'ADDRESS', 'NAME', 'CURRENT_ADDRESS' ,'NUM_READS', 'OFFSET', 'TYPE_SIZE', 'TYPE'])

    print(address_reads)
    # Print the first few rows of the dataframe to verify that it was loaded correctly
    #print(df.head())
    address_reads = read_all_dataflash(df, address_reads)
    #address_reads = check(df, address_reads)
    # Add the two columns together and place the result in a new column 'c'
    address_reads['TYPE_SIZE'] = address_reads['OFFSET'] + address_reads['TYPE_SIZE']
    address_reads = address_reads.rename(columns={'OFFSET': 'FROM'})
    address_reads = address_reads.rename(columns={'TYPE_SIZE': 'TO'})
    print(address_reads[:20])

    # Convert the ADDRESS column to integers
    address_reads['ADDRESS'] = address_reads['ADDRESS'].apply(lambda x: int(x, 16))

    # Compute the remainder of the ADDRESS column with respect to 32
    address_reads['OFFSET'] = address_reads['ADDRESS'] % 32

    # Round down the ADDRESS column to the nearest 32-byte boundary
    address_reads['ADDRESS'] = address_reads['ADDRESS'].apply(lambda x: x & ~0x1F)

    # Replace the FROM column with the OFFSET column
    address_reads['ADDRESS'] = address_reads['ADDRESS'].apply(lambda x: hex(x))

    # Drop the TO and CURRENT_ADDRESS columns
    address_reads.drop(['TO', 'CURRENT_ADDRESS', 'FROM'], axis=1, inplace=True)


    # Swap the locations of columns B and C
    address_reads = address_reads.reindex(columns=['CLASS', 'SUBCLASS', 'NAME', 'ADDRESS', 'OFFSET', 'NUM_READS', 'TYPE'])

    # Save the modified DataFrame to a new CSV file
    address_reads.to_csv('BQ4050_read_help.csv', index=False)