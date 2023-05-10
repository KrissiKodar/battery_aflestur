import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def read_from_3060(class_, subclass_, data_df, add_read):
    test = data_df.loc[(data_df["CLASS"] == class_) & (data_df['SUBCLASS ID'] == subclass_)]
    # subclass ID: number of bytes according to the datasheet for BQ3060
    # bugs = {82: 10, 107: 3, 59: 8, 65: 1}
    two_reads = [34,48,85,106]
    num_reads = 1
    if int(subclass_) in two_reads:
        num_reads = 2
    
    for j in range(len(test)):
        offset = int(test["OFFSET"].iloc[j])
        type = test["TYPE"].iloc[j]
        new_row  = {'CLASS': class_, 'SUBCLASS': test["SUBCLASS"].iloc[j], 'NAME': test["NAME"].iloc[j], 'SUBCLASS ID': subclass_, 'OFFSET': offset, 'NUM_READS': num_reads, 'OFFSET': offset, 'TYPE': type}
        
        add_read = add_read.append(new_row, ignore_index=True)
        print(f"Subclass: {subclass_}")
    return add_read



def read_all_dataflash(data_df, add_read):
    # print all sublaclasses (one of each) to see how many different subclasses there are
    all_classes = data_df["CLASS"].unique()
    all_subclasses = data_df["SUBCLASS ID"].unique()
    for i in all_classes:
        for j in data_df.loc[data_df["CLASS"] == i]["SUBCLASS ID"].unique():
            #print("i: ", i, "j: ", j)
            add_read = read_from_3060(i,j, data_df, add_read)
    return add_read

if __name__ == "__main__":
    # Replace 'file_name.pkl' with the name of your pkl file
    df = pd.read_pickle('pkl_files\BQ3060_df.pkl')
    print(list(df.columns.values))
    # Create an empty DataFrame
    address_reads = pd.DataFrame(columns=['CLASS', 'SUBCLASS', 'NAME', 'SUBCLASS ID', 'OFFSET', 'NUM_READS', 'TYPE'])

    # Print the first few rows of the dataframe to verify that it was loaded correctly
    address_reads = read_all_dataflash(df, address_reads)
    print("test")
    print(address_reads[:20])
    address_reads.to_csv('example_rheo.csv', index=False)