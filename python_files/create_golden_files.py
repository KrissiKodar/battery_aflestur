from tabula.io import read_pdf
import pandas as pd
import pickle

 ### BQ4050 dataflash golden file ###
with open('pkl_files\BQ4050_0x0036_dataflash.pkl', 'rb') as file:
    # Load the dictionary from the file
    data_df = pickle.load(file)

### save BQ4050 dataflash golden file ###
with open('pkl_files\BQ4050_df_golden_file.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(data_df, file)


### BQ3060 dataflash golden file ###
with open('pkl_files\BQ3060_0x2203_dataflash.pkl', 'rb') as file:
    # Load the dictionary from the file
    data_df = pickle.load(file)

### save BQ3060 dataflash golden file ###
with open('pkl_files\BQ3060_df_golden_file.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(data_df, file)

### BQ78350 dataflash golden file ###
with open('pkl_files\BQ78350_0x0000_dataflash.pkl', 'rb') as file:
    # Load the dictionary from the file
    data_df = pickle.load(file)

### save BQ78350 dataflash golden file ###
with open('pkl_files\BQ78350_df_golden_file.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(data_df, file)




