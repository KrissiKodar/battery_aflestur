from tabula.io import read_pdf
import pandas as pd
import pickle

file1 = "datasheets/BQ3060_tech_ref.pdf"
#lets read from pages 178 to 185


table = read_pdf(file1, pages="76-77",  multiple_tables=True)#, stream=True)

table_two = read_pdf(file1, pages="90-91",  multiple_tables=True)#, stream=True)

print(len(table))
print(len(table_two))


# change column names of table[3] to be same as column names of table[2]
table[3].columns = table[2].columns

# combine table[2] and table[3] into one table using concat
SBS_3060_upper = pd.concat([table[2], table[3]], ignore_index=True)

# where "UNIT" is "mAh or" change it to "mAh or 10mWh"
SBS_3060_upper.loc[SBS_3060_upper['UNIT'] == 'mAh or', 'UNIT'] = 'mAh or 10mWh'


# combine tables table_two[1] and table_two[2] into one table
SBS_3060_lower = table_two[1].append(table_two[2], ignore_index=True)

# change column names of SBS_3060_lower to be same as column names of SBS_3060_upper
SBS_3060_lower.columns = SBS_3060_upper.columns

# combine SBS_3060_upper and SBS_3060_lower into one table using concat
SBS_3060 = pd.concat([SBS_3060_upper, SBS_3060_lower], ignore_index=True)


# where "SBS CMD" is NaN remove the row
SBS_3060 = SBS_3060.dropna(subset=['SBS CMD'])


# remove all \r, \t and \n from all columns
for column in SBS_3060:
    SBS_3060[column] = SBS_3060[column].str.replace('\r', ' ')
    SBS_3060[column] = SBS_3060[column].str.replace('\t', ' ')
    SBS_3060[column] = SBS_3060[column].str.replace('\n', ' ')

# # in column FORMAT change occurences of "String" to "string"
SBS_3060["FORMAT"] = SBS_3060["FORMAT"].str.replace("String", "string")

# add column "Measured Value" to table[0] beteween "DATA TYPE" and "MIN VALUE" columns
SBS_3060.insert(5, "Measured Value", None)

# capitalize all column names
SBS_3060.columns = SBS_3060.columns.str.upper()

# rename column "SIZE IN" to "SIZE IN BYTES"
SBS_3060.rename(columns={"SIZE IN": "SIZE IN BYTES"}, inplace=True)

# remove all instances of "+1" form column "SIZE IN BYTES"
SBS_3060["SIZE IN BYTES"] = SBS_3060["SIZE IN BYTES"].str.replace("\+1", "")


# for NAME TempRange make Format hex ans Size in Bytes 2
SBS_3060.loc[SBS_3060['NAME'] == 'TempRange', 'FORMAT'] = 'hex'
SBS_3060.loc[SBS_3060['NAME'] == 'TempRange', 'SIZE IN BYTES'] = '2'


# convert FORMAT "signed int" to "integer"
SBS_3060.loc[SBS_3060['FORMAT'] == 'signed int', 'FORMAT'] = 'integer'

print(SBS_3060[-40:])

with open('SBS_BQ3060.pkl', 'wb') as f:
    pickle.dump(SBS_3060, f)

""" for i in SBS_3060.loc[:, "SBS CMD"]:
    # convert i which is string "0x00" to int 0
    i = int(i, 16)
    print(i) """