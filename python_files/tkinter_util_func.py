import sys
import time
import pickle
import pandas as pd
from serial import Serial
from serial.tools import list_ports
from sqlalchemy import create_engine
from sqlalchemy import text

from batteries import *
from tkinter_settings import BAUD, engine, connection


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
    if "bq3060" in battery_type:
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
    
    elif "1737" in battery_type or "1636" in battery_type:
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



def golden_file_checks(battery_type, battery_data_id):
    update_dataflash_pass_query = text(f'''
        UPDATE BatteryDataLine_Dataflash
        SET PASS = 
            CASE
                WHEN EXISTS (
                    SELECT 1 FROM GoldenFile_{battery_type}_Dataflash_test
                    WHERE BatteryDataLine_Dataflash.CLASS = GoldenFile_{battery_type}_Dataflash_test.CLASS 
                    AND BatteryDataLine_Dataflash.SUBCLASS = GoldenFile_{battery_type}_Dataflash_test.SUBCLASS 
                    AND BatteryDataLine_Dataflash.NAME = GoldenFile_{battery_type}_Dataflash_test.NAME
                    AND (
                        (GoldenFile_{battery_type}_Dataflash_test.CheckType = 'EQUALITY' 
                        AND BatteryDataLine_Dataflash.MEASURED_VALUE = GoldenFile_{battery_type}_Dataflash_test.ExactValue)
                        OR
                        (GoldenFile_{battery_type}_Dataflash_test.CheckType = 'BOUNDARY'
                        AND CAST(BatteryDataLine_Dataflash.MEASURED_VALUE AS INT) >= CAST(GoldenFile_{battery_type}_Dataflash_test.MinBoundary AS INT)
                        AND CAST(BatteryDataLine_Dataflash.MEASURED_VALUE AS INT) <= CAST(GoldenFile_{battery_type}_Dataflash_test.MaxBoundary AS INT))
                    )
                ) THEN 'True'
                WHEN EXISTS (
                    SELECT 1 FROM GoldenFile_{battery_type}_Dataflash_test
                    WHERE BatteryDataLine_Dataflash.CLASS = GoldenFile_{battery_type}_Dataflash_test.CLASS 
                    AND BatteryDataLine_Dataflash.SUBCLASS = GoldenFile_{battery_type}_Dataflash_test.SUBCLASS 
                    AND BatteryDataLine_Dataflash.NAME = GoldenFile_{battery_type}_Dataflash_test.NAME
                ) THEN 'False'
                ELSE 'NA'
            END
        WHERE BatteryDataLine_Dataflash.FkID_BatteryData = {battery_data_id}
    ''')


    update_sbs_pass_query = text(f'''
    UPDATE BatteryDataLine_SBS
    SET PASS = 
        CASE
            WHEN EXISTS (
                SELECT 1 FROM GoldenFile_{battery_type}_SBS_test
                WHERE BatteryDataLine_SBS.NAME = GoldenFile_{battery_type}_SBS_test.NAME 
                AND (
                    (GoldenFile_{battery_type}_SBS_test.CheckType = 'EQUALITY' 
                    AND BatteryDataLine_SBS.MEASURED_VALUE = GoldenFile_{battery_type}_SBS_test.ExactValue)
                    OR
                    (GoldenFile_{battery_type}_SBS_test.CheckType = 'BOUNDARY'
                    AND CAST(BatteryDataLine_SBS.MEASURED_VALUE AS INT) >= CAST(GoldenFile_{battery_type}_SBS_test.MinBoundary AS INT)
                    AND CAST(BatteryDataLine_SBS.MEASURED_VALUE AS INT) <= CAST(GoldenFile_{battery_type}_SBS_test.MaxBoundary AS INT))
                )
            ) THEN 'True'
            WHEN EXISTS (
                SELECT 1 FROM GoldenFile_{battery_type}_SBS_test
                WHERE BatteryDataLine_SBS.NAME = GoldenFile_{battery_type}_SBS_test.NAME 
            ) THEN 'False'
            ELSE 'NA'
        END
    WHERE BatteryDataLine_SBS.FkID_BatteryData = {battery_data_id}
    ''')


    update_battery_data_pass_query = text(f'''
    UPDATE BatteryData
    SET PASS_SBS = (SELECT CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END
                    FROM BatteryDataLine_SBS
                    WHERE FkID_BatteryData = {battery_data_id} AND PASS = 'False'),
        PASS_Dataflash = (SELECT CASE WHEN COUNT(*) = 0 THEN 1 ELSE 0 END
                            FROM BatteryDataLine_Dataflash
                            WHERE FkID_BatteryData = {battery_data_id} AND PASS = 'False')
    WHERE PkID_BatteryData = {battery_data_id}
    ''')

    result = connection.execute(update_dataflash_pass_query)
    print(f"Dataflash affected rows: {result.rowcount}")

    result = connection.execute(update_sbs_pass_query)
    print(f"SBS affected rows: {result.rowcount}")

    result = connection.execute(update_battery_data_pass_query)
    print(f"BatteryData affected rows: {result.rowcount}")
    connection.commit()


def process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input, status):
    """Read, save, and send battery data for a given battery type."""

    small_delay()
    # read basic SBS data
    current_battery.read_basic_SBS_new()
    print(f"Done reading SBS data for {battery_type}...")
    small_delay()
    # read the dataflash
    current_battery.read_all_dataflash()
    print(f"Done reading dataflash for {battery_type}...")

    connection = engine.connect()
    serial_number = scanned_input
    # Insert the general battery information into the BatteryData table
    # Insert the general battery information into the BatteryData table
    battery_data = pd.DataFrame({
        "SerialNumber": [serial_number],
        "BatteryType": [battery_type],
        "Status": [status],
    })
    battery_data.to_sql("BatteryData", engine, if_exists="append", index=False)

    # get battery_data_id
    query = text('SELECT max(PkID_BatteryData) FROM BatteryData')
    result = connection.execute(query)
    battery_data_id = int(result.fetchone()[0])

    # Insert data from the data_SBS dataframe into the BatteryDataLine_SBS table
    sbs_data_to_insert = current_battery.data_SBS[['SBS_CMD', 'NAME', 'MEASURED_VALUE', 'UNIT']].copy()
    sbs_data_to_insert['FkID_BatteryData'] = battery_data_id
    sbs_data_to_insert.to_sql("BatteryDataLine_SBS", engine, if_exists="append", index=False)

    # Insert data from the data_df dataframe into the BatteryDataLine_Dataflash table
    dataflash_data_to_insert = current_battery.data_df[['CLASS', 'SUBCLASS', 'NAME', 'TYPE', 'MEASURED_VALUE', 'UNIT']].copy()
    dataflash_data_to_insert['FkID_BatteryData'] = battery_data_id
    dataflash_data_to_insert.to_sql("BatteryDataLine_Dataflash", engine, if_exists="append", index=False)
    
    print("Comparing to golden files...")
    golden_file_checks(battery_type, battery_data_id)

    print(f'Battery ID: {battery_data_id}')

    


def read_battery_data(current_battery, battery_type, serial_number, scanned_input, status):
    """Read battery data and save it to pickle files and SQL database."""

    if "bq3060" in battery_type:
        battery_type = "BQ3060"
        process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input, status)
        return True

    elif "1936.1B" in battery_type:
        battery_type = "BQ4050"
        process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input, status)
        return True

    elif "1737" in battery_type or "1636" in battery_type:
        battery_type = "BQ78350"
        current_battery.unseal_battery()
        time.sleep(1)
        process_battery_data(current_battery, battery_type, serial_number, engine, scanned_input, status)
        time.sleep(1)
        current_battery.seal_battery()
        return True
    else:
        return False



def gui_to_read_battery(scanned_input, status):
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
        read_success = read_battery_data(battery, battery_type, serial_number, scanned_input, status)
        if not read_success:
            print("\n\n")
            print("Could not read battery data")
            print("Please connect a battery and press 'Read battery' again")
            print("\n\n")
            ser.close()
            return False
        else:
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
