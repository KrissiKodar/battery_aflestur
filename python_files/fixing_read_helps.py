import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('BQ78350_df_read_help_changed.csv')

# Convert the ADDRESS column to integers
df['ADDRESS'] = df['ADDRESS'].apply(lambda x: int(x, 16))

# Compute the remainder of the ADDRESS column with respect to 32
df['OFFSET'] = df['ADDRESS'] % 32

# Round down the ADDRESS column to the nearest 32-byte boundary
df['ADDRESS'] = df['ADDRESS'].apply(lambda x: x & ~0x1F)

# Replace the FROM column with the OFFSET column
df['ADDRESS'] = df['ADDRESS'].apply(lambda x: hex(x))

# Drop the TO and CURRENT_ADDRESS columns
df.drop(['TO', 'CURRENT_ADDRESS', 'FROM'], axis=1, inplace=True)


# Swap the locations of columns B and C
df = df.reindex(columns=['CLASS', 'SUBCLASS', 'NAME', 'ADDRESS', 'OFFSET', 'NUM_READS', 'TYPE'])

# Save the modified DataFrame to a new CSV file
df.to_csv('changed_data.csv', index=False)
