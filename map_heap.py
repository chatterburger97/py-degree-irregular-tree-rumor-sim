from heapq import *
import itertools

class MapHeap : 

	REMOVED = '<removed-task>'      # placeholder for a removed task
	
	def __init__(self, argument_map=dict()) :
		self.pq = []				# list of entries arranged in a heap
		self.entry_finder = {}		# mapping of tasks to entries
		self.counter = itertools.count()     # unique sequence count
		for val in argument_map.keys() :
			self.add_task(val, argument_map[val])

	def add_task(self, task, priority=0):
	    # 'Add a new task or update the priority of an existing task'
	    if task in self.entry_finder:
	        self.remove_task(task)
	    count = next(self.counter)
	    entry = [priority, count, task]
	    self.entry_finder[task] = entry
	    heappush(self.pq, entry)

	def remove_task(self, task):
	    # 'Mark an existing task as REMOVED.  Raise KeyError if not found.'
	    entry = self.entry_finder.pop(task)
	    entry[-1] = MapHeap.REMOVED

	def pop_task(self):
	    # 'Remove and return the lowest priority task. Raise KeyError if empty.'
	    while self.pq:
	        priority, count, task = heappop(self.pq)
	        if task is not MapHeap.REMOVED:
	            del self.entry_finder[task]
	            return task
	    raise KeyError('pop from an empty priority queue')

	def peek_min(self):
	    # 'Remove and return the lowest priority task. Raise KeyError if empty.'
	    while self.pq:
	        priority, count, task = heappop(self.pq)
	        if task is not REMOVED:
	            del self.entry_finder[task]
	            return task
	    raise KeyError('pop from an empty priority queue')