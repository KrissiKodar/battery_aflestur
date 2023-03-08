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

# turn off warnings
import warnings
warnings.filterwarnings("ignore")


import PySimpleGUI as sg


def print_and_refresh(window, text):
    print(text)
    window.refresh()

# only for newer batteries (BQ3060 does not have the same class names)
def check_template_df(window, current_df, golden_df):
    for index, row in current_df.iterrows():
        # only check "Class" "Protections" and "Permanent Fail" for now
        if row['Class'] == "Protections" or row['Class'] == "Permanent Fail":
            print("\n")
            print("Class: ", row['Class'], "\nSubclass: ", row['Subclass'], "\nName: ", row['Name']
                    , "\nGolden File: ", golden_df['Measured Value'][index], " ", row["Units"] ,"\nCurrent File: ", row['Measured Value'], " ", row["Units"])
            print("\n")
    window.refresh()
if __name__ == "__main__":

    
    frame_layout = [[sg.Multiline("", size=(80, 40), autoscroll=True,
        reroute_stdout=True, reroute_stderr=True, key='-OUTPUT-')]]

    layout = [
        [sg.Frame("Output console", frame_layout)],
        [sg.Push(), sg.Button("Read battery")]
    ]
    window = sg.Window("Read battery gauges", layout, finalize=True)



    BAUD = 250000
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

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Read battery":
            print_and_refresh(window, "Reading battery...")
            try:
                port = list(list_ports.comports())
                if len(port) == 0:
                    print_and_refresh(window, "No USB connection found")
                    continue
                print(port)
                for p in port:
                    print(p.device)
                connect_to = port[0].device
                ser = Serial(connect_to, BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
                print_and_refresh(window, "Connected to: " + connect_to)
                startup = battery_gauge(ser)
                time.sleep(0.1)
                startup.wait_for_connection()
                time.sleep(0.1)
                which_battery = startup.identify_device()
                print_and_refresh(window, "which_battery: " + which_battery)
                # if which battery is empty, then
                if which_battery == "":
                    print_and_refresh(window, "No battery connected")
                    print_and_refresh(window, "Please connect a battery and press 'Read battery' again")
                    ser.close()
                    continue
                time.sleep(0.1)

                ############################# BQ3060 ########################################

                if which_battery == "bq3060":
                    print_and_refresh(window, "bq3060")
                    serial_number = startup.serial_number()
                    time.sleep(0.1)
                    with open('pkl_files\BQ3060_df.pkl', 'rb') as file:
                        # Load the dictionary from the file
                        data_df = pickle.load(file)
                    with open('pkl_files\SBS_BQ3060.pkl', 'rb') as file:
                        # Load the dictionary from the file
                        data_SBS = pickle.load(file)
                    current_battery = BQ3060(ser, data_df, data_SBS)
                    time.sleep(0.1)
                    # load golden file to compare read data to
                    with open('pkl_files\BQ3060_df_golden_file.pkl', 'rb') as file:
                        golden_file = pickle.load(file)
                    
                    
                    current_battery.read_basic_SBS_new()
                    print_and_refresh(window, "Done reading SBS data for BQ3060...")
                    with open('measured_data_pkl_files\BQ3060_'+ serial_number + '_SBS.pkl', 'wb') as file:
                        pickle.dump(current_battery.data_SBS, file)
                    print_and_refresh(window, "Done saving SBS data for BQ3060 (pickle file, pandas dataframe)...")
                    
                    current_battery.data_SBS.to_sql('BQ3060_'+ serial_number + '_SBS', engine, if_exists='replace')
                    print("Done sending SBS data for BQ3060 to server...")

                    time.sleep(0.1)
                    current_battery.read_all_dataflash_3060()
                    print_and_refresh(window, "Done reading dataflash for BQ3060...")
                    # save dataframe to pickle file
                    with open('measured_data_pkl_files\BQ3060_' + serial_number + '_dataflash.pkl', 'wb') as file:	
                        pickle.dump(current_battery.data_df, file)
                    print_and_refresh(window, "Done saving dataflash for BQ3060 (pickle file, pandas dataframe)...")
                    
                    current_battery.data_df.to_sql('BQ3060_' + serial_number + '_dataflash', engine, if_exists='replace')
                    
                    diff_meas_value_current = current_battery.data_df.loc[current_battery.data_df['Measured Value'] != golden_file['Measured Value']]
                    diff_meas_value_golden = golden_file.loc[golden_file['Measured Value'] != current_battery.data_df['Measured Value']]
                    for index, row in diff_meas_value_current.iterrows():
                        # only check "Class" "Protections" and "Permanent Fail" for now
                        if row['CLASS'] == "1st Level Safety" or row['CLASS'] == "2nd Level Safety":
                            print("\n")
                            print("Class: ", row['CLASS'], "\nSubclass: ", row['SUBCLASS'], "\nName: ", row['Name']
                                    , "\nGolden File: ", diff_meas_value_golden['Measured Value'][index], " ", row["UNIT"] ,"\nCurrent File: ", row['Measured Value'], " ", row["Units"])
                            print("\n")
                    window.refresh()

                    print_and_refresh(window, "Done sending dataflash for BQ3060 to server...")
                
                #################################### BQ4050 ###################################3

                # if which_battery contains "1936.1B" anywhere in the string, then
                # on test battery was "1936.1B-6" and another was "1936.1B-3"
                if "1936.1B" in which_battery: 
                    print_and_refresh(window, "BQ4050")
                    serial_number = startup.serial_number()
                    time.sleep(0.1)
                    with open('pkl_files\BQ4050_df.pkl', 'rb') as file:
                        # Load the dictionary from the file
                        data_df = pickle.load(file)
                    with open('pkl_files\SBS_BQ4050.pkl', 'rb') as file:
                        # Load the dictionary from the file
                        data_SBS = pickle.load(file)
                    current_battery= BQ4050(ser, data_df, data_SBS)

                    # load golden file to compare read data to
                    with open('pkl_files\BQ4050_df_golden_file.pkl', 'rb') as file:
                        golden_file = pickle.load(file)


                    time.sleep(0.1)
                    current_battery.read_basic_SBS_new()
                    print_and_refresh(window, "Done reading SBS data for BQ4050...")
                    with open('measured_data_pkl_files\BQ4050_'+ serial_number + '_SBS.pkl', 'wb') as file:
                        pickle.dump(current_battery.data_SBS, file)
                    print_and_refresh(window, "Done saving SBS data for BQ4050 (pickle file, pandas dataframe)...")
                    current_battery.data_SBS.to_sql('BQ4050_'+ serial_number + '_SBS', engine, if_exists='replace')
                    print_and_refresh(window, "Done sending SBS data for BQ4050 to server...")

                    time.sleep(0.1)
                    current_battery.read_all_dataflash_4050()
                    print_and_refresh(window, "Done reading dataflash for BQ4050...")
                    # save dataframe to pickle file
                    with open('measured_data_pkl_files\BQ4050_' + serial_number + '_dataflash.pkl', 'wb') as file:	
                        pickle.dump(current_battery.data_df, file)
                    print_and_refresh(window, "Done saving dataflash for BQ4050 (pickle file, pandas dataframe)...")
                    current_battery.data_df.to_sql('BQ4050_' + serial_number + '_dataflash', engine, if_exists='replace')


                    # for rows where value in "Measured Value" column is not equal to value in "Golden File" column
                    diff_meas_value_current = current_battery.data_df.loc[current_battery.data_df['Measured Value'] != golden_file['Measured Value']]
                    diff_meas_value_golden = golden_file.loc[golden_file['Measured Value'] != current_battery.data_df['Measured Value']]
                    check_template_df(window, diff_meas_value_current, diff_meas_value_golden)



                    print_and_refresh(window, "Done sending dataflash for BQ4050 to server...")
                
                
                ###################################### BQ78350 ########################################################3

                if which_battery == "1737":
                    print_and_refresh(window, "bq78350")
                    serial_number = startup.serial_number()
                    time.sleep(0.1)
                    with open('pkl_files\BQ78350_df.pkl', 'rb') as file:
                        # Load the dictionary from the file
                        data_df = pickle.load(file)
                    with open('pkl_files\SBS_BQ78350.pkl', 'rb') as file:
                        # Load the dictionary from the file
                        data_SBS = pickle.load(file)
                    current_battery = BQ78350(ser, data_df, data_SBS)
                    time.sleep(0.1)
                    with open('pkl_files\BQ78350_df_golden_file.pkl', 'rb') as file:
                        golden_file = pickle.load(file)
                    current_battery.read_basic_SBS_new()
                    print_and_refresh(window, "Done reading SBS data for BQ78350...")
                    with open('measured_data_pkl_files\BQ78350_'+ serial_number + '_SBS.pkl', 'wb') as file:
                        pickle.dump(current_battery.data_SBS, file)
                    print_and_refresh(window, "Done saving SBS data for BQ78350 (pickle file, pandas dataframe)...")
                    current_battery.data_SBS.to_sql('BQ78350_'+ serial_number + '_SBS', engine, if_exists='replace')
                    print_and_refresh(window, "Done sending SBS data for BQ78350 to server...")

                    time.sleep(0.1)
                    current_battery.read_all_dataflash_78350()
                    print_and_refresh(window, "Done reading dataflash for BQ78350...")
                    
                    # save dataframe to pickle file
                    with open('measured_data_pkl_files\BQ78350_' + serial_number + '_dataflash.pkl', 'wb') as file:	
                        pickle.dump(current_battery.data_df, file)
                    print_and_refresh(window, "Done saving dataflash for BQ78350 (pickle file, pandas dataframe)...")
                    current_battery.data_df.to_sql('BQ78350_' + serial_number + '_dataflash', engine, if_exists='replace')
                    print_and_refresh(window, "Done sending dataflash for BQ78350 to server...")
                    print_and_refresh(window, "Comparing read data to template...")
                    
                    # for rows where value in "Measured Value" column is not equal to value in "Golden File" column
                    diff_meas_value_current = current_battery.data_df.loc[current_battery.data_df['Measured Value'] != golden_file['Measured Value']]
                    diff_meas_value_golden = golden_file.loc[golden_file['Measured Value'] != current_battery.data_df['Measured Value']]
                    check_template_df(window, diff_meas_value_current, diff_meas_value_golden)
                    

                    print_and_refresh(window, "Done reading battery, connect another battery and press 'Read battery' again")



                print_and_refresh(window, "Done reading battery, connect another battery and press 'Read battery' again")
                # end serial connection
                ser.close()
            except:
                # print and refresh the exception
                print_and_refresh(window, "Error: " + str(sys.exc_info()[0]))
                print_and_refresh(window, "Error: " + str(sys.exc_info()[1]))
                # go back to main menu
                continue



    window.close()