from tabula.io import read_pdf
import pandas as pd
import pickle

#file1 = "/home/kristjan/Downloads/3060_technical_reference.pdf"
#file1 = "/home/kristjan/Downloads/4050_technical_reference.pdf"

file1 = "datasheets/BQ40z50_r2_tech_ref.pdf"
table =read_pdf(file1, pages="253-270",  multiple_tables=True)# stream=True)


#print(len(table))
#print(table[2])


# combine tables table[2] to table[-1] into one table
for i in range(3,len(table)):
    table[2] = table[2].append(table[i], ignore_index=True)


#remove all instances of '\r', '\t' and '\n' from all columns
for column in table[2]:
    table[2][column] = table[2][column].str.replace('\r', ' ')
    table[2][column] = table[2][column].str.replace('\t', ' ')
    table[2][column] = table[2][column].str.replace('\n', ' ')

#print(table[2][10:40])

# add column "Measured Value" to table[2]
# add it betwween "Type" and "Min Value" columns
table[2].insert(5, "Measured Value", None)



#print row 2 in column Address
#print(type(table[2].loc[2, "Address"]))

# convert Address where the numbers are strings "0x0000" to 32 bit integers
table[2]["Address"] = table[2]["Address"].apply(lambda x: int(x, 16))

print(table[2].head(10))


# save table[2] to pickle file
""" with open('BQ4050_df.pkl', 'wb') as file:
    # Dump the dictionary to the fileq
    pickle.dump(table[2], file) """