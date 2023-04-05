# Contents

BQ"number"_df is the dataframe that the program uses for reading the dataflash from the respective battery. The program uses the dataframe to know which address stores which measurement. It also stores the size in byte of the measurement and the program also uses that to know how much to read at once (a word or a block read (> 2 bytes)).

BQ"number"_df_golden_file is the file which the newly read dataflash data is supposed to be compared to, to see if some values are not what they are supposed to be.

SBS_BQ"number" are dataframes used for reading the "simple" SBS data off of the batteries. The standard SBS commands are the same for all batteries (the values in 0x00 to 0x3f), but they all have extended SBS commands that can be very different between batteries and that is why multiple "SBS" dataframes are required.