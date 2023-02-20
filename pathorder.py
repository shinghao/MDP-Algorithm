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

def connect_graph(nodes: List[node], start: node):
	''' nodes should be the positional nodes that the robot needs to visit in the graph '''
	# adjacency matrix
	
	edges = [[0 for i in range(0, len(nodes)+1)] for j in range(0, len(nodes)+1)]


	print(edges)


# testing #

if __name__ == '__main__':
	n1,n2,n3 = node(pair(2,3), pair(0,1)), node(pair(8,8), pair(-1,0)), node(pair(17,4), pair(1,0))
	s1 = node(pair(1,1), pair(0,1))
	l1 = list((n1,n2,n3))
	connect_graph(l1, s1)