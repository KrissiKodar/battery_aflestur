from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd
import pickle

# SQL settings
my_uid = "LAPTOP-GG7823IL\dadas"
my_pwd = "testpass"
my_host = "LAPTOP-GG7823IL\SQLEXPRESS"
my_db = "battery_test_6"
my_odbc_driver = "ODBC Driver 17 for SQL Server"

connection_url = URL.create(
    "mssql+pyodbc",
    username=my_uid,
    #password=my_pwd,
    host=my_host,
    database=my_db,  # required; not an empty string
    query={
        "driver": my_odbc_driver,
        "Trusted_Connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(connection_url, fast_executemany=True)
#connection = engine.raw_connection()
connection = engine.connect()
print(f'engine: {engine}')
print(f'connection: {connection}')


battery_data_id = '19'
battery_type = 'BQ4050'

# Check if PASS_Dataflash or PASS_SBS is 0 (False)
check_pass_query = text(f"""
SELECT PASS_SBS, PASS_Dataflash
FROM BatteryData
WHERE PkID_BatteryData = {battery_data_id}
""")

result = connection.execute(check_pass_query).fetchone()
pass_sbs, pass_dataflash = result[0], result[1]

if pass_sbs == 0 or pass_dataflash == 0:
    # Get BatteryDataLine_Dataflash rows with PASS not 'NA'
    dataflash_checks_query = text(f"""
        SELECT *
        FROM BatteryDataLine_Dataflash
        WHERE FkID_BatteryData = {battery_data_id}
        AND PASS <> 'NA'
    """)

    dataflash_checks_df = pd.read_sql_query(dataflash_checks_query, connection)

    # Get BatteryDataLine_SBS rows with PASS not 'NA'
    sbs_checks_query = text(f"""
        SELECT *
        FROM BatteryDataLine_SBS
        WHERE FkID_BatteryData = {battery_data_id}
        AND PASS <> 'NA'
    """)

    sbs_checks_df = pd.read_sql_query(sbs_checks_query, connection)

    # Fetch GoldenFile_Dataflash_test rows
    dataflash_golden_file_query = text(f"""
        SELECT *
        FROM GoldenFile_{battery_type}_Dataflash_test
    """)

    dataflash_golden_file_df = pd.read_sql_query(dataflash_golden_file_query, connection)
    # Fetch GoldenFile_SBS_test rows
    sbs_golden_file_query = text(f"""
        SELECT *
        FROM GoldenFile_{battery_type}_SBS_test
    """)

    sbs_golden_file_df = pd.read_sql_query(sbs_golden_file_query, connection)
    # get the rows in dataflash_golden_file_df where PASS in dataflash_checks_df is "False"
    # So where the rows are False in dataflash_checks_df, use the "CLASS", "SUBCLASS" and "NAME" columns to get the corresponding rows in dataflash_golden_file_df
    for index, row in dataflash_checks_df.iterrows():
        if row['PASS'] == 'False':
            golden_row = dataflash_golden_file_df.loc[(dataflash_golden_file_df['CLASS'] == row["CLASS"]) & (dataflash_golden_file_df['SUBCLASS'] == row["SUBCLASS"]) & (dataflash_golden_file_df['NAME'] == row["NAME"])]
            # print value where columns is "ExactValue"
            ExactValue = golden_row["ExactValue"].values[0]
            MinBoundary = golden_row["MinBoundary"].values[0]
            MaxBoundary = golden_row["MaxBoundary"].values[0]
            checktype = golden_row["CheckType"].values[0]
            print(f"Checktype is {checktype}")
            unit = golden_row["UNIT"].values[0]
            if checktype == "BOUNDARY":
                print(f"\nFAILED TEST FOR: {row['CLASS']}, {row['SUBCLASS']}, {row['NAME']} in Dataflash")
                print(f"Min boundary is {MinBoundary} {unit} and max boundary is {MaxBoundary} {unit}")
                print(f"But the measured value is {row['MEASURED_VALUE']} {unit}\n")
            else:
                print(f"\nFAILED TEST FOR: {row['CLASS']}, {row['SUBCLASS']}, {row['NAME']} in Dataflash")
                print(f"Exact value is {ExactValue} {unit}\n")
                print(f"But the measured value is {row['MEASURED_VALUE']} {unit}\n")

    for index, row in sbs_checks_df.iterrows():
        if row['PASS'] == 'False':
            golden_row = sbs_golden_file_df.loc[(sbs_golden_file_df['NAME'] == row["NAME"])]
            ExactValue = golden_row["ExactValue"].values[0]
            MinBoundary = golden_row["MinBoundary"].values[0]
            MaxBoundary = golden_row["MaxBoundary"].values[0]
            checktype = golden_row["CheckType"].values[0]
            unit = golden_row["UNIT"].values[0]
            if checktype == "BOUNDARY":
                print(f"\nFAILED TEST FOR: {row['NAME']} in SBS")
                print(f"Min boundary is {MinBoundary} {unit} and max boundary is {MaxBoundary} {unit}")
                print(f"But the measured value is {row['MEASURED_VALUE']} {unit}\n")
            else:
                print(f"\nFAILED TEST FOR: {row['NAME']} in SBS")
                print(f"Exact value is {ExactValue} {unit}\n")
                print(f"But the measured value is {row['MEASURED_VALUE']} {unit}\n")
            
print(f'Battery ID: {battery_data_id}')

print("Golden file checks complete.")




connection.close()