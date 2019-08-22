#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  npuzzle.py                                                                  #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday August 2019 8:46:34 pm                                      #
#  Modified: Wednesday Aug 2019 9:24:12 pm                                     #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import argparse
import re
import itertools
from generate import make_random_puzzle, make_goal_puzzle
from PQueue import PQueue

def check_random_size_input(val):
	try:
		int_val = int(val)
	except:
		raise argparse.ArgumentTypeError(f'{val} is not a valid int')
	if 2 < int(val) < 6:
		return val
	else:
		raise argparse.ArgumentTypeError(f'{val} is invalid - must be between 2 and 6')

def parse():
	parser = argparse.ArgumentParser(description='N-Puzzle solver using A* searching '
		'with selectable heuristics')
	parser.add_argument('-f', '--function', help='Specify heuristic function')
	input_group = parser.add_mutually_exclusive_group(required=True)
	input_group.add_argument('-r', '--random', dest='size', type=check_random_size_input,
		help='Generate random puzzle of specified size')
	input_group.add_argument('-m', '--map', dest='file', metavar='MAP',
		help='Read puzzle from file')
	return parser.parse_args()

def parse_map(data):
	data = list(filter(lambda l: l[0] != '#', data))
	try:
		n = int(re.search('^(\d)$', data[0]).group())
	except:
		raise SyntaxError('Invalid or missing N value')
	if len(data[1:]) > n:
		raise SyntaxError('Invalid map size')
	n_map = []
	for i, l in enumerate(data[1:]):
		try:
			row = tuple(map(int, l.split('#')[0].split()))
		except:
			raise SyntaxError(f'Bad syntax in map row {i + 1}')
		if len(row) != n:
			raise SyntaxError(f'Invalid map row: {i + 1}')
		n_map.append(row)
	return [n, tuple(n_map)]

def process_input(args):
	if args.size:
		print('Using Random map of size:', args.size)
		return [int(args.size), make_random_puzzle(int(args.size))]
	elif args.file:
		with open(args.file, 'r') as f:
			data = f.read().splitlines()
		return parse_map(data)

def fn_hamming(size, n_map, goal):
	ham = 0
	for row in zip(n_map, goal):
		for val in zip(row[0], row[1]):
			if val[0] != val[1]:
				ham += 1
	return ham

class State:
	def __init__(self, n_map, g_val, parent, h_fn, goal):
		self.n_map = n_map
		self.size = len(n_map);
		self.g_val = g_val
		self.parent = parent
		self.h_fn = h_fn
		self.h_val = h_fn(self.size, self.n_map, goal)
		self.f_val = g_val + self.h_val
		self.goal = goal
	def __repr__(self):
		return '\n'.join([' '.join(map(str, row)) for row in self.n_map])
	def __eq__(self, other):
		if isinstance(other, State):
			return self.n_map == other.n_map
		return NotImplemented
	def is_goal(self):
		return self.n_map == self.goal
	def map_str(self, n_map):
		return '\n'.join([' '.join(map(str, row)) for row in n_map])
	def generate_children(self):
		zero = [[i, row.index(0)] for i, row in enumerate(self.n_map) if row.count(0)][0]
		pos_lst = [[sum(y) for y in zip(zero, x)] for x in [[0,1], [0,-1], [1,0], [-1,0]]]
		for pos in pos_lst:
			if all(map(lambda x: x < self.size and x >= 0, pos)):
				new_map = list([list(row) for row in self.n_map])
				new_map[zero[0]][zero[1]], new_map[pos[0]][pos[1]] =  new_map[pos[0]][pos[1]], new_map[zero[0]][zero[1]]
				yield State(tuple(tuple(row) for row in new_map), self.g_val + 1, self, self.h_fn, self.goal)

def generate_children(n_map, size):
	zero = [[i, row.index(0)] for i, row in enumerate(n_map) if row.count(0)][0]
	pos_lst = [[sum(y) for y in zip(zero, x)] for x in [[0,1], [0,-1], [1,0], [-1,0]]]
	for pos in pos_lst:
		if all(map(lambda x: x < size and x >= 0, pos)):
			new_map = list([list(row) for row in n_map])
			new_map[zero[0]][zero[1]], new_map[pos[0]][pos[1]] =  new_map[pos[0]][pos[1]], new_map[zero[0]][zero[1]]
			yield tuple(tuple(row) for row in new_map)

class Puzzle:
	def __init__(self, size, in_map, h_fn):
		self.size = size
		self.finish = make_goal_puzzle(self.size)
		self.start = in_map
		self.h_fn = h_fn
		self.open_set = PQueue(key=lambda x: self.g_val[x] + self.h_fn(self.size, x, self.finish))
		self.closed_set = {}
		self.parent = {}

		#initialize g_val dict
		self.g_val = {}
		self.g_val[self.start] = 0

		self.states_processed = 0
	def solve(self):
		self.open_set.push(self.start)
		while not self.open_set.is_empty():
			self.states_processed += 1
			current = self.open_set.pop()
			self.closed_set[current] = current
			if current == self.finish:
				return
			for child in generate_children(current, self.size):
				if child in self.closed_set:
					continue
				tentative_g_val = self.g_val[current] + 1
				if not self.open_set.contains(child):
					self.g_val[child] = tentative_g_val
					self.parent[child] = current
					self.open_set.push(child)
				elif tentative_g_val < self.g_val[child]:
					print('here')
					self.g_val[child] = tentative_g_val
					self.parent[child] = current
	def map_str(self, n_map):
		return '\n'.join([' '.join(map(str, row)) for row in n_map])

	def print_all_states(self, state):
		while state != self.start:
			print(self.map_str(state), '\n')
			state = self.parent[state]
		print(self.map_str(self.start))
	def print_solution(self):
		self.print_all_states(self.finish)
		print("Number of states processed:", self.states_processed)
		print("Max Size:", len(self.closed_set))
		print("Number of steps:", self.g_val[self.finish])


# class Puzzle:
# 	def __init__(self, size, start_map, h_fn):
# 		self.size = size
# 		self.goal_map = make_goal_puzzle(self.size)
# 		self.start = State(self.goal_map, 0, None, h_fn, start_map)
# 		self.h_fn = h_fn
# 		self.open_set = PQueue(key=lambda x: x.f_val)
# 		self.closed_set = {}
# 		self.states_processed = 0
# 		self.bad = 0
# 	def solve(self):
# 		self.open_set.push(self.start)
# 		while not self.open_set.is_empty():
# 			self.states_processed += 1
# 			current = self.open_set.pop()
# 			self.closed_set[current.n_map] = current
# 			if current.is_goal():
# 				self._goal = current
# 				return
# 			for child in current.generate_children():
# 				if child.n_map in self.closed_set:
# 					continue
# 				# if child.n_map not in self.open_dict or child.g_val < self.open_dict[child.n_map].g_val:
# 				# self.open_dict[child.n_map] = child
# 				if self.open_set.contains(child):
# 					self.bad += 1;
# 				else:
# 					self.open_set.push(child)
# 	def print_all_states(self, state):
# 		while state:
# 			print(state, '\n')
# 			state = state.parent
# 	def print_solution(self):
# 		self.print_all_states(self._goal)
# 		print("Number of states processed:", self.states_processed)
# 		print("Max Size:", len(self.closed_set))
# 		print("Number of steps:", self._goal.g_val)
# 		print("bad", self.bad)

if __name__ == "__main__":
	args = parse()
	# try:
	puzzle = Puzzle(*process_input(args), fn_hamming)
	puzzle.solve()
	puzzle.print_solution()
	# except SyntaxError as e:
	# 	print(e)

