from tabula.io import read_pdf
import pandas as pd
import pickle

#file1 = "/home/kristjan/Downloads/3060_technical_reference.pdf"
#file1 = "/home/kristjan/Downloads/4050_technical_reference.pdf"



file1 = "datasheets/BQ78350_r1_ref.pdf"
table =read_pdf(file1, pages="96-97",  multiple_tables=True)


# combine tables table[1] and table[2] into one table using concat
SBS_78350 = pd.concat([table[1], table[2]], ignore_index=True)

# remove all \r, \t and \n from all columns
for column in SBS_78350:
    SBS_78350[column] = SBS_78350[column].str.replace('\r', ' ')
    SBS_78350[column] = SBS_78350[column].str.replace('\t', ' ')
    SBS_78350[column] = SBS_78350[column].str.replace('\n', ' ')

# remove all instances of '\r', '\t' and '\n' in column names
SBS_78350.columns = SBS_78350.columns.str.replace('\r', ' ')
SBS_78350.columns = SBS_78350.columns.str.replace('\t', ' ')
SBS_78350.columns = SBS_78350.columns.str.replace('\n', ' ')

# remove all instances of "+" in columns Min and Max
SBS_78350["Min"] = SBS_78350["Min"].str.replace('+', '')
SBS_78350["Max"] = SBS_78350["Max"].str.replace('+', '')

# Where column "Min" is "0%" and column "Max" is "100%" replace "0%" with "0" and "100%" with "100"
# then write "%" to column "Units" in the same row
SBS_78350.loc[(SBS_78350["Min"] == "0%") & (SBS_78350["Max"] == "100%"), "Units"] = "%"
SBS_78350.loc[(SBS_78350["Min"] == "0%"), "Min"] = "0"
SBS_78350.loc[(SBS_78350["Max"] == "100%"), "Max"] = "100"

# combine "Units" into "Unit", that is if "Units" is not NaN then write "Units" to "Unit"
SBS_78350["Unit"] = SBS_78350["Unit"].fillna(SBS_78350["Units"])
# remove column "Units"
SBS_78350 = SBS_78350.drop(columns=["Units"])

# Where "Name" is "BatteryStatus" change the "Format" to "hex"
SBS_78350.loc[SBS_78350["Name"] == "BatteryStatus", "Format"] = "hex"

# in column format change occurences of "String" to "string"
SBS_78350["Format"] = SBS_78350["Format"].str.replace("String", "string")


# add column "Measured Value" to table[0] beteween "DATA TYPE" and "MIN VALUE" columns
SBS_78350.insert(5, "Measured Value", None)

# capitalize all column names
SBS_78350.columns = SBS_78350.columns.str.upper()

# remove all instances of "+1" form column "SIZE IN BYTES"
SBS_78350["SIZE IN BYTES"] = SBS_78350["SIZE IN BYTES"].str.replace("\+1", "")


print("length of SBS_78350: ", len(SBS_78350))

#print row where column "SBS CMD" is "0x2F"
print(SBS_78350.loc[SBS_78350["SBS CMD"] == "0x2F"])
# print print next 10 rows after row where column "SBS CMD" is "0x2F"
print(SBS_78350.loc[SBS_78350["SBS CMD"] == "0x2F"].iloc[0:10])
# save pickle

# remove row where "NAME" is "Reserved"
SBS_78350 = SBS_78350[SBS_78350.NAME != "Reserved"]
print(SBS_78350[45:65])
""" with open('SBS_BQ78350.pkl', 'wb') as f:
    pickle.dump(SBS_78350, f) """
