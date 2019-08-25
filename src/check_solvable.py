#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  check_solvable.py                                                           #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Saturday Aug 2019 1:04:04 pm                                      #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

def is_solvable(n, n_map, goal):
	start = []
	for row in n_map:
		start += list(row)
	finish = []
	for row in goal:
		finish += list(row)
	inversion = 0
	for i in range(n * n):
		for j in range(i + 1, n * n):
			if finish.index(start[i]) > finish.index(start[j]):
				inversion += 1
	start_zero_row = start.index(0) // n
	start_zero_col = start.index(0) % n
	finish_zero_row = finish.index(0) // n
	finish_zero_col = finish.index(0) % n
	zero_dif = abs(start_zero_row - finish_zero_row) + abs(start_zero_col - finish_zero_col)
	if zero_dif % 2 == 0 and inversion % 2 == 0:
		return True
	if zero_dif % 2 == 1 and inversion % 2 == 1:
		return True
	return False
