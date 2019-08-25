#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  parse.py                                                                    #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Saturday Aug 2019 7:08:47 pm                                      #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import argparse
import re
import itertools
from src.generate import make_random_puzzle

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
	parser.add_argument('-f', '--function', help='Specify heuristic function', default="manhattan", choices=['hamming', 'manhattan', 'conflicts'])
	parser.add_argument('-g', '--greedy', help='Use greedy path finding', action='store_true')
	input_group = parser.add_mutually_exclusive_group(required=True)
	input_group.add_argument('-r', '--random', dest='size', type=check_random_size_input,
		help='Generate random puzzle of specified size')
	input_group.add_argument('-m', '--map', dest='file', metavar='MAP',
		help='Read puzzle from file')
	return parser.parse_args()

def validate_map(n, n_map):
	valid = []
	try:
		valid.append(len(n_map) == n)
		valid.append(all([len(row) == n for row in n_map]))
		flat = list(itertools.accumulate([list(row) for row in n_map]))[-1]
		valid.append(all([flat.count(i) == 1 for i in range(n * n)]))
	except:
		raise SyntaxError('Invalid Map')
	if not all(valid):
		raise SyntaxError('Invalid Map')
	return [n, n_map]

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
	return validate_map(n, tuple(n_map))

def process_input(args):
	if args.size:
		print('Using Random map of size:', args.size)
		return [int(args.size), make_random_puzzle(int(args.size))]
	elif args.file:
		with open(args.file, 'r') as f:
			data = f.read().splitlines()
		return parse_map(data)