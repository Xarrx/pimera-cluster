# led-controller
#
#

import serial, time

ser = serial.Serial('/dev/ttyACM0')
ser.write(b'B#000000-0050#FFFF00-0050\n')
ser.flush()
time.sleep(.3)

ser.write(b'F0100\n')
ser.flush()
time.sleep(.3)

ser.close()
