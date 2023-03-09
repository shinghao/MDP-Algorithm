''' Algo to find shortest traveling path '''

# Feed a set of destination coordinates and (direction) orientation
# This first processing layer determines the order of visiting 

# Considerations #
# Consider the arc + straight line distance? - Diagonal movements?
# Consider the robot's orientation in start & end state?
# Consider obstacles and boundaries that inhibits robot movement?

#---------------------- PACKAGES
import math
import copy
from griddyworld import *
from typing import List
from heuristics import euc_dist
from pathfinder import astar
import itertools

#------------------------------------------------------ CLASSES

INF = float('Inf') # positive infinity

#------------------------------------------------------ FUNCTIONS

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


# usage: pathfound = astar(bot,goal)

def connect_graph(bot, visit: List[node], start: node, obstacles: List[obstacle]):
	''' "visit" should be the positional nodes that the robot needs to visit in the graph '''
	# adjacency matrix

	nodes = [start] + visit
	adjM = [[None for i in range(0, len(nodes))] for j in range(0, len(nodes))]	

	# it's NO LONGER solving some problems twice (since we can take reverse of A-B to find B-A)
	i = 0
	for edges in adjM:
		j = 1 # we skip first index because it's just the start node
		for edge in range(0, len(visit)):
			bot.move(nodes[i])
			if not nodes[i] == nodes[j]: # DON'T NEED SOLUTION TO ITSELF
				if adjM[j][i]: adjM[i][j] = adjM[j][i].reverse_path()
				else: adjM[i][j] = astar(bot, nodes[j], obstacles)

			j+=1
		i += 1

	return adjM

def permutate(graph):
	# number of nodes to visit
	tovisit = list(range(1, len(graph[0])))
	permutations = list(itertools.permutations(tovisit))
	# print(tovisit)
	# print(permutations)

	mincost = INF
	minpath = None

	illegal = list() # new check to see if any goal states cannot be visited by algo (no solution)

	for permutation in permutations:
		index = 0 # always start from zero
		pathcost = 0
		route = list()
		try: 
			for goto in permutation:
				
				if goto not in illegal and not graph[index][goto]: # no solution
					illegal.append(goto)
					print("ILLEGAL OBSTACLE DETECTED - IGNORING OBSTACLE %s" %goto)

				if index not in illegal and goto not in illegal:
					pathcost += graph[index][goto].cost
					route.append(graph[index][goto])
					index = goto

				else: continue # do nothing, no path will be added to try and reach this illegal state

			if pathcost < mincost:
				mincost = pathcost
				minpath = route

			#print(pathcost)
			
		except:
			#print("index is %s and goto is %s" % (index, goto))
			raise Exception("SOMETHING WENT WRONG, PLEASE CHECK YOUR CODE")

	return minpath

# testing #

if __name__ == '__main__':
	n1,n2,n3 = node(pair(2,3), pair(0,1)), node(pair(8,8), pair(-1,0)), node(pair(17,4), pair(1,0))
	s1 = node(pair(1,1), pair(0,1))
	l1 = list((n1,n2,n3))

	bot = robot(s1, 3)
	graph = connect_graph(bot, l1, s1)

	route = permutate(graph)

	print(route)

	# for edges in graph:
	# 	for edge in edges:
	# 		if edge: print([node.get() for node in edge.nodes])
	# 		if edge: print(edge.moves)
	# 		if edge: print(edge.cost)