from griddyworld import *
from typing import List
import math

def euc_dist(a:tuple,b:tuple):
	''' Euclidean Distance
	Finds the straight line distance between two points
	Inputs: a,b where a and b are coordinate sets of the two points
	Output: Straight line distance in (cm)
	'''
	straight_line_dist = math.sqrt(pow(b[0]-a[0], 2) + pow(b[1]-a[1], 2))
	return straight_line_dist

def costing(f):
	if f.__name__ == 'left' or f.__name__ == 'backleft':
		return 6

	elif f.__name__ == 'right' or f.__name__ == 'backright':
		return 8

	else: return 1

def doppelganger(goal: node, obstacles: List[obstacle], allowance = 2):
	''' This function checks if an obstacle has a nearby obstacle with the same orientation (returns True)
		Else, returns false (no doppelganger => save to consider alternate goal state position)'''

	for o in obstacles:
		check = o.goal_state()
		if check == goal:
			continue # this is the obstacle for this goal state

		if check.direction == goal.direction: # only worth to continue if goal states are facing same side
			if goal.grid.x - allowance <= check.grid.x <= goal.grid.x + allowance:
				return True

			elif goal.grid.y - allowance <= check.grid.y <= goal.grid.y + allowance:
				return True

	return False

def alt_goal_states(goal: node):
	''' This function checks for alternative goal states that robot can land on as well
		This should ease pathfinding and make algo more efficient as well'''
	x,y = goal.grid.get()
	ori = goal.direction.get()

	if ori in [N,S]:
		goals = [node(pair(x-1,y), pair(*ori)), goal, node(pair(x+1,y), pair(*ori))] # side positions are fine too
		for i in range(0, len(goals)):
			goal = goals[i]
			x,y = goal.grid.get()
			if ori == N: offset = -1
			else: offset = 1
			goals.append(node(pair(x,y+offset), pair(*ori))) # 1 tile behind is fine - further from obstacle


	elif ori in [E,W]:
		goals = [node(pair(x,y-1), pair(*ori)), goal, node(pair(x,y+1), pair(*ori))] # side positions are fine too
		for i in range(0, len(goals)):
			goal = goals[i]
			x,y = goal.grid.get()
			if ori == E: offset = -1
			else: offset = 1
			goals.append(node(pair(x + offset, y), pair(*ori))) # 1 tile behind is fine - further from obstacle

	else: raise Exception("Illegal goal state orientation detected: %s" % ori)
	
	return goals

# TESTING #

test = node(pair(17,4), pair(*W))

for g in alt_goal_states(test):
	print(g.get())



# UNUSED #

def man_dist(a,b):
	''' Manhattan distance
	Similar to euclidean distance, but here we find the shortest distance using points/axes measured at right angles.
	'''
	pass

def rel_ori(start:node, dest: node):
	''' get relative orientation : gives us direction of destination node relative to reference node '''
	Y = dest.y - start.y
	X = dest.x - start.x

	radians = math.atan2(Y, X)
	return math.degrees(radians)

def perspective(start: node, angle):
	''' changes the relative angle based on the orientation of the node - all nodes should appear north facing '''
	if start.z == E:
		if angle > 0: return angle - 90
		elif angle < -90: return 360 + angle - 90
		else: return angle - 90

	elif start.z == W:
		if angle < 0: return angle + 90
		elif angle > 90: return 360 - angle - 90
		if angle < 90: return angle + 90
		else: return -90 - (180 - angle)

	elif start.z == S:
		if angle > 0: return angle - 180
		else: return angle + 180

	else: return angle # original was north facing

# incomplete #
def weigh(start: node, dest: node):
	'''
	find cost of a node relative to starting position. also accounts for orientation
	'''
	t_cost = 0.5 # arbitrary turning factor cost
	ori = rel_ori(start, dest)
	perspective(start, ori)

	if start.z == dest.z:
		t_cost *= ori # best case is straight ahead, worst case is 180 behind

	elif start.z: pass
	return euc_dist((start.x,start.y), (dest.x,dest.y))