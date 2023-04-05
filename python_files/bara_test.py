import serial
from serial.tools import list_ports
from serial import Serial

port = list(list_ports.comports())
if len(port) == 0:
    print("No USB connection found")

print(port)
for p in port:
    print(p.device)