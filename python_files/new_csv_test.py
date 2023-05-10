import pandas as pd

def read_from_4050(class_, subclass_, data_df):
    test = data_df.loc[(data_df["CLASS"] == class_) & (data_df["SUBCLASS"] == subclass_)]
    # print out all rows up to the rows where there is more than 32 bytes between any two rows (Address column)
    k = 0
    print(f"| CLASS = {class_} | SUBCLASS = {subclass_}")
    for i in range(1,len(test)):
        if test["ADDRESS"].iloc[i] - test["ADDRESS"].iloc[i-1] > 32:
            xx = test["ADDRESS"].iloc[i] - test["ADDRESS"].iloc[i-1]
            print("INSIDE")
            print(f"xx = {xx}, i = {i}, i-1 = {i-1}")
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
            hex_string = f'{min_address:0>4X}'  
            print(f"WRITING ADDRESS 0x{hex_string} TO 0x44")
            #super().write_block(0x44, address_read)
            #time.sleep(DELAY)
            temp_data = []
            for j in range(num_reads):
                #temp = super().read_block(0x44)
                print("reading 0x44 inside")
                #temp_data.extend(temp[3:])
            # read
            # for each row in test[k:i]
            
            for j in range(k,i):
                offset = test["ADDRESS"].iloc[j] - min_address
                #print("offset: ", offset)
                # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
                type_size = int(test["TYPE"].iloc[j][1:])	
                #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
                #print(f"Offset = {offset}")
                #print(f"Offset+type_size: {offset+type_size}")
                #measured_values.append(temp_data[offset:offset+type_size])
            k = i
    print("OUTSIDE")
    max_address = test["ADDRESS"].iloc[len(test)-1]
    min_address = test["ADDRESS"].iloc[k]
    # convert min address to hex like this 0x4600 -> [0x46, 0x00]
    address_read = [min_address >> 8, min_address & 0xFF]
    
    hex_string = f'{min_address:0>4X}'  
    print(f"WRITING ADDRESS 0x{hex_string} TO 0x44")
    type_max_address = test.loc[test["ADDRESS"] == max_address, "TYPE"].values[0]
    num_bytes = max_address + int(type_max_address[1:]) - min_address	
    if num_bytes % 32 == 0:
        num_reads = num_bytes // 32
    else:
        num_reads = num_bytes // 32 + 1
    temp_data = []
    for j in range(num_reads):
        #temp = super().read_block(0x44)
        #temp_data.extend(temp[3:])
        print("reading 0x44 outside")
        #print(temp_data)
    #print(temp_data)
    for j in range(k,len(test)):
        offset = test["ADDRESS"].iloc[j] - min_address
        #print("offset: ", offset)
        # place temp_data[offset:offset+type_size] in test["MEASURED_VALUE"].iloc[j]
        type_size = int(test["TYPE"].iloc[j][1:])
        #print(f"Offset = {offset}")
        #print(f"Offset+type_size: {offset+type_size}")
        #test["MEASURED_VALUE"].iloc[j] = temp_data[offset:offset+type_size]
        #measured_values.append(temp_data[offset:offset+type_size])
    return 

def read_all_dataflash(data_df):
    # print all sublaclasses (one of each) to see how many different subclasses there are
    all_classes = data_df["CLASS"].unique()
    all_subclasses = data_df["SUBCLASS"].unique()
    
    for i in all_classes:
        for j in data_df.loc[data_df["CLASS"] == i]["SUBCLASS"].unique():
            print("------------- NEW ---------------")
            read_from_4050(i,j, data_df)
            print("---------------------------------\n")

    return


# Load the pickle file into a DataFrame
data_df = pd.read_pickle('pkl_files\\BQ4050_df.pkl')
read_all_dataflash(data_df)