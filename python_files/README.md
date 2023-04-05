# Contents

Here are all of the python files used for this project.

The `gui.py` file contains the graphical user interface and is very much a work in progress. Right now it works sort of like this. First connect battery to the arduino and then the arduino the PC. Then a "Read battery" button is pressed. The program then reads the "Device name" of the current battery. It uses the "Device name" to know which battery type it is supposed to read, which is very important because otherwise it will just read jibberish or crash the program due to trying to process information that might not be there. After it gets the "Device name" it reads the battery gauge serial number and then goes through reading the SBS and dataflash. The measured values are compared to "golden files" (which have not clearly been defined yet), if something is different between the measure and golden file the program can ouptut a message to the screen. After reading the SBS and dataflash the measured values are stored as dataframes in the folder `./python_files/measured_data_pkl_files/`. After all of this the battery can be read again (which is kind of pointless) or a new battery can be connected and read.

The `create_golden_files.py` basically contains code that reads a specified dataframe and then saves that dataframe as "the golden file".

The `batteries.py` file contains a parent class `battery_gauge` as well as battery gauge classes which inherit from `battery_gauge` for each of the specific batteries that were read from in this project. Those classes take as input the serial number of the current battery, a dataframe for the dataflash and a dataframe for the SBS commands. They then use those dataframes to correctly read from the batteries and process the information, and place the read values back in to the dataframes in a column called `MEASURED VALUES`.

The `simple_reads.py` file contains code that was used in the project to test reading from the battery and for debugging.