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


print("length of SBS_78350: ", len(SBS_78350))




# remove rows from SBS_78350 where "SBS Cmd" is 0x2B, 0x2C, 0x2D, 0x2E
rm = ["0x2B", "0x2C", "0x2D", "0x2E"]
SBS_78350 = SBS_78350[~SBS_78350["SBS Cmd"].isin(rm)]

# also remove rows where "SBS Cmd" is 0x30 to 0x3B
rm = ["0x30", "0x31", "0x32", "0x33", "0x34", "0x35", "0x36", "0x37", "0x38", "0x39", "0x3A", "0x3B"]
SBS_78350 = SBS_78350[~SBS_78350["SBS Cmd"].isin(rm)]

rm = ["0x4C","0x4D","0x4E"]
SBS_78350 = SBS_78350[~SBS_78350["SBS Cmd"].isin(rm)]

rm = ["0x58", "0x59", "0x5A", "0x5B"]
SBS_78350 = SBS_78350[~SBS_78350["SBS Cmd"].isin(rm)]

rm = ["0x65", "0x66", "0x80", "0x81"]
SBS_78350 = SBS_78350[~SBS_78350["SBS Cmd"].isin(rm)]



# add the following rows to SBS_78350
add_this = {"BTPDischargeSet":  "0x4A",
"BTPChargeset":     "0x4B", 
"AFE Register":     "0x58",
"MaxTurboPwr":      "0x59",
"SusTurboPwr":      "0x5A",
"TURBO_PACK_R":     "0x5B",
"TURBO_SYS_R":      "0x5C",
"TURBO_EDV":        "0x5D",
"MaxTurboCurr":     "0x5E",
"SusTurboCurr":     "0x5F",
"GaugeStatus1":     "0x73",
"GaugeStatus2":     "0x74",
"GaugeStatus3":     "0x75",
"CBStatus":         "0x76",
"State-of-Health":  "0x77",
"FilteredCapacity": "0x78"}

# add from add_this to SBS_78350
# the items in add_this are "SBS Cmd" and the keys are "Name"
for key, value in add_this.items():
    SBS_78350 = SBS_78350.append({"Name": key, "SBS Cmd": value}, ignore_index=True)

# sort rows by "SBS Cmd", "SBS Cmd" are strings that represent hex numbers
SBS_78350 = SBS_78350.sort_values(by=["SBS Cmd"])

# in column format change occurences of "String" to "string"
SBS_78350["Format"] = SBS_78350["Format"].str.replace("String", "string")

# where "Name" is BTPDischargeSet: change "Mode" to "R/W", "Format" to "integer", "Size in Bytes" to "2", "Min" to "—", "Max" to "65535", "Default" to 150, "Unit" to "mAh"
SBS_78350.loc[SBS_78350["Name"] == "BTPDischargeSet", "Mode"] = "R/W"
SBS_78350.loc[SBS_78350["Name"] == "BTPDischargeSet", "Format"] = "integer"
SBS_78350.loc[SBS_78350["Name"] == "BTPDischargeSet", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "BTPDischargeSet", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "BTPDischargeSet", "Max"] = "65535"
SBS_78350.loc[SBS_78350["Name"] == "BTPDischargeSet", "Default"] = "150"
SBS_78350.loc[SBS_78350["Name"] == "BTPDischargeSet", "Unit"] = "mAh"

# where "Name" is BTPChargeset: change "Format" to "integer", "Size in Bytes" to "2", "Min" to "—", "Max" to "65535", "Default" to 175, "Unit" to "mAh"
SBS_78350.loc[SBS_78350["Name"] == "BTPChargeset", "Mode"] = "R/W"
SBS_78350.loc[SBS_78350["Name"] == "BTPChargeset", "Format"] = "integer"
SBS_78350.loc[SBS_78350["Name"] == "BTPChargeset", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "BTPChargeset", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "BTPChargeset", "Max"] = "65535"
SBS_78350.loc[SBS_78350["Name"] == "BTPChargeset", "Default"] = "175"
SBS_78350.loc[SBS_78350["Name"] == "BTPChargeset", "Unit"] = "mAh"

# where "Name" is "AFE REgister" change "Mode" to "R", "Format" to "string", "Size in Bytes" to "?", "Min" to "—", "Max" to "—", "Default" to "—", "Unit" to "—"
SBS_78350.loc[SBS_78350["Name"] == "AFE Register", "Mode"] = "R"
SBS_78350.loc[SBS_78350["Name"] == "AFE Register", "Format"] = "string"
SBS_78350.loc[SBS_78350["Name"] == "AFE Register", "Size in Bytes"] = "?"
SBS_78350.loc[SBS_78350["Name"] == "AFE Register", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "AFE Register", "Max"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "AFE Register", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "AFE Register", "Unit"] = "—"

# for both MaxTurboPwr and SusTurboPwr change "Mode" to "R/W", "Format" to "unsigned int", "Size in Bytes" to "2", "Min" to "—", "Max" to "65535", "Default" to "—", "Unit" to "cW"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboPwr", "Mode"] = "R"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboPwr", "Format"] = "unsigned int"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboPwr", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboPwr", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboPwr", "Max"] = "65535"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboPwr", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboPwr", "Unit"] = "cW"

SBS_78350.loc[SBS_78350["Name"] == "SusTurboPwr", "Mode"] = "R"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboPwr", "Format"] = "unsigned int"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboPwr", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboPwr", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboPwr", "Max"] = "65535"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboPwr", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboPwr", "Unit"] = "cW"

# for both TURBO_PACK_R and TURBO_SYS_R change "Mode" to "R/W", "Format" to "unsigned int", "Size in Bytes" to "2", "Min" to "—", "Max" to "65535", "Default" to "—", "Unit" to "mOhm"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_PACK_R", "Mode"] = "R/W"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_PACK_R", "Format"] = "unsigned int"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_PACK_R", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_PACK_R", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_PACK_R", "Max"] = "65535"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_PACK_R", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_PACK_R", "Unit"] = "mOhm"

SBS_78350.loc[SBS_78350["Name"] == "TURBO_SYS_R", "Mode"] = "R/W"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_SYS_R", "Format"] = "unsigned int"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_SYS_R", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_SYS_R", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_SYS_R", "Max"] = "65535"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_SYS_R", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_SYS_R", "Unit"] = "mOhm"

# for TURBO_EDV change "Mode" to "R/W", "Format" to "unsigned int", "Size in Bytes" to "2", "Min" to "—", "Max" to "65535", "Default" to "—", "Unit" to "mV"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_EDV", "Mode"] = "R/W"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_EDV", "Format"] = "unsigned int"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_EDV", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_EDV", "Min"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_EDV", "Max"] = "65535"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_EDV", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "TURBO_EDV", "Unit"] = "mV"

# for MaxTurboCurr change "Mode" to "R/W", "Format" to "integer", "Size in Bytes" to "2", "Min" to "-32786", "Max" to "32767", "Default" to "—", "Unit" to "mA"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboCurr", "Mode"] = "R/W"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboCurr", "Format"] = "integer"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboCurr", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboCurr", "Min"] = "-32786"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboCurr", "Max"] = "32767"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboCurr", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "MaxTurboCurr", "Unit"] = "mA"

# for SusTurboCurr change "Mode" to "R/W", "Format" to "integer", "Size in Bytes" to "2", "Min" to "-32786", "Max" to "32767", "Default" to "—", "Unit" to "mA"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboCurr", "Mode"] = "R/W"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboCurr", "Format"] = "integer"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboCurr", "Size in Bytes"] = "2"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboCurr", "Min"] = "-32786"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboCurr", "Max"] = "32767"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboCurr", "Default"] = "—"
SBS_78350.loc[SBS_78350["Name"] == "SusTurboCurr", "Unit"] = "mA"

# Dont sort indices, but change their values to be in order
SBS_78350.index = range(len(SBS_78350))

# for all rows beneath row where "Name" is DAStatus 2, change "Mode" to "R", "Format" to "string", "Size in Bytes" to "32+1", "Min" to "—", "Max" to "—", "Default" to "—", "Unit" to "—"
for i in range(SBS_78350.index[SBS_78350["Name"] == "DAStatus 2"][0], len(SBS_78350)):
    SBS_78350.loc[i, "Mode"] = "R"
    SBS_78350.loc[i, "Format"] = "string"
    SBS_78350.loc[i, "Size in Bytes"] = "32+1"
    SBS_78350.loc[i, "Min"] = "—"
    SBS_78350.loc[i, "Max"] = "—"
    SBS_78350.loc[i, "Default"] = "—"
    SBS_78350.loc[i, "Unit"] = "—"

# change "Size in Bytes" for "Name" = "PFAlert" to 4+1
SBS_78350.loc[SBS_78350["Name"] == "PFAlert", "Size in Bytes"] = "4+1"
# change "Size in Bytes" for "Name" = "ChargingStatus" to 4+1
SBS_78350.loc[SBS_78350["Name"] == "ChargingStatus", "Size in Bytes"] = "4+1"
# change "Size in Bytes" for "Name" = "GaugingStatus" to 4+1
SBS_78350.loc[SBS_78350["Name"] == "GaugingStatus", "Size in Bytes"] = "4+1"
# change "Size in Bytes" for "Name" = "ManufacturingStatus" to 4+1
SBS_78350.loc[SBS_78350["Name"] == "ManufacturingStatus", "Size in Bytes"] = "4+1"

# for indices 57 and below change "Size in Bytes" to "—" and "Default" to "—" and "Unit" to "—"

for i in range(57, len(SBS_78350)):
    SBS_78350.loc[i, "Size in Bytes"] = "—"
    SBS_78350.loc[i, "Default"] = "—"
    SBS_78350.loc[i, "Unit"] = "—"


# add column "Measured Value" to table[0] beteween "DATA TYPE" and "MIN VALUE" columns
SBS_78350.insert(5, "Measured Value", None)



# capitalize all column names
SBS_78350.columns = SBS_78350.columns.str.upper()

# remove all instances of "+1" form column "SIZE IN BYTES"
SBS_78350["SIZE IN BYTES"] = SBS_78350["SIZE IN BYTES"].str.replace("\+1", "")

print("length of SBS_78350: ", len(SBS_78350))


# occurances of "?" in SIZE IN BYTES column to 4
SBS_78350.loc[SBS_78350["SIZE IN BYTES"] == "?", "SIZE IN BYTES"] = "4"


# change occurances of "—" in SIZE IN BYTES column to 32
SBS_78350.loc[SBS_78350["SIZE IN BYTES"] == "—", "SIZE IN BYTES"] = "32"


# in row DeviceName change "DEFAULT" to bq40z50-R2
SBS_78350.loc[SBS_78350["NAME"] == "DeviceName", "DEFAULT"] = "bq40z50-R2"

print(SBS_78350[-30:])

SBS_4050 = SBS_78350

# print row where column "NAME" is "Authenticate"
print(SBS_4050.loc[SBS_4050["NAME"] == "Authenticate"])

# save pickle
with open('SBS_BQ4050.pkl', 'wb') as f:
    pickle.dump(SBS_4050, f)
