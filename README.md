# battery_i2c
This folder contains the c++ code for the arduino that communicates with the batteries through I2C. This folder should not need any changes.

# python_files

Files in this folder communicate with the arduino and tell it what it wants to read from the batteries, it contains:
- gui.py contains the graphical user interface
- pkl_files contain templates that are used for reading the data of the various batteries
- measured_data_pkl_files contains the data read from the various batteries
- reading_datasheets_tabular contains the datasheets for the batteries and the python files used for reading data tables from the datasheets
- batteries.py contains the code for reading data of the various batteries
- simple_reads.py is for testing and debugging
- requirements.txt contains the python packages used for this project. To install the packages type `pip install -r requirements.txt`