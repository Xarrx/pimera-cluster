#!/usr/bin/python3.7
#
# TODO:	Add function to check if the serial device exits.
#	Add function to locate the correct serial device.
#	Add option to specify tty serial device.
#
import sys

def get_serial_device():
	ret = None
	#f = open('/tmp/tty_device', 'r')
	#ret = f.readline()
	#f.close()
	with open('/tmp/tty_device', 'r') as f:
		ret = f.readline()

	return ret

def set_led(bin):
	import serial
	from time import sleep

	# create the serial device
	ser = serial.Serial(get_serial_device())
	
	# write binary to open seial device
	ser.write(bin)
	ser.flush()

	# sleep to wait for setting to apply
	sleep(.3)
	
	# close the serial device
	ser.close()
	
def main(argv):
	import getopt
	version = 'v0.2.20210506'
	def usage(ret=0):
		print('''
Usage: led_controller.py <option> [-D]

Options:
  -h,--help \tPrint this usage info and exit.
  -a,--attn \tSet the LED state to attention mode.
  -b,--blink \tSet the LED state to blinking mode.
  -d,--default \tReset the LED state to deafult mode.
  -e,--error \tSet the LED state to error mode.
  -v,--version \tPrint the version number and exit.
  -D,--device \tSpecify tty device to use.
''')
		sys.exit(ret)
	
	try:
		opts, args = getopt.getopt(argv, 'habdev', ['help', 'attn', 'blink', 
		'default', 'error', 'version'])
	except getopt.GetoptError:
		print('Error: Invalid option')
		usage(2)
	
	# loop over passed arguments
	for opt, arg in opts:
	
		if opt == '-h' or opt == '--help':
			usage()
		
		elif opt == '-a' or opt == '--attn':
			set_led(b'B#000000-0050#FFFF00-0050\n')
			
		elif opt == '-b' or opt == '--blink':
			set_led(b'B#000000-0050#0000FF-0050\n')
			
		elif opt == '-d' or opt == '--default':
			set_led(b'B#002000-0200#004000-200\n')
			
		elif opt == '-e' or opt == '--error':
			set_led(b'B#000000-0200#FF0000-200\n')
			
		elif opt == '-v' or opt == '--version':
			print(version)
			sys.exit()
			
		else:
			print('Error: Invalid option.')
			usage(2)
			
		
		
if __name__ == '__main__':
	main(sys.argv[1:])
