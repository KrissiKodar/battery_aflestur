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
my_db = "battery_test_2"
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
with open('pkl_files\BQ4050_df_golden_file.pkl', 'rb') as file:
    # Dump the dictionary to the file
    data_df = pickle.load(file)

with open('pkl_files\SBS_BQ4050.pkl', 'rb') as file:
    # Dump the dictionary to the file
    data_SBS = pickle.load(file)

serial_number = "1234567890"
battery_type = "BQ4050"
# Insert the general battery information into the BatteryData table
# Insert the general battery information into the BatteryData table
battery_data = pd.DataFrame({
    "SerialNumber": [serial_number],
    "BatteryType": [battery_type],
})
battery_data.to_sql("BatteryData", engine, if_exists="append", index=False)



query = text('SELECT * FROM BatteryData')
result = connection.execute(query)

for row in result.fetchall():
    print(row)

query = text('SELECT max(PkID_BatteryData) FROM BatteryData')
result = connection.execute(query)
print("\n")
print(int(result.fetchone()[0]))

connection.close()