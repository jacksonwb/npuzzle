#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  npuzzle.py                                                                  #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday August 2019 8:46:34 pm                                      #
#  Modified: Tuesday Sep 2019 2:53:34 pm                                       #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

from src.solver import Puzzle
from src.parse import *
from src.heuristic import heuristic

if __name__ == "__main__":
	args = parse()
	try:
		puzzle = Puzzle(*process_input(args), heuristic[args.function], args.greedy)
		puzzle.solve()
		puzzle.print_solution()
	except (BaseException) as e:
		print("npuzzle:",e)

