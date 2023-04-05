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
        if row["CLASS"] == "Protections" or row["CLASS"] == "Permanent Fail":
            print("\n")
            print("Class: ", row["CLASS"], "\nSubclass: ", row["SUBCLASS"], "\nName: ", row["NAME"]
                    , "\nGolden File: ", golden_df["MEASURED VALUE"][index], " ", row["UNIT"] ,"\nCurrent File: ", row["MEASURED VALUE"], " ", row["UNIT"])
            print("\n")
    window.refresh()
if __name__ == "__main__":

    # serial baud rate
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





    sg.theme('SystemDefault')
    
    frame_layout = [[sg.Multiline("", size=(120, 30), autoscroll=True,
        reroute_stdout=True, reroute_stderr=True, font = "consolas 8", key='-OUTPUT-')]]
    
    
    # ----------- Create the 3 layouts this Window will display -----------
    # beginning layout
    layout1 = [ [sg.Push(), sg.Button("Incoming"), sg.Button("Service")]]


    # incoming layout
    layout2 = [ [sg.Push(), sg.Button("Read battery")]]
    
    # service layout
    layout3 = [ [sg.Push(), sg.Button("Show new SBS reading"), sg.Button("Show new dataflash reading") ,sg.Button("Read battery")]]

    # ----------- Create actual layout using Columns and a row of Buttons
    layout = [[sg.Frame("Output console", frame_layout)],
            [sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
            [sg.Checkbox('Check golden file?', default=True, key='check_golden_file')],
            [sg.Text('Scan product', size =(15, 1)), sg.InputText(key = 'scan_product')],
            [sg.Button("Back"), sg.Button("Scan new battery"), sg.Button('Exit')]]



    window = sg.Window("Read battery gauges", layout)

    
    battery_read_check = False

    #currently visible layout
    layout = 1 
    while True:
        event, values = window.read()
        print(event)
        #print(values)
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        elif event == "Back":
            window[f'-COL{layout}-'].update(visible=False)
            layout = 1
            window[f'-COL{layout}-'].update(visible=True)

        elif event == "Incoming":
            window[f'-COL{layout}-'].update(visible=False)
            layout = 2
            window[f'-COL{layout}-'].update(visible=True)

        elif event == "Service":

            print("Currently scanned battery: ", values['scan_product'])

            window[f'-COL{layout}-'].update(visible=False)
            layout = 3
            window[f'-COL{layout}-'].update(visible=True)

        elif "Read battery" in event:
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

                # let program know that a battery has been read
                battery_read_check = True

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
                    # check if radio button 'Check golden file?' is checked
                    # the columns are named differently for this battery compared to the other two (BQ4050 and BQ7850)
                    if values['check_golden_file']:
                        diff_meas_value_current = current_battery.data_df.loc[current_battery.data_df["MEASURED VALUE"] != golden_file["MEASURED VALUE"]]
                        diff_meas_value_golden = golden_file.loc[golden_file["MEASURED VALUE"] != current_battery.data_df["MEASURED VALUE"]]
                        for index, row in diff_meas_value_current.iterrows():
                            # only check "Class" "Protections" and "Permanent Fail" for now
                            if row['CLASS'] == "1st Level Safety" or row['CLASS'] == "2nd Level Safety":
                                print("\n")
                                print("Class: ", row['CLASS'], "\nSubclass: ", row['SUBCLASS'], "\nName: ", row["NAME"]
                                        , "\nGolden File: ", diff_meas_value_golden["MEASURED VALUE"][index], " ", row["UNIT"] ,"\nCurrent File: ", row["MEASURED VALUE"], " ", row["UNIT"])
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

                    if values['check_golden_file']:
                        # for rows where value in "Measured Value" column is not equal to value in "Golden File" column
                        diff_meas_value_current = current_battery.data_df.loc[current_battery.data_df["MEASURED VALUE"] != golden_file["MEASURED VALUE"]]
                        diff_meas_value_golden = golden_file.loc[golden_file["MEASURED VALUE"] != current_battery.data_df["MEASURED VALUE"]]
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
                    
                    if values['check_golden_file']:
                        # for rows where value in "Measured Value" column is not equal to value in "Golden File" column
                        print_and_refresh(window, "Comparing read data to template...")
                        diff_meas_value_current = current_battery.data_df.loc[current_battery.data_df["MEASURED VALUE"] != golden_file["MEASURED VALUE"]]
                        diff_meas_value_golden = golden_file.loc[golden_file["MEASURED VALUE"] != current_battery.data_df["MEASURED VALUE"]]
                        check_template_df(window, diff_meas_value_current, diff_meas_value_golden)
                

                print("\n\n")
                print("Done reading battery, connect another battery and press 'Read battery' again")
                print("\n\n")
                window.refresh()
                # end serial connection
                ser.close()
            except:
                # print and refresh the exception
                print_and_refresh(window, "Error: " + str(sys.exc_info()[0]))
                print_and_refresh(window, "Error: " + str(sys.exc_info()[1]))
                # go back to main menu
                continue
    

        elif event == "Show new SBS reading":
            if battery_read_check:
                print("\n\n\n")
                display_SBS = (current_battery.data_SBS[['SBS CMD', "NAME", "MEASURED VALUE", 'UNIT']])
                max = 35
                for index, row in display_SBS.iterrows():
                    print(row['SBS CMD'])
                    print(row["NAME"])
                    print(row["MEASURED VALUE"], row['UNIT'])
                    print("\n")
            print("\n\n")
            print("Done reading battery, connect another battery and press 'Read battery' again")
            print("\n\n")
            window.refresh()
        
        elif event == "Show new dataflash reading":
            if battery_read_check:
                print("\n\n\n")
                # display_df is current_battery.data_df but with all columns capitalized
                display_df = current_battery.data_df
                # get columns, CLASS, SUBCLASS, NAME and MEASURED VALUE
                display_df.columns = map(str.upper, display_df.columns)
                # if one column is named UNITS rename it to UNIT
                if 'UNITS' in display_df.columns:
                    display_df = display_df.rename(columns={'UNITS': 'UNIT'})
                display_df = display_df[['CLASS', 'SUBCLASS', "NAME", "MEASURED VALUE", 'UNIT']]
                max = 35
                for index, row in display_df.iterrows():
                    print(row['CLASS']," - ", row['SUBCLASS']," - ",  row["NAME"], (max - len(row["NAME"]))*" ", row["MEASURED VALUE"], row['UNIT'])
            print("\n\n")
            print("Done reading battery, connect another battery and press 'Read battery' again")
            print("\n\n")
            window.refresh()

        elif event == "Scan new battery":
            # clear scan_prduct text box
            window['scan_product'].update("")
            window.refresh()


    window.close()