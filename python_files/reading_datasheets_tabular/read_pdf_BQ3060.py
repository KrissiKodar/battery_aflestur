from tabula.io import read_pdf
import pandas as pd
import pickle

file1 = "datasheets/BQ3060_tech_ref.pdf"
#lets read from pages 178 to 185
table =read_pdf(file1, pages="178-185",  multiple_tables=False)#, stream=True)


#print(table[0][10:40])
# remove from table all rows where the SUBCLASS column is SUBCLASS
table[0] = table[0].loc[table[0]['SUBCLASS'] != 'SUBCLASS']


#remove all instances of '\r', '\t' and '\n' from all columns
for column in table[0]:
    table[0][column] = table[0][column].str.replace('\r', ' ')
    table[0][column] = table[0][column].str.replace('\t', ' ')
    table[0][column] = table[0][column].str.replace('\n', ' ')


#remove all instances of '\r', '\t' and '\n' in column names
table[0].columns = table[0].columns.str.replace('\r', ' ')

# add column "Measured Value" to table[0] beteween "DATA TYPE" and "MIN VALUE" columns
table[0].insert(6, "Measured Value", None)

print(table[0][230:])




""" # save table[0] to pickle file
with open('BQ3060_df.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(table[0], file) """