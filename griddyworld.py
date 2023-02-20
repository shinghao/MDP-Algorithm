import math
import random

N,E,S,W = (0,1), (1,0), (0,-1), (-1,0)

START = (1,1)

O1 = (4,4)

GRID_X, GRID_Y = 20, 20

class pair:

	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def __add__(self, other): # moving grids - single point
		return pair(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return pair(self.x - other.x, self.y - other.y)

	def __mul__(self, constant): # for direction vectors
		return pair(self.x*constant, self.y*constant)

	def get(self):
		return self.x, self.y

class node:

	def __init__(self, grid: pair, direction: pair):
		self.grid = grid # pair type
		self.direction = direction # pair type

	def get(self):
		return (self.grid.x, self.grid.y), (self.direction.x, self.direction.y)

class path:

	def __init__(self, nodes = None, cost = 0, moves = None):
		self.nodes = list() # list of nodes
		if nodes: self.nodes += nodes # populate list with argument

		self.moves = list() # list of moves
		if moves: self.moves += moves

		self.cost = cost # cost of path or g() cost
		self.hcost = 0 # heuristic cost - let this be 0 if there is none

	def __add__(self, path2):
		return path(self.nodes + path2.nodes, self.cost + path2.cost, self.moves + path2.moves)

	def __lt__(self, path2):
		'''use this to compare and sort paths for the heap queue'''
		return self.cost + self.hcost < path2.cost + path2.hcost

	def add(self, newnode:node):
		self.nodes.append(newnode)

	def add_cost(self, cost: int):
		self.cost += cost

	def update_hcost(self, hcost):
		self.hcost = hcost
	
	def add_move(self, move):
		# note that move should be a function
		self.moves.append(move.__name__)

	def get_moves(self):
		return self.moves

	def reverse_moves(self):
		reverse = list()
		for move in self.moves[::-1]:
			if move == 'forward':
				reverse.append('back')
			elif move == 'back':
				reverse.append('forward')
			elif move == 'left':
				reverse.append('backleft')
			elif move == 'right':
				reverse.append('backright')
			elif move == 'backleft':
				reverse.append('left')
			elif move == 'backright':
				reverse.append('right')
			else:
				raise Exception("instruction received in wrong format, cannot reverse.")
		return reverse

	def reverse_path(self):
		return path(self.nodes[::-1], self.cost, self.reverse_moves())

	def print_path(self):
		print("path taken:", [n.get() for n in self.nodes])
		print("moves used:", [m for m in self.moves])
		print("cost:",self.cost)

	def get(self):
		return [n.get() for n in self.nodes]

	def last(self):
		return self.nodes[-1] # last node visited on path

class obstacle:
	def __init__(self, pos):
		self.pos = pos # node type

	def block(self, grid):
		if abs(grid.x - self.pos.grid.x) <= 1 or \
			abs(grid.y - self.pos.grid.y) <= 1:
			# if difference is less than 1
			return True
		else: return False

	def relative_ori(self):
		''' get the relative orientation the robot needs to be in
		to scan the image on the obstacle'''
		# how to handle outofbounds?

		if self.pos.direction.get() == N:
			goto = self.pos.grid + pair(0,3)
			orientation = pair(*S)
			return node(goto, orientation)

		elif self.pos.direction.get() == S:
			goto = self.pos.grid + pair(0,-3)
			orientation = pair(*N)
			return node(goto, orientation)

		elif self.pos.direction.get() == E:
			goto = self.pos.grid + pair(3,0)
			orientation = pair(*W)
			return node(goto, orientation)

		elif self.pos.direction.get() == W:
			goto = self.pos.grid + pair(-3,0)
			orientation = pair(*E)
			return node(goto, orientation)

		else:
			raise Exception("Obstacle orientation error - only N,S,E,W are allowed.")

class robot:
	pos = None # node type
	turning = 3 # T grids to turn

	def __init__(self, pos, turning):
		self.pos = pos
		self.turning = turning

	def move(self, new_pos):
		self.pos = new_pos

	def forward(self, dist=1):
		return node(self.pos.grid + self.pos.direction*dist, self.pos.direction)

	def back(self, dist=1):
		return node(self.pos.grid - self.pos.direction*dist, self.pos.direction)

	def left(self):

		T = self.turning

		if self.pos.direction.get() == N:
			return node(self.pos.grid + pair(-T,T), pair(*W))

		elif self.pos.direction.get() == S:
			return node(self.pos.grid + pair(T,-T), pair(*E))

		elif self.pos.direction.get() == E:
			return node(self.pos.grid + pair(T,T), pair(*N))

		elif self.pos.direction.get() == W:
			return node(self.pos.grid + pair(-T,-T), pair(*S))
		else:
			raise Exception("undefined behaviour")

	def right(self):

		T = self.turning

		if self.pos.direction.get() == N:
			return node(self.pos.grid + pair(T,T), pair(*E))

		elif self.pos.direction.get() == S:
			return node(self.pos.grid + pair(-T,-T), pair(*W))

		elif self.pos.direction.get() == E:
			return node(self.pos.grid + pair(T,-T), pair(*S))

		elif self.pos.direction.get() == W:
			return node(self.pos.grid + pair(-T,T), pair(*N))
		else:
			raise Exception("undefined behaviour")

	def backleft(self):

		T = self.turning

		if self.pos.direction.get() == N:
			return node(self.pos.grid + pair(-T,-T), pair(*E))

		elif self.pos.direction.get() == S:
			return node(self.pos.grid + pair(T,T), pair(*W))

		elif self.pos.direction.get() == E:
			return node(self.pos.grid + pair(-T,T), pair(*S))

		elif self.pos.direction.get() == W:
			return node(self.pos.grid + pair(T,-T), pair(*N))
		else:
			raise Exception("undefined behaviour")

	def backright(self):

		T = self.turning

		if self.pos.direction.get() == N:
			return node(self.pos.grid + pair(T,-T), pair(*W))

		elif self.pos.direction.get() == S:
			return node(self.pos.grid + pair(-T,T), pair(*E))

		elif self.pos.direction.get() == E:
			return node(self.pos.grid + pair(-T,-T), pair(*N))

		elif self.pos.direction.get() == W:
			return node(self.pos.grid + pair(T,T), pair(*S))
		else:
			raise Exception("undefined behaviour")

	def controls(self):
		return self.forward, self.back, self.left, self.right, self.backleft, self.backright

	def tight_oob(self, grid):
		''' strict out of bounds check '''
		for i in [-1,0,1]: # use this don't want robot to go near bounds
			if not 0 < grid.x + i <= GRID_X:
				return True
			elif not 0 < grid.y + i <= GRID_Y:
				return True

			return False

	def oob(self, grid):
		''' check if a grid is out of bounds '''
		if not 0 < grid.x <= GRID_X:
			return True
		elif not 0 < grid.y <= GRID_Y:
			return True

		return False

	def check_obstacle(self):
		pass

	def turning_clearance(self, movement):
		''' movement here is the function call (use for turning only) '''
		dest = movement() # returns destination node
		displacement = dest.grid - self.pos.grid # how much we have moved

		if displacement.x >= 0: horizontal = 1
		else: horizontal = -1

		if displacement.y >= 0: vertical = 1
		else: vertical = -1

		# cases by orientation:
		if movement.__name__ == 'left':
			pass

		elif movement.__name__ == 'right':
			pass

		elif movement.__name__ == 'backleft':
			pass
 
		elif movement.__name__ == 'backright':
			pass

		else:
			raise Exception("turning clearance is only for turning movements!")

		# find diagonal


def random_obstacles(n):

	obstacles = list()
	selected = list()
	
	for i in range (0,n):

		new = False

		while not new:
			x = random.choice(range(1,GRID_X))
			y = random.choice(range(1,GRID_Y))
			z = random.choice([N,E,S,W])
			if (x,y) not in selected:
				selected.append((x,y))
				check = pair(x,y) + pair(*z)*3
				if not 0 < check.x <= 20 or not 0 < check.y <= 20:
					# this obstacle is illegal
					continue
				else:
					obstacles.append((x,y,z))
					new = True
	
	return obstacles


# TESTING #
if __name__ == '__main__':
	test1 = node(pair(1,1), pair(0,1))
	test2 = node(pair(4,4), pair(1,0))
	path1 = path([test1], 1)
	path2 = path([test2], 6, ['right'])

	path3 = path1 + path2

	path3.print_path()

	path3.reverse_path().print_path()