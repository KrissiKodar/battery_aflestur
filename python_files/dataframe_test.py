import pandas as pd
import pickle

### save BQ4050 dataflash golden file ###
with open('pkl_files\BQ4050_df_golden_file.pkl', 'rb') as file:
    # Dump the dictionary to the file
    data_df = pickle.load(file)


print(data_df)

if "SUBCLAS" in data_df:
    print("yes")