# battery_i2c
This folder contains the c++ code for the arduino that communicates with the batteries through I2C.

The code has been modified to read the dataflashes of BQ3060, BQ4050, BQ78350 correctly. 

For BQ78350 it first unseals the battery, goes into full access mode and then reads the dataflash. After the whole dataflash has been read it seals the battery again.



# GUI
## contains OssurBatteryReader windows forms application for reading of the batteries (work in progress)

It is a modified version of SmartBatteryHack, it has been modified to read the dataflash off BQ3060, BQ4050, BQ78350 correctly.

Currently it reads the entire dataflashes and save them to .csv files which contain the data in raw bytes. It also parses the raw data bytes and saves the measured values in .CSV files. SQL queries are still to be implemented for the C# code.

# python_files
## see inside the "python_files" folder for more detailed information.

Files in this folder communicate with the arduino and tell it what it wants to read from the batteries, it contains:
- gui.py contains the graphical user interface
- pkl_files contain templates that are used for reading the data of the various batteries
- measured_data_pkl_files contains the data read from the various batteries
- reading_datasheets_tabular contains the datasheets for the batteries and the python files used for reading data tables from the datasheets
- batteries.py contains the code for reading data of the various batteries
- simple_reads.py is for testing and debugging
- requirements.txt contains the python packages used for this project. To install the packages type `pip install -r requirements.txt`