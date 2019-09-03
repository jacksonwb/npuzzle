#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  fn_c_heuristic_wrapper.py                                                   #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Wednesday December 1969 4:00:00 pm                                 #
#  Modified: Tuesday Sep 2019 3:02:07 pm                                       #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

import ctypes
import os

LIB = 'lib'

def fn_c_linear_conflicts(size, n_map, goal):
	lib_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], LIB)
	lib = os.path.join(lib_path, 'fn_c_lib.so')
	if not os.path.exists(lib):
		exit("Make C binaries to use fast heuristics!");
	fn_heur_lib = ctypes.CDLL(lib)
	n_ar = []
	for row in n_map:
		n_ar += list(row)
	g_ar = []
	for row in goal:
		g_ar += list(row)
	return fn_heur_lib.linearConflictDist((ctypes.c_int * (size ** 2))(*n_ar),
		(ctypes.c_int * (size ** 2))(*g_ar), size)
