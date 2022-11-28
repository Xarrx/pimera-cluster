#!/usr/bin/python
#
# TODO:	Add function to check if the serial device exits.
#	Add function to locate the correct serial device.
#	Add option to specify tty serial device.
#
import sys
import heapq

'''
Class to implement a custom priority queue.
 - data will be stored as 4-tuples
  ( priority, entry_count, mode, event )
 - need to be able to check if a task already exists for a given event.
 - if 
'''
class LEDStateQueue():
	
	DEACTIVATED	= '<Deactivated>'

	def __init__(self):
		self.queue = []
		self.entry_count = 0
		self.entry_tracker = {}

	def dispose(self):
		self.queue = []
		self.entry_count = 0
		self.entry_tracker = {}

	def add_task(self, task, priority):
		# check if the event already exists
		if task not in self.entry_tracker:
			#print('task add')
			entry = [priority, self.entry_count, task]
			self.entry_tracker[task] = entry
			self.entry_count += 1
			heapq.heappush(self.queue, entry)
			#print(self.entry_tracker)


	def remove_task(self, task):
		# check if the task exists
		if task in self.entry_tracker:
			#print('task remove')
			# remove the task from the tracker
			#entry = self.entry_tracker.pop(task)
			self.entry_tracker[task] = self.DEACTIVATED
			# set the task to deactivated
			#entry[-1] = self.DEACTIVATED

	def pop_task(self):
		
		# loop until the queue is empty or a valid task is found
		while self.queue:
			
			# pop using heappop
			priority, count, task = heapq.heappop(self.queue)
			
			# check if the task is not deactivated
			if not self.entry_tracker[task] == self.DEACTIVATED:
	
				# delete the entry from the tracker
				del self.entry_tracker[task]
				
				# return the valid popped task
				return [priority, count, task]
			else:
				del self.entry_tracker[task]
	
		# found no valid tasks or the queue was empty
		return []
			


	def peek(self):
		
		# loop until the q is empty or a valid task is at the head of the heap
		while self.queue:
			
			# copy the head
			copy = self.queue[0].copy()

			# check if the head is valid
			if not self.entry_tracker[copy[-1]] == self.DEACTIVATED:
				return copy
			
			else:
				# head is deactivated; pop it off and try again
				heapq.heappop(self.queue)
				del self.entry_tracker[copy[-1]]

		# found no valid tasks to peek or the queue was empty
		return []
	
	def peek2(self):
		pop = self.pop_task()
		if pop == []:
			return []
		else: 
			ret = pop.copy()
			self.entry_tracker[ret[-1]] = ret
			heapq.heappush(self.queue, pop)
			return ret
		return []
'''
Class to handle the state of the FitStatUSB device.
 - Stores the current state of the FitStatUSB device and handles requests to change this state,
 - Uses a priority queue to determine which mode should be set and when.
 
 - When an attempt to set the LED state is received, the instance needs to:
  * check if that state is already in the mode queue; if it is the mode change is ignored.
  * if it is not in the mode queue, it is added
'''
class FSUSBDevice():

	# Define color bytes
	attn_bytes 	= b'B#000000-0050#FFFF00-0050\n'
	blink_bytes 	= b'B#000000-0050#0000FF-0050\n'
	default_bytes 	= b'B#002000-0200#004000-200\n'
	error_bytes	= b'B#000000-0200#FF0000-200\n'

	# define mode priority
	MODE_DEFAULT	= 3
	MODE_BLINK	= 0
	MODE_ATTN	= 2
	MODE_ERROR	= 1

	def __init__(self, serial_device):
		self.serial_device = serial_device
		#self.mode = self.MODE_DEFAULT
	
	def get_mode(self):
		pass
		
	def set_mode(self, new_mode):
		if new_mode == self.MODE_DEFAULT:
			self.set_led_default()
		elif new_mode == self.MODE_BLINK:
			self.set_led_blink()
		elif new_mode == self.MODE_ATTN:
			self.set_led_attn()
		elif new_mode == self.MODE_ERROR:
			self.set_led_error()
		else:
			self.set_led_default()
	
	def set_led(self, b):
		import serial
		from time import sleep
		ser = serial.Serial(self.serial_device)
		ser.write(b)
		ser.flush
		sleep(0.3)
		ser.close()
		
	def set_led_attn(self):
		self.set_led(self.attn_bytes)
		#self.mode = self.MODE_ATTN

	def set_led_blink(self):
		self.set_led(self.blink_bytes)
		#self.mode = self.MODE_BLINK

	def set_led_default(self):
		self.set_led(self.default_bytes)
		#self.mode = self.MODE_DEFAULT

	def set_led_error(self):
		self.set_led(self.error_bytes)
		#self.mode = self.MODE_ERROR

	


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

