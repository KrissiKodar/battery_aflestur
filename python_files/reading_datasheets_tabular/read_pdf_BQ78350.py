from tabula.io import read_pdf
import pandas as pd
import pickle

#file1 = "/home/kristjan/Downloads/3060_technical_reference.pdf"
#file1 = "/home/kristjan/Downloads/4050_technical_reference.pdf"



file1 = "datasheets/BQ78350_r1_ref.pdf"
table =read_pdf(file1, pages="145-157",  multiple_tables=True)



#print(type(table[0]))
#print(len(table))
#print(table[1])
#print(table[0])
#print(table[1])
# combine tables table[0] to table[-1] into one table
for i in range(2,len(table)):
    table[1] = table[1].append(table[i], ignore_index=True)

#print(table[1])

bq78350_df_table = table[1]

#remove all instances of '\r', '\t' and '\n' from all columns
for column in table[1]:
    bq78350_df_table[column] = bq78350_df_table[column].str.replace('\r', ' ')
    bq78350_df_table[column] = bq78350_df_table[column].str.replace('\t', ' ')
    bq78350_df_table[column] = bq78350_df_table[column].str.replace('\n', ' ')

#print(bq78350_df_table)


# add column "Measured Value" to bq78350_df_table and fill it with None
# between columns "Type" and "Min Value"
bq78350_df_table.insert(5, "Measured Value", None)

# convert Address where the numbers are strings "0x0000" to 32 bit integers
bq78350_df_table["Address"] = bq78350_df_table["Address"].apply(lambda x: int(x, 16))


#################### template part ####################

""" # add column check value to bq78350_df_table and fill it with False
bq78350_df_table.insert(6, "Check Value", False)
# add column Min Check Value to bq78350_df_table and fill it with None
bq78350_df_table.insert(7, "Min Check Value", None)
# add column Max Check Value to bq78350_df_table and fill it with None
bq78350_df_table.insert(8, "Max Check Value", None)

# where Subclass is "SOT" and Name is "Threshold" set "Check Value" to True and set Max Check Value to 500
bq78350_df_table.loc[(bq78350_df_table["Subclass"] == "SOT") & (bq78350_df_table["Name"] == "Threshold"), "Check Value"] = True
bq78350_df_table.loc[(bq78350_df_table["Subclass"] == "SOT") & (bq78350_df_table["Name"] == "Threshold"), "Max Check Value"] = 500
bq78350_df_table.loc[(bq78350_df_table["Subclass"] == "SOT") & (bq78350_df_table["Name"] == "Threshold"), "Min Check Value"] = 0 """

########################################################



# make all column names upper case
bq78350_df_table.columns = bq78350_df_table.columns.str.upper()

# convert column UNITS to UNIT
bq78350_df_table.rename(columns={'UNITS': 'UNIT'}, inplace=True)

print(bq78350_df_table.head(10))



with open('..\pkl_files\BQ78350_df.pkl', 'wb') as file:
    # Dump the dictionary to the file
    pickle.dump(bq78350_df_table, file)