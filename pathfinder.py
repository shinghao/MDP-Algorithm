import math

N,E,S,W = (0,1), (1,0), (0,-1), (-1,0)

START = (1,1)

O1 = (4,4)

GRID_X, GRID_Y = 20, 20

class pair:

	def __init__(self, x, y):
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

	def __init__(self, nodes = None, cost = 0):
		self.nodes = list() # list of nodes
		if nodes: self.nodes += nodes # populate list with argument
		self.cost = cost # cost of path

	def add(self, newnode:node):
		self.nodes.append(newnode)
		self.cost += 1 # placeholder cost

	def __add__(self, path2):
		return path(self.nodes + path2.nodes, self.cost + path2.cost)
		
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

	def rbsg(self, start, goal):
		# RANDOM BULLSHIT GO -> BFS

		explore = list()
		p = path()
		p.add(start)
		explore.append(p)
		self.move(start)

		while explore:
			for p in explore:
				for f in [self.forward, self.back, self.left, self.right, self.backleft, self.backright]:
					self.move(p.last())
					newnode = f()
					if not self.oob(newnode.grid):
						print(p.get())
						new_p = path() + p # copy old path
						new_p.add(newnode)
						if new_p.last().get() == goal.get():
							print("FOUND GOAL")
							return new_p

						else:
							explore.append(new_p)

					else: continue

				explore.remove(p) # remove object from list by reference
			# try a new path

# djikstra - idea to do it before i forget:
''' populate statespace and then solve shortest path to every node until goal state found
	20 * 20 means 400 possible positions and 4 orientations mean 1600 possible states
	this means computation shouldn't be too bad hopefully.
'''
