
# class State:
# 	def __init__(self, n_map, g_val, parent, h_fn, goal):
# 		self.n_map = n_map
# 		self.size = len(n_map);
# 		self.g_val = g_val
# 		self.parent = parent
# 		self.h_fn = h_fn
# 		self.h_val = h_fn(self.size, self.n_map, goal)
# 		self.f_val = g_val + self.h_val
# 		self.goal = goal
# 	def __repr__(self):
# 		return '\n'.join([' '.join(map(str, row)) for row in self.n_map])
# 	def __eq__(self, other):
# 		if isinstance(other, State):
# 			return self.n_map == other.n_map
# 		return NotImplemented
# 	def is_goal(self):
# 		return self.n_map == self.goal
# 	def map_str(self, n_map):
# 		return '\n'.join([' '.join(map(str, row)) for row in n_map])
# 	def generate_children(self):
# 		zero = [[i, row.index(0)] for i, row in enumerate(self.n_map) if row.count(0)][0]
# 		pos_lst = [[sum(y) for y in zip(zero, x)] for x in [[0,1], [0,-1], [1,0], [-1,0]]]
# 		for pos in pos_lst:
# 			if all(map(lambda x: x < self.size and x >= 0, pos)):
# 				new_map = list([list(row) for row in self.n_map])
# 				new_map[zero[0]][zero[1]], new_map[pos[0]][pos[1]] =  new_map[pos[0]][pos[1]], new_map[zero[0]][zero[1]]
# 				yield State(tuple(tuple(row) for row in new_map), self.g_val + 1, self, self.h_fn, self.goal)

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