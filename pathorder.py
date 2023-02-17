''' Algo to find shortest traveling path '''

# Feed a set of destination coordinates and (direction) orientation
# This first processing layer determines the order of visiting 

# Considerations #
# Consider the arc + straight line distance? - Diagonal movements?
# Consider the robot's orientation in start & end state?
# Consider obstacles and boundaries that inhibits robot movement?

#---------------------- PACKAGES
import math
import random
import copy
from griddyworld import *
from typing import List

#------------------------------------------------------ CLASSES

INF = float('Inf') # positive infinity

#------------------------------------------------------ FUNCTIONS

def euc_dist(a:tuple,b:tuple):
	''' Euclidean Distance
	Finds the straight line distance between two points
	Inputs: a,b where a and b are coordinate sets of the two points
	Output: Straight line distance in (cm)
	'''
	straight_line_dist = math.sqrt(pow(b[0]-a[0], 2) + pow(b[1]-a[1], 2))
	return straight_line_dist

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

def greedy(nodes: List[node], start: tuple):
	''' we can simply take the shortest path at each step '''
	visit = copy.deepcopy(nodes)
	index = 0
	shortest = INF
	i = 0
	route = list()

	while visit:
		for n in visit:
			d = euc_dist(start, n.grid.get())
			if d < shortest:
				shortest = d
				index = i
			i += 1

		route.append(visit[index])
		start = visit[index].grid.get()
		del visit[index]
		index = 0
		i = 0
		shortest = INF

	return(route)
			

def djikstra(nodes):
	''' we can use djikstra to find the node visitation order '''
	visited = [0 for i in range(0, len(nodes))] # set all nodes as unvisited
	print(visited)

