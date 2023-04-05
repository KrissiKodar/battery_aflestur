# Contents

This folder contains the code which allows the Arduino to read from the batteries by sending SMBus commands (using Two-wire communication (I2C)). The arduino is powered on, the python program waits for the boot message. After the boot message has been sent, then the python program can send which register it wants to read from, the arduino reads from the battery and then sends it back to the python program.