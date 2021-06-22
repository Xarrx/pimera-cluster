import unittest
from fsusbutil import LEDStateQueue

class TestLEDStateQueue(unittest.TestCase):
	
	def setUp(self):
		# init empty queue
		self.q_init = LEDStateQueue()
		
		# init 1 element queue
		self.q_1ele = LEDStateQueue()
		self.q_1ele.queue = [[0, 0, 'Event1']]
		self.q_1ele.entry_count = 1
		self.q_1ele.entry_tracker = {'Event1' : [0, 0, 'Event1']}

		# init multi element queue
		self.q_mult = LEDStateQueue()
		self.q_mult.queue = [
			[0, 0, 'Event1'],
			[1, 2, 'Event3'],
			[2, 1, 'Event2']
		]
		self.q_mult.entry_count = 3
		self.q_mult.entry_tracker = {
			'Event1' : [0, 0, 'Event1'],
			'Event3' : [1, 2, 'Event3'],
			'Event2' : [2, 1, 'Event2']
		}
	
	def tearDown(self):
		self.q_init.queue = []
		self.q_init.entry_count = 0
		self.q_init.entry_tracker = {}
		
		self.q_1ele.queue = []
		self.q_1ele.entry_count = 0
		self.q_1ele.entry_tracker = {}

		self.q_mult.queue = []
		self.q_mult.entry_count = 0
		self.q_mult.entry_tracker = {}

	#	
	# Test valid usage of add	
	#
	def test_add_on_empty(self):
		self.q_init.add_task('CPUTemperature', 0)
		self.assertEqual(self.q_init.queue[0], [0, 0, 'CPUTemperature'])
		self.assertEqual(self.q_init.entry_count, 1)
		self.assertTrue('CPUTemperature' in self.q_init.entry_tracker)
		self.assertEqual(self.q_init.entry_tracker['CPUTemperature'], [0, 0, 'CPUTemperature'])

	def test_add_on_1_element(self):
		self.q_1ele.add_task('Event2', 1)
		self.assertEqual(self.q_1ele.queue[0], [0, 0, 'Event1'])
		self.assertEqual(self.q_1ele.queue[1], [1, 1, 'Event2'])
		self.assertTrue('Event2' in self.q_1ele.entry_tracker)
		self.assertTrue('Event1' in self.q_1ele.entry_tracker)
		self.assertEqual(self.q_1ele.entry_tracker['Event2'], [1, 1, 'Event2'])
		self.assertEqual(self.q_1ele.entry_count, 2)
		
	def test_add_on_multi_element(self):
		self.q_mult.add_task('Event4', 1)
		self.assertEqual(self.q_mult.queue[0], [0, 0, 'Event1'])
		self.assertEqual(self.q_mult.queue[1], [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.queue[2], [1, 3, 'Event4'])
		self.assertEqual(self.q_mult.queue[3], [2, 1, 'Event2'])
		self.assertTrue('Event4' in self.q_mult.entry_tracker)
		self.assertEqual(self.q_mult.entry_tracker['Event4'], [1, 3, 'Event4'])
		self.assertEqual(self.q_mult.entry_count, 4)
	
	# 
	# Test invalid usage of add
	#	
	def test_add_duplicate(self):
		self.q_mult.add_task('Event3', 3)
		self.assertEqual(self.q_mult.queue[0], [0, 0, 'Event1'])
		self.assertEqual(self.q_mult.queue[1], [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.queue[2], [2, 1, 'Event2'])
		self.assertTrue('Event3' in self.q_mult.entry_tracker)
		self.assertEqual(self.q_mult.entry_tracker['Event3'], [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.entry_count, 3)

	
	#
	# Test valid usage of remove
	#	
	def test_remove_on_1_element(self):
		self.q_1ele.remove_task('Event1')
		self.assertEqual(self.q_1ele.queue[0], [0, 0, 'Event1'])
		self.assertTrue('Event1' in self.q_1ele.entry_tracker)
		self.assertEqual(self.q_1ele.entry_tracker['Event1'], '<Deactivated>')
		self.assertEqual(self.q_1ele.entry_count, 1)

	def test_remove_on_multi_element(self):
		self.q_mult.remove_task('Event3')
		self.assertEqual(self.q_mult.queue[0], [0, 0, 'Event1'])
		self.assertEqual(self.q_mult.queue[1], [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.queue[2], [2, 1, 'Event2'])
		self.assertTrue('Event3' in self.q_mult.entry_tracker)
		self.assertEqual(self.q_mult.entry_tracker['Event3'], '<Deactivated>')
		self.assertEqual(self.q_mult.entry_count, 3)

	# 
	# Test invalud usage of remove
	#
	def test_remvove_invalid_task(self):
		self.q_mult.remove_task('Event4')
		self.assertEqual(self.q_mult.queue[0], [0, 0, 'Event1'])
		self.assertEqual(self.q_mult.queue[1], [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.queue[2], [2, 1, 'Event2'])
		self.assertFalse('Event4' in self.q_mult.entry_tracker)
		self.assertEqual(self.q_mult.entry_count, 3)
		
	def test_remove_on_empty(self):
		self.q_init.remove_task('Event4')
		self.assertEqual(self.q_init.queue, [])
		self.assertFalse('Event4' in self.q_init.entry_tracker)
		self.assertEqual(self.q_init.entry_count, 0)


	#
	# Test pop usage
	#
	def test_pop_on_empty(self):
		popped = self.q_init.pop_task()
		self.assertEqual(popped, [])
		self.assertEqual(self.q_init.queue, [])
		self.assertEqual(self.q_init.entry_count, 0)

	def test_pop_on_1_element(self):
		popped = self.q_1ele.pop_task()
		self.assertEqual(popped, [0, 0, 'Event1'])
		self.assertEqual(self.q_1ele.queue, [])
		self.assertFalse('Event1' in self.q_1ele.entry_tracker)
		self.assertEqual(self.q_1ele.entry_count, 1)

	def test_pop_on_multi_element(self):
		popped = self.q_mult.pop_task()
		self.assertEqual(popped, [0, 0, 'Event1'])
		self.assertEqual(self.q_mult.queue[0], [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.queue[1], [2, 1, 'Event2'])
		self.assertFalse('Event1' in self.q_mult.entry_tracker)
		self.assertTrue('Event2' in self.q_mult.entry_tracker)
		self.assertTrue('Event3' in self.q_mult.entry_tracker)
		self.assertEqual(self.q_mult.entry_count, 3)
		
	def test_pop_on_removed_head(self):
		#self.q_mult.queue[0][2] = '<Deactivated>'
		self.q_mult.entry_tracker['Event1'] = '<Deactivated>'
		#self.q_mult.entry_tracker.pop('Event1')
		popped = self.q_mult.pop_task()
		self.assertEqual(popped, [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.queue[0], [2, 1, 'Event2'])
		self.assertFalse('Event1' in self.q_mult.entry_tracker)
		self.assertFalse('Event3' in self.q_mult.entry_tracker)
		self.assertTrue('Event2' in self.q_mult.entry_tracker)
		self.assertEqual(self.q_mult.entry_count, 3)


	#
	# Test peek usage
	#
	def test_peek_on_empty(self):
		peeked = self.q_init.peek()
		self.assertEqual(peeked, [])
		self.assertEqual(self.q_init.queue, [])
		self.assertEqual(self.q_init.entry_count, 0)

	def test_peek_on_1_element(self):
		peeked = self.q_1ele.peek()
		self.assertEqual(peeked, [0, 0, 'Event1'])
		self.assertEqual(self.q_1ele.queue[0], [0, 0, 'Event1'])
		self.assertTrue('Event1' in self.q_1ele.entry_tracker)
		self.assertEqual(self.q_1ele.entry_count, 1)

	def test_peek_on_multi_element(self):
		peeked = self.q_mult.peek()
		self.assertEqual(peeked, [0, 0, 'Event1'])
		self.assertEqual(self.q_mult.queue[0], [0, 0, 'Event1'])
		self.assertTrue('Event1' in self.q_mult.entry_tracker)
		self.assertEqual(self.q_mult.entry_count, 3)

	def test_peek_on_removed_head(self):
		self.q_mult.entry_tracker['Event1'] = '<Deactivated>'
		#self.q_mult.entry_tracker.pop('Event1')
		peeked = self.q_mult.peek()
		self.assertEqual(peeked, [1, 2, 'Event3'])
		self.assertEqual(self.q_mult.queue[0], [1, 2, 'Event3'])
		self.assertFalse('Event1' in self.q_mult.entry_tracker)
		self.assertTrue('Event2' in self.q_mult.entry_tracker)
		self.assertTrue('Event3' in self.q_mult.entry_tracker)



if __name__ == '__main__':
	unittest.main()
