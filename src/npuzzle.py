#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  npuzzle.py                                                                  #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday August 2019 8:46:34 pm                                      #
#  Modified: Monday Aug 2019 3:31:05 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import argparse
import re

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
	return tuple(n_map)

def validate_input(args):
	if args.size:
		print('Using Random map of size:', args.size)
	elif args.file:
		with open(args.file, 'r') as f:
			data = f.read().splitlines()
		return parse_map(data)

def npuzzle(args):
	n_map = validate_input(args)

if __name__ == "__main__":
	args = parse()
	print(args)
	try:
		npuzzle(args)
	except Exception as e:
		print(e)

