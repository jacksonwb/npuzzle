#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  npuzzle.py                                                                  #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday August 2019 8:46:34 pm                                      #
#  Modified: Sunday Aug 2019 9:26:29 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import argparse

def parse():
	parser = argparse.ArgumentParser(description='N-Puzzle solver using A* searching '
		'with selectable heuristics')
	parser.add_argument('-f', '--function', help='Specify heuristic function')
	input_group = parser.add_mutually_exclusive_group(required=True)
	input_group.add_argument('-r', '--random', dest='size', help='Use random puzzle of specified size')
	input_group.add_argument('-i', '--input', dest='file', help='Use puzzle read from file')
	return parser.parse_args()

if __name__ == "__main__":
	print(parse())