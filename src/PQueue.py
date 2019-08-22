#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  PQueue.py                                                                   #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Wednesday Aug 2019 9:15:55 pm                                     #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import heapq

class PQueue:
	def __init__(self, key=lambda x: x):
		self.key = key
		self._data = []
		self._set = set()
	def push(self, item):
		heapq.heappush(self._data, (self.key(item), item))
		self._set.add(item)
	def pop(self):
		item = heapq.heappop(self._data)[1]
		self._set.remove(item)
		return item
	def is_empty(self):
		return False if len(self._data) else True
	def print_queue(self):
		for e in self._data:
			print(e)
	def contains(self, item):
		return item in self._set
	def heapify(self):
		heapq.heapify(self._data)