#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  npuzzle.py                                                                  #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday August 2019 8:46:34 pm                                      #
#  Modified: Thursday Aug 2019 5:21:43 pm                                      #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import argparse
import re
import itertools
from generate import make_random_puzzle, make_goal_puzzle
from PQueue import PQueue
from check_solvable import is_solvable

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
			if val[0] != 0 and val[0] != val[1]:
				ham += 1
	return ham

def generate_children(n_map, size):
	zero = [[i, row.index(0)] for i, row in enumerate(n_map) if row.count(0)][0]
	pos_lst = [[sum(y) for y in zip(zero, x)] for x in [[0,1], [0,-1], [1,0], [-1,0]]]
	for pos in pos_lst:
		if all(map(lambda x: x < size and x >= 0, pos)):
			new_map = list([list(row) for row in n_map])
			new_map[zero[0]][zero[1]], new_map[pos[0]][pos[1]] =  new_map[pos[0]][pos[1]], new_map[zero[0]][zero[1]]
			yield tuple(tuple(row) for row in new_map)

class PuzzleException(Exception):
	pass

class Puzzle:
	def __init__(self, size, in_map, h_fn):
		self.size = size
		self.start = make_goal_puzzle(self.size)
		self.finish = in_map
		if not is_solvable(size, self.finish, self.start):
			raise PuzzleException("Not Solvable")
		self.h_fn = h_fn
		self.open_set = PQueue(key=lambda x: self.g_val[x] + self.h_fn(self.size, x, self.finish))
		self.closed_set = {}
		self.parent = dict([(self.start, None)])

		#initialize g_val dict
		self.g_val = {}
		self.g_val[self.start] = 0

		self.states_processed = 0
		self.max_size = 0
	def solve(self):
		self.open_set.push(self.start)
		while not self.open_set.is_empty():
			self.states_processed += 1
			self.max_size = max(self.max_size, self.open_set.size())
			current = self.open_set.pop()
			self.closed_set[current] = current
			if current == self.finish:
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
		return '\n'.join([' '.join(map(str, row)) for row in n_map])

	def print_all_states(self, state):
		solution = []
		while state:
			solution.append(state)
			print(self.map_str(state), '\n')
			state = self.parent[state]
		print(self.map_str(self.start))
	def print_solution(self):
		self.print_all_states(self.finish)
		print("Number of states processed:", len(self.closed_set))
		print("Max Size:", len(self.g_val))
		print("Number of steps:", self.g_val[self.finish])

if __name__ == "__main__":
	args = parse()
	try:
		puzzle = Puzzle(*process_input(args), fn_hamming)
		puzzle.solve()
		puzzle.print_solution()
	except (SyntaxError, PuzzleException) as e:
		print("npuzzle:",e)

