from typing import List
from Constants import N, E, S, W, GRID_NUM

START = (2,2)

O1 = (4, 4)

GRID_X, GRID_Y = GRID_NUM, GRID_NUM

# ROBOT ACTUAL HARDWARE CONFIGURATION #
# self.F_LEFT = pair(-turning, turning)
# self.F_RIGHT = pair(turning, turning)
# self.B_LEFT = pair(-turning, -turning)
# self.B_RIGHT = pair(turning, -turning)

F_LEFT = (-4, 2)
B_LEFT = (-4, -2)
F_RIGHT = (5, 3)
B_RIGHT = (5, -3)


class pair:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):  # moving grids - single point
        return pair(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return pair(self.x - other.x, self.y - other.y)

    def __mul__(self, constant: int):  # for direction vectors
        return pair(self.x*constant, self.y*constant)

    def __rshift__(self, other):
        return pair(self.x * other.x, self.y * other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get(self):
        return self.x, self.y

    def flip(self):
    	return pair(self.y, self.x)


class node:

    def __init__(self, grid: pair, direction: pair):
        self.grid = grid  # pair type
        self.direction = direction  # pair type

    def get(self):
        return (self.grid.x, self.grid.y), (self.direction.x, self.direction.y)


class path:

    def __init__(self, nodes=None, cost=0, moves=None):
        self.nodes = list()  # list of nodes
        if nodes:
            self.nodes += nodes  # populate list with argument

        self.moves = list()  # list of moves
        if moves:
            self.moves += moves

        self.cost = cost  # cost of path or g() cost
        self.hcost = 0  # heuristic cost - let this be 0 if there is none

    def __add__(self, path2):
        return path(self.nodes + path2.nodes, self.cost + path2.cost, self.moves + path2.moves)

    def __lt__(self, path2):
        '''use this to compare and sort paths for the heap queue'''
        return self.cost + self.hcost < path2.cost + path2.hcost

    def add(self, newnode: node):
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
                raise Exception(
                    "instruction received in wrong format, cannot reverse.")
        return reverse

    def reverse_path(self):
        return path(self.nodes[::-1], self.cost, self.reverse_moves())

    def print_path(self):
        print("path taken:", [n.get() for n in self.nodes])
        print("moves used:", [m for m in self.moves])
        print("cost:", self.cost)

    def get(self):
        return [n.get() for n in self.nodes]

    def last(self):
        return self.nodes[-1]  # last node visited on path


class obstacle:
    def __init__(self, ID: int, pos):
        self.ID = ID
        self.pos = pos  # node type

    def get_pos(self):
        return self.pos

    def get_xy_coord(self):
        return self.pos.get()[0]

    def get_ID(self):
        return self.ID

    def block(self, grid):
        if abs(grid.x - self.pos.grid.x) <= 1 and \
                abs(grid.y - self.pos.grid.y) <= 1:
            # if difference is less than 1
            return True
        else:
            return False

    def relative_ori(self, dist=3):
        ''' get the relative orientation the robot needs to be in
        to scan the image on the obstacle'''
        # how to handle outofbounds?

        if self.pos.direction.get() == N:
            goto = self.pos.grid + pair(0, dist)
            orientation = pair(*S)
            return node(goto, orientation)

        elif self.pos.direction.get() == S:
            goto = self.pos.grid + pair(0, -dist)
            orientation = pair(*N)
            return node(goto, orientation)

        elif self.pos.direction.get() == E:
            goto = self.pos.grid + pair(dist, 0)
            orientation = pair(*W)
            return node(goto, orientation)

        elif self.pos.direction.get() == W:
            goto = self.pos.grid + pair(-dist, 0)
            orientation = pair(*E)
            return node(goto, orientation)

        else:
            raise Exception(
                "Obstacle orientation error - only N,S,E,W are allowed.")


class robot:

    def __init__(self, pos:node = None, F_LEFT:pair = None, F_RIGHT:pair = None, B_LEFT:pair = None, B_RIGHT:pair = None, turning=3):
        self.pos = pos

        # ideal case is same turning radius, use this to adjust all turning aspects
        if F_LEFT and F_RIGHT and B_LEFT and B_RIGHT:
        	self.F_LEFT = F_LEFT
	        self.F_RIGHT = F_RIGHT
	        self.B_LEFT = B_LEFT
	        self.B_RIGHT = B_RIGHT
        else:
	        self.F_LEFT = pair(-turning, turning)
	        self.F_RIGHT = pair(turning, turning)
	        self.B_LEFT = pair(-turning, -turning)
	        self.B_RIGHT = pair(turning, -turning)

    def move(self, new_pos):
        self.pos = new_pos

    def config_turning(self, F_LEFT : pair, F_RIGHT: pair, B_LEFT: pair, B_RIGHT: pair):
        self.F_LEFT = F_LEFT
        self.F_RIGHT = F_RIGHT
        self.B_LEFT = B_LEFT
        self.B_RIGHT = B_RIGHT

    def perspective(self, turn):
        ''' translates turning vector into one that matches the current perspective of the robot
			e.g. turning left while facing north vs turning left while facing south from the same                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   grid will yield different destinations
        '''

        if self.pos.direction.get() == N:
            if turn == 'left':
                return self.F_LEFT, W
            if turn == 'right':
                return self.F_RIGHT, E
            if turn == 'backleft':
                return self.B_LEFT, E
            if turn == 'backright':
                return self.B_RIGHT, W

        elif self.pos.direction.get() == S:
            if turn == 'left':
                return self.F_LEFT >> pair(-1, -1), E
            if turn == 'right':
                return self.F_RIGHT >> pair(-1, -1), W
            if turn == 'backleft':
                return self.B_LEFT >> pair(-1, -1), W
            if turn == 'backright':
                return self.B_RIGHT >> pair(-1, -1), E

        elif self.pos.direction.get() == E:
            if turn == 'left':
                return (self.F_LEFT >> pair(-1, 1)).flip(), N
            if turn == 'right':
                return (self.F_RIGHT >> pair(-1, 1)).flip(), S
            if turn == 'backleft':
                return (self.B_LEFT >> pair(-1, 1)).flip(), S
            if turn == 'backright':
                return (self.B_RIGHT >> pair(-1, 1)).flip(), N

        elif self.pos.direction.get() == W:
            if turn == 'left':
                return (self.F_LEFT >> pair(1, -1)).flip(), S
            if turn == 'right':
                return (self.F_RIGHT >> pair(1, -1)).flip(), N
            if turn == 'backleft':
                return (self.B_LEFT >> pair(1, -1)).flip(), N
            if turn == 'backright':
                return (self.B_RIGHT >> pair(1, -1)).flip(), S

        else:
            raise Exception(
                "illegal robot orientation - please only use N,S,E,W")

    def forward(self, dist=1):
        return node(self.pos.grid + self.pos.direction*dist, self.pos.direction)

    def back(self, dist=1):
        return node(self.pos.grid - self.pos.direction*dist, self.pos.direction)

    def left(self):
        turn, ori = self.perspective('left')
        return node(self.pos.grid + turn, pair(*ori))

    def right(self):
        turn, ori = self.perspective('right')
        return node(self.pos.grid + turn, pair(*ori))

    def backleft(self):
        turn, ori = self.perspective('backleft')
        return node(self.pos.grid + turn, pair(*ori))

    def backright(self):
        turn, ori = self.perspective('backright')
        return node(self.pos.grid + turn, pair(*ori))

    def controls(self):
        return self.forward, self.back, self.left, self.right, self.backleft, self.backright

    def tight_oob(self, grid):
        ''' strict out of bounds check '''
        for i in [-1, 0, 1]:  # use this if  don't want robot to go near bounds
            if not (0 < grid.x + i <= GRID_X):
                return True
            elif not (0 < grid.y + i <= GRID_Y):
                return True

        return False

    def oob(self, grid):
        ''' check if a grid is out of bounds '''
        if not 0 < grid.x <= GRID_X:
            return True
        elif not 0 < grid.y <= GRID_Y:
            return True

        return False

    def check_obstacle(self, checkthis: pair, obstacles: List[obstacle]):
        # print(f"checking for obstacle at {checkthis.get()}")

        for o in obstacles:
            if o.block(checkthis):
                # print("obstacle detected")
                return True

        return False

    def turning_clear(self, movement, obstacles):
    	dest = movement()
    	if movement.__name__ == 'left':
    		turn, ori  = self.perspective('left')
    	elif movement.__name__ == 'right':
    		turn, ori  = self.perspective('right')
    	elif movement.__name__ == 'backleft':
    		turn, ori  = self.perspective('backleft')
    	elif movement.__name__ == 'backright':
    		turn, ori  = self.perspective('backright')
    	else: raise Exception("illegal move found while checking turn: %s" % movement.__name__)

    	# print(turn.get(), ori)

    	# IF ORIENTATION IS N,S : CHECK ALONG Y AXIS THEN X; ELSE CHECK X THEN Y

    	if self.pos.direction.get() in [N,S]:
    		vertical,horizontal = turn.y, turn.x
    		if vertical >= 0: offset1 = pair(0,1)
    		else: offset1 = pair(0, -1)
    		if horizontal >= 0: offset2 = pair(1,0)
    		else: offset2 = pair(-1, 0)

    	elif self.pos.direction.get() in [E,W]:
    		vertical, horizontal = turn.x, turn.y
    		if vertical >= 0: offset1 = pair(1,0)
    		else: offset1 = pair(-1, 0)
    		if horizontal >= 0: offset2 = pair(0,1)
    		else: offset2 = pair(0, -1)

    	else: raise Exception("robot found in illegal orientation: %s" % self.pos.direction)

    	# print(vertical, horizontal, offset1.get(), offset2.get())

    	# DO OBSTACLE 3X3 CHECK FOR EVERY GRID TRAVELED HORIZONTALLY AND VERTICALLY (DOESN'T ACCOUNT FOR DIAGONAL)

    	current = self.pos.grid # remember location to simulate movement

    	for i in range(1, abs(vertical)+1):
    		current += offset1
    		# print(f"Checking {current.get()} for obstacles")
    		if self.check_obstacle(current, obstacles): return False # turning cannot be done
    		#print("Clear.")

    	# CHECK THE OFF-ANGLE DURING THE TURN:
    	# print(f"Checking {(current-offset1+offset2).get()} for obstacles")
    	if self.check_obstacle(current-offset1+offset2, obstacles): return False # turning cannot be done
    	# print("Clear.")

    	for j in range(1, abs(horizontal)+1):
    		current += offset2
    		# print(f"Checking {current.get()} for obstacles")
    		if self.check_obstacle(current, obstacles): return False # turning cannot be done
    		# print("Clear.")

    	return True # above checks pass, turning can be made

    ### THIS IS ONLY USABLE IF TURNING IS SYMMETRIC (I.E. SAME X AND Y TRAVELED ON TURNS) ###
    # def turning_clearance(self, movement, obstacle_list, mult=2):
    #     ''' movement here is the function call (use for turning only)
    #     mult is degree of clearance, higher number means more restrictive turns but higher clearing
    #     mult specifies the amount of room "above" the turning diagonal to clear'''

    #     dest = movement()  # returns destination node

    #     # OFFSET helps us check the correct side of the diagonal when clearing the turn
    #     if movement.__name__ in ['left', 'right']:
    #         offset = pair(1, 1)

    #     elif movement.__name__ in ['backleft', 'backright']:
    #         offset = pair(-1, -1)

    #     else:
    #         raise Exception(
    #             "invalid turning movement format, valid turning formats are left, right, backleft, backright")

    #     # print(dest.get())
    #     displacement = dest.grid - self.pos.grid  # how much we have moved

    #     if displacement.x >= 0:
    #         horizontal = 1
    #     else:
    #         horizontal = -1

    #     if displacement.y >= 0:
    #         vertical = 1
    #     else:
    #         vertical = -1

    #     # therefore to move along the diagonal, we should move
    #     xy = pair(horizontal, vertical)

    #     # boundaries for checking
    #     if self.pos.grid.x <= dest.grid.x:
    #         lower_x, upper_x = self.pos.grid.x, dest.grid.x
    #     else:
    #         upper_x, lower_x = self.pos.grid.x, dest.grid.x

    #     if self.pos.grid.y <= dest.grid.y:
    #         lower_y, upper_y = self.pos.grid.y, dest.grid.y
    #     else:
    #         upper_y, lower_y = self.pos.grid.y, dest.grid.y

    #     # print(lower_x, upper_x, lower_y, upper_y)

    #     checkthis = self.pos.grid

    #     # check along diagonal and grids in the direction of the robot's current orientation (depending on mult)

    #     while checkthis != dest.grid:
    #         # do this for every grid along the diagonal
    #         # check grid above diagonal ONLY for now - previous versions too strict, can't turn
    #         for i in range(0, mult+1):
    #             checking = checkthis + (self.pos.direction >> offset)*i
    #             if lower_x <= checking.x <= upper_x and lower_y <= checking.y <= upper_y:
    #                 if self.check_obstacle(checking, obstacle_list):
    #                     # turn is illegal
    #                     return False

    #             else:
    #                 continue  # not in scope of check, continue.

    #         # move along the diagonal
    #         checkthis += xy

    #     if self.check_obstacle(dest.grid, obstacle_list):
    #         return False  # check if destination is clear

    #     return True  # all checks passed - turn can be made


# TESTING #
if __name__ == '__main__':

    test1 = node(pair(1, 1), pair(0, 1))
    test2 = node(pair(4, 4), pair(1, 0))
    path1 = path([test1], 1)
    path2 = path([test2], 6, ['right'])

    # path3 = path1 + path2

    # path3.print_path()

    # path3.reverse_path().print_path()

    start = node(pair(5, 5), pair(1,0))

    bot = robot(start, F_LEFT = pair(*F_LEFT), F_RIGHT = pair(*F_RIGHT), B_LEFT = pair(*B_LEFT), B_RIGHT = pair(*B_RIGHT))

    #bot.move(bot.backleft())

    print(bot.pos.get())

    O1 = node(pair(8,7), pair(-1, 0))

    obstacle_list = [obstacle(1, O1)]

    # print(bot.right().get())

    print(bot.turning_clear(bot.backright, obstacle_list))

    #bot.turning_clearance(bot.backleft, obstacle_list)