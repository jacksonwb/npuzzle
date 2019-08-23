#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  PQueue.py                                                                   #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Thursday Aug 2019 11:58:18 am                                     #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import heapq
from itertools import count

class PQueue:
	def __init__(self, key=lambda x: x):
		self.key = key
		self._data = []
		self._dict = {}
		self.REM = '<removed-item>'
		self.counter = count()
	def __le__(self, value):
	 return super().__le__(value)
	def push(self, item):
		# Add item to PQ, if already present, update the entry
		if item in self._dict:
			self.remove(item)
		count = next(self.counter)
		entry = [self.key(item), count, item]
		self._dict[item] = entry
		heapq.heappush(self._data, entry)
	def remove(self, item):
		entry = self._dict.pop(item)
		entry[-1] = self.REM
	def pop(self):
		while self._data:
			priority, count, item = heapq.heappop(self._data)
			if item is not self.REM:
				del(self._dict[item])
				return item
		raise KeyError('pop from empty Priority Queue')
	def is_empty(self):
		return False if len(self._dict) else True
	def print_queue(self):
		for e in self._data:
			print(e)
	def contains(self, item):
		return item in self._dict
	def size(self):
		return len(self._dict)
