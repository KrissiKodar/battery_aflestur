import os
import pickle
import pandas as pd

# Set the input and output directory paths
input_dir = "pkl_files"
output_dir = "csv_files"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all .pkl files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".pkl"):
        # Load the pickle file
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Save the DataFrame as a CSV file in the output directory
        output_filename = filename[:-4] + ".csv"
        output_path = os.path.join(output_dir, output_filename)
        df.to_csv(output_path, index=False, encoding='utf-8')

print("Conversion complete!")


import csv

# open the CSV file
with open('csv_files/BQ4050_df.csv', 'r', encoding='utf-8') as file:

    # create a CSV reader object
    csv_reader = csv.reader(file)

    # loop through the rows and print the top contents
    for i, row in enumerate(csv_reader):
        if i < 10: # display only the first 10 rows
            print(row)
