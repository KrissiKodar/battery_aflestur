import sys
import time
import pickle
import pandas as pd
from serial import Serial
from serial.tools import list_ports
from sqlalchemy import create_engine

from batteries import *
from tkinter_settings import BAUD, engine


def connect_to_serial_port():
    """Connect to the serial port and return the Serial object."""
    port = list(list_ports.comports())
    if len(port) == 0:
        print("No USB connection found")
        return None

    connect_to = port[0].device
    ser = Serial(connect_to, BAUD, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
    print("Connected to:", connect_to)
    return ser

def small_delay():
    """Small delay to allow the battery to respond."""
    time.sleep(0.1)

def identify_battery(ser):
    """Identify the connected battery and return its name."""
    startup = battery_gauge(ser)
    small_delay()
    startup.wait_for_connection()
    small_delay()
    which_battery = startup.identify_device()
    return startup, which_battery


def get_serial_number(startup, ser):
    """Get the battery's serial number."""
    serial_number = startup.serial_number()
    small_delay()
    return serial_number


def create_battery_object(startup, battery_type, ser):
    """Create a battery object based on the battery type."""
    if battery_type == "bq3060":
        small_delay()
        with open('pkl_files\BQ3060_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('pkl_files\SBS_BQ3060.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery = BQ3060(ser, data_df, data_SBS)
        small_delay()
        return current_battery

    if "1936.1B" in battery_type:
        small_delay()
        with open('pkl_files\BQ4050_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('pkl_files\SBS_BQ4050.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery= BQ4050(ser, data_df, data_SBS)
        small_delay()
        return current_battery
    
    if battery_type == "1737":
        small_delay()
        with open('pkl_files\BQ78350_df.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_df = pickle.load(file)
        with open('pkl_files\SBS_BQ78350.pkl', 'rb') as file:
            # Load the dictionary from the file
            data_SBS = pickle.load(file)
        current_battery = BQ78350(ser, data_df, data_SBS)
        small_delay()
        return current_battery

    return None


def process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input):
    """Read, save, and send battery data for a given battery type."""

    small_delay()
    # read basic SBS data
    current_battery.read_basic_SBS_new()
    print(f"Done reading SBS data for {battery_type}...")

    # save the SBS data to a pickle file
    with open(f'measured_data_pkl_files\{battery_type}_{scanned_input}_{serial_number}_SBS.pkl', 'wb') as file:
        pickle.dump(current_battery.data_SBS, file)
    print(f"Done saving SBS data for {battery_type} (pickle file, pandas dataframe)...")

    # send the SBS data to the SQL database
    current_battery.data_SBS.to_sql(f'{battery_type}_{scanned_input}_{serial_number}_SBS', engine, if_exists='replace')
    print(f"Done sending SBS data for {battery_type} to server...")
    small_delay()

    # read the dataflash
    current_battery.read_all_dataflash()
    print(f"Done reading dataflash for {battery_type}...")

    # save the dataflash to a pickle file
    with open(f'measured_data_pkl_files\{battery_type}_{scanned_input}_{serial_number}_dataflash.pkl', 'wb') as file:
        pickle.dump(current_battery.data_df, file)
    print(f"Done saving dataflash for {battery_type} (pickle file, pandas dataframe)...")

    # send the dataflash to the SQL database
    current_battery.data_df.to_sql(f'{battery_type}_{scanned_input}_{serial_number}_dataflash', engine, if_exists='replace')
    print(f"Done sending dataflash for {battery_type} to server...")
    print("Add comparison to golden file later...")


def read_battery_data(current_battery, battery_type, serial_number, scanned_input):
    """Read battery data and save it to pickle files and SQL database."""

    if battery_type == "bq3060":
        battery_type = "BQ3060"
        process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input)

    if "1936.1B" in battery_type:
        battery_type = "BQ4050"
        process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input)

    if battery_type == "1737":
        battery_type = "BQ78350"
        process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input)



def gui_to_read_battery(scanned_input):
    try:
        print(f"The scanned input is: {scanned_input}")
        ser = connect_to_serial_port()
        if not ser:
            return False

        startup, battery_type = identify_battery(ser)
        if not battery_type:
            print("No battery connected")
            print("Please connect a battery and press 'Read battery' again")
            ser.close()
            return False

        serial_number = get_serial_number(startup, ser)

        battery = create_battery_object(startup, battery_type, ser)
        read_battery_data(battery, battery_type, serial_number, scanned_input)

        print("\n\n")
        print("Done reading battery, connect another battery and press 'Read battery' again")
        print("\n\n")
        ser.close()
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False


#if __name__ == "__main__":
#    main()
