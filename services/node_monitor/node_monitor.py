#!/usr/bin/python3.7

from gpiozero import CPUTemperature
from signal import pause
from src.fsusbutil import LEDStateQueue, FSUSBDevice, get_serial_device
from threading import Lock
#import pprint

# probably wont need to use a mutex unless the class is changed to hold the state of the led device.
led_device = FSUSBDevice(get_serial_device())

# This will NEED some kind of locking; getting bugs with the entry_tracker not having anything in it right after adding to it.
led_q = LEDStateQueue()

qlock = Lock()

#pp = pprint.PrettyPrinter(indent=4)

'''
 Callback to handle when the state changes
'''
def activated_callback(device):
	with qlock:
		#print(led_q.entry_tracker)
		if device.is_active:
			# change the led state to attn mode
			#led_device.set_led_attn()
			print('CPU Temperature Threshold Reached | Activated | CPU Temp: {}'.format(device.temperature))
			led_q.add_task('CPUTemperature', led_device.MODE_ATTN)
		else:
			# change the led state to default mode
			#led_device.set_led_default()
			print('CPU Temperature Threshold Reached | Deactivated | CPU Temp: {}'.format(device.temperature))
			led_q.remove_task('CPUTemperature')
			#led_q.pop_task()
	
		#print(led_q.entry_tracker)
	
		peeked = led_q.peek()
	
		#print(peeked)	
	
		if not peeked == []:
			led_device.set_mode(peeked[0])
		else:
			led_device.set_led_default()
		#pp.pprint(led_q.queue)
		#pp.pprint(led_q.entry_tracker)



'''
 Function to handle the service.
'''
def main(argv):
	#import getopt # going to add arguments later for daemonization, logging, etc...

	# init the cputemperature class
	cpu = CPUTemperature(
		threshold=50.0,
		event_delay=1.0
	)
	
	# set the callbacks
	cpu.when_activated = activated_callback
	cpu.when_deactivated = activated_callback

	# wait for events to happen
	pause()
	


if __name__ == '__main__':
	import sys
	main(sys.argv[1:])
