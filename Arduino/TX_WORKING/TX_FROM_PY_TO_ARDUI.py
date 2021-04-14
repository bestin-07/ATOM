import serial
import struct
import time

arduino = serial.Serial('COM5', 9600, timeout=0)

# let it initialize
time.sleep(2)

# send the first int in binary format
arduino.write(struct.pack('>BBBB',2,3,5,10))
