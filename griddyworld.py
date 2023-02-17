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
		self.cost = cost # cost of path

	def add(self, newnode:node):
		self.nodes.append(newnode)
		self.cost += 1 # placeholder cost

	def __add__(self, path2):
		return path(self.nodes + path2.nodes, self.cost + path2.cost, self.moves + path2.moves)
	
	def add_move(self, move: str):
		self.moves.append(move)

	def get_moves(self):
		return self.moves

	def compute_cost(self):
		pass

	def print_path(self):
		for n in self.nodes:
			print(n.get())

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

def random_obstacles(n):

	obstacles = list()
	selected = list()
	
	for i in range (0,n):

		new = False

		while not new:
			x = random.choice(range(1,21))
			y = random.choice(range(1,21))
			z = random.choice([N,E,S,W])
			if (x,y) not in selected:
				selected.append((x,y))
				obstacles.append((x,y,z))
				new = True
	
	return obstacles