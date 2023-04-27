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
my_db = "battery_test_5"
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


battery_data_id = '1'
battery_type = 'BQ4050'

update_dataflash_pass_query = text(f'''
    UPDATE BatteryDataLine_Dataflash
    SET PASS = 
        CASE
            WHEN EXISTS (
                SELECT 1 FROM GoldenFile_{battery_type}_Dataflash_test
                WHERE BatteryDataLine_Dataflash.CLASS = GoldenFile_{battery_type}_Dataflash_test.CLASS 
                AND BatteryDataLine_Dataflash.SUBCLASS = GoldenFile_{battery_type}_Dataflash_test.SUBCLASS 
                AND BatteryDataLine_Dataflash.NAME = GoldenFile_{battery_type}_Dataflash_test.NAME 
                AND BatteryDataLine_Dataflash.TYPE = GoldenFile_{battery_type}_Dataflash_test.TYPE 
                AND BatteryDataLine_Dataflash.MEASURED_VALUE = GoldenFile_{battery_type}_Dataflash_test.Optimal_value 
            ) THEN 'True'
            WHEN EXISTS (
                SELECT 1 FROM GoldenFile_{battery_type}_Dataflash_test
                WHERE BatteryDataLine_Dataflash.CLASS = GoldenFile_{battery_type}_Dataflash_test.CLASS 
                AND BatteryDataLine_Dataflash.SUBCLASS = GoldenFile_{battery_type}_Dataflash_test.SUBCLASS 
                AND BatteryDataLine_Dataflash.NAME = GoldenFile_{battery_type}_Dataflash_test.NAME 
                AND BatteryDataLine_Dataflash.TYPE = GoldenFile_{battery_type}_Dataflash_test.TYPE 
            ) THEN 'False'
            ELSE 'NA'
        END
    WHERE BatteryDataLine_Dataflash.FkID_BatteryData_Dataflash = {battery_data_id}
''')


update_sbs_pass_query = text(f'''
UPDATE BatteryDataLine_SBS
SET PASS = 
    CASE
        WHEN EXISTS (
            SELECT 1 FROM GoldenFile_{battery_type}_SBS_test
            WHERE BatteryDataLine_SBS.NAME = GoldenFile_{battery_type}_SBS_test.NAME 
            AND BatteryDataLine_SBS.MEASURED_VALUE = GoldenFile_{battery_type}_SBS_test.Optimal_value 
        ) THEN 'True'
        WHEN EXISTS (
            SELECT 1 FROM GoldenFile_{battery_type}_SBS_test
            WHERE BatteryDataLine_SBS.NAME = GoldenFile_{battery_type}_SBS_test.NAME 
        ) THEN 'False'
        ELSE 'NA'
    END
WHERE BatteryDataLine_SBS.FkID_BatteryData_SBS = {battery_data_id}
''')
update_battery_data_pass_query = text(f'''
UPDATE BatteryData
SET PASS_SBS = (SELECT CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END
                FROM BatteryDataLine_SBS
                WHERE FkID_BatteryData_SBS = {battery_data_id} AND PASS = 'False'),
    PASS_Dataflash = (SELECT CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END
                        FROM BatteryDataLine_Dataflash
                        WHERE FkID_BatteryData_Dataflash = {battery_data_id} AND PASS = 'False')
WHERE PkID_BatteryData = {battery_data_id}
''')

result = connection.execute(update_dataflash_pass_query)
print(f"Dataflash affected rows: {result.rowcount}")

result = connection.execute(update_sbs_pass_query)
print(f"SBS affected rows: {result.rowcount}")

result = connection.execute(update_battery_data_pass_query)
print(f"BatteryData affected rows: {result.rowcount}")
connection.commit()

print(f'Battery ID: {battery_data_id}')

print("Golden file checks complete.")




connection.close()