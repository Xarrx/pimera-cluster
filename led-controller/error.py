# led-controller
#
#

import serial, time

ser = serial.Serial('/dev/ttyACM0')
ser.write(b'B#000000-0200#FF0000-200\n')
ser.flush()
time.sleep(.3)

ser.write(b'F1000\n')
ser.flush()
time.sleep(.3)

ser.close()
