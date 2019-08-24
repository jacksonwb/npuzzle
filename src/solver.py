#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  solver.py                                                                   #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Friday Aug 2019 4:58:06 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import time
from src.generate import make_goal_puzzle
from src.check_solvable import is_solvable
from src.PQueue import PQueue

GREEN = "\033[32m"
RED = "\033[31m"
NO_COLOR = "\033[0m"

class PuzzleException(Exception):
	pass

def generate_children(n_map, size):
	zero = [[i, row.index(0)] for i, row in enumerate(n_map) if row.count(0)][0]
	pos_lst = [[sum(y) for y in zip(zero, x)] for x in [[0,1], [0,-1], [1,0], [-1,0]]]
	for pos in pos_lst:
		if all(map(lambda x: x < size and x >= 0, pos)):
			new_map = list([list(row) for row in n_map])
			new_map[zero[0]][zero[1]], new_map[pos[0]][pos[1]] =  new_map[pos[0]][pos[1]], new_map[zero[0]][zero[1]]
			yield tuple(tuple(row) for row in new_map)

class Puzzle:
	def __init__(self, size, in_map, h_fn, lazy):
		self.size = size
		self.start = make_goal_puzzle(self.size)
		self.finish = in_map
		if not is_solvable(size, self.finish, self.start):
			raise PuzzleException(RED + "Not Solvable" + NO_COLOR)
		self.h_fn = h_fn
		self.open_set = PQueue(key=lambda x: (self.g_val[x] if not lazy else 0) + self.h_fn(self.size, x, self.finish))
		self.closed_set = {}
		self.parent = dict([(self.start, None)])
		self.g_val = {}
		self.g_val[self.start] = 0

	def solve(self):
		self.start_time = time.process_time()
		self.open_set.push(self.start)
		while not self.open_set.is_empty():
			current = self.open_set.pop()
			self.closed_set[current] = current
			if current == self.finish:
				self.end_time = time.process_time()
				return
			for child in generate_children(current, self.size):
				if child in self.closed_set:
					continue
				tentative_g_val = self.g_val[current] + 1
				if not self.open_set.contains(child) or tentative_g_val < self.g_val[child]:
					self.g_val[child] = tentative_g_val
					self.parent[child] = current
					self.open_set.push(child)

	def map_str(self, n_map):
		s = len(str(len(n_map) ** 2))
		return '\n'.join([''.join(map(lambda x: str(x).rjust(s + 1), row)) for row in n_map])

	def print_all_states(self, state):
		solution = []
		while state:
			solution.append(state)
			print(self.map_str(state), '\n')
			state = self.parent[state]

	def print_solution(self):
		self.print_all_states(self.finish)
		print(GREEN, f"Solved in {self.end_time - self.start_time:.4f} seconds", NO_COLOR, sep='')
		print("Time complexity:", len(self.closed_set))
		print("Space Complexity:", len(self.g_val))
		print("Number of steps:", self.g_val[self.finish])