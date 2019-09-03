#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  heuristic.py                                                                #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Monday Sep 2019 9:23:28 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

from src.fn_c_heuristic_wrapper import fn_c_linear_conflicts

def fn_hamming(size, n_map, goal):
	# Find Hamming Heuristic Value
	ham = 0
	for row in zip(n_map, goal):
		for val in zip(row[0], row[1]):
			if val[0] != 0 and val[0] != val[1]:
				ham += 1
	return ham

def fn_manhattan(size, n_map, goal):
	# Find Manhattan Heuristic Value
	ret = 0
	state = []
	for row in n_map:
		state += list(row)
	end = []
	for row in goal:
		end += list(row)
	for i in range(size * size):
		ret += abs(i // size - end.index(state[i]) // size) + abs(i % size - end.index(state[i]) % size)
	return ret

def fn_linear_conflicts(size, n_map, goal):
	def get_loc(search_map, val):
		return [[i, row.index(val)] for i, row in enumerate(search_map) if row.count(val)][0]

	ret = fn_manhattan(size, n_map, goal)
	for i in range(size):
		for j in range(size):
			n = get_loc(goal, n_map[i][j])
			n2 = get_loc(goal, n_map[j][i])
			for k in range(j + 1, size):
				if n[0] == i:
					m = get_loc(goal, n_map[i][k])
					if m[0] == i and n[1] > m[1]:
						ret += 2
				if n[1] == i:
					m2 = get_loc(goal, n_map[k][i])
					if m2[1] == i and n2[0] > m2[0]:
						ret += 2
	return ret

heuristic = {"hamming":fn_hamming, "manhattan":fn_manhattan, "conflicts":fn_linear_conflicts, "fast":fn_c_linear_conflicts}