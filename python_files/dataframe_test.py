import pandas as pd
import pickle

with open('pkl_files\BQ4050_df_golden_file.pkl', 'rb') as file:
    # Dump the dictionary to the file
    data_df = pickle.load(file)

with open('pkl_files\SBS_BQ4050.pkl', 'rb') as file:
    # Dump the dictionary to the file
    data_SBS = pickle.load(file)


print(data_SBS)