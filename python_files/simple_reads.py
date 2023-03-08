import serial
from serial.tools import list_ports
from serial import Serial
import sys
import time
import pickle
import pandas as pd
import struct

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pyodbc

from batteries import *

port = list(list_ports.comports())
print(port)
for p in port:
    print(p.device)

BAUD = 250000
# serial port is at /dev/ttyUSB0 (a linux velinni minni)
#ser = Serial('/dev/ttyUSB0', BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
# windows fartolva
ser = Serial('COM6', BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
# bordtolva
#ser = Serial('COM5', BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

####################### SQL ############################
my_uid = "LAPTOP-GG7823IL\dadas"
my_pwd = "testpass"
my_host = "LAPTOP-GG7823IL\SQLEXPRESS"
my_db = "test"
my_odbc_driver = "ODBC Driver 17 for SQL Server"

connection_url = URL.create(
    "mssql+pyodbc",
    username=my_uid,
    #password=my_pwd,
    host=my_host,
    database=my_db,  # required; not an empty string
    query={
        "driver": my_odbc_driver ,
        "Trusted_Connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(connection_url, fast_executemany=True)


# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])



if len(sys.argv) > 1:
    time.sleep(0.1)
    startup = battery_gauge(ser)
    time.sleep(0.1)
    startup.wait_for_connection()
    time.sleep(0.1)
    if sys.argv[1] == "BQ3060":
        with open('pkl_files\BQ3060_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('pkl_files\SBS_BQ3060.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery= BQ3060(ser, data_df, data_SBS)
        time.sleep(0.1)
        if sys.argv[2] == "0":
            current_battery.read_basic_SBS_new()
            print(current_battery.data_SBS[:20])
        elif sys.argv[2] == "1":
            current_battery.read_all_dataflash_3060()
            print(current_battery.data_df[:20])


    if sys.argv[1] == "BQ4050":
        # Open a file in read binary mode
        with open('pkl_files\BQ4050_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('pkl_files\SBS_BQ4050.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery= BQ4050(ser, data_df, data_SBS)
        time.sleep(0.1)
        if sys.argv[2] == "0":
            current_battery.read_basic_SBS_new()
            print(current_battery.data_SBS[:20])
        elif sys.argv[2] == "1": 
            current_battery.read_all_dataflash_4050()
            print(current_battery.data_df[:20])

    
    if sys.argv[1] == "BQ78350":
        with open('pkl_files\BQ78350_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('pkl_files\SBS_BQ78350.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery = BQ78350(ser, data_df, data_SBS)
        if sys.argv[2] == "0":
            current_battery.read_basic_SBS_new()
            print(current_battery.data_SBS[:20])
        if sys.argv[2] == "1":
            current_battery.read_all_dataflash_78350()
            print(current_battery.data_df[:20])
