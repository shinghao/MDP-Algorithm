from griddyworld import *

from pathfinder import naive, astar

import pathorder

def hpath_astar(bot, nodes, start):
	order = pathorder.greedy(nodes, start.grid.get())

	print("Node visitation order:")

	for g in order:
		print(g.get())

	route = list()

	for goal in order:
		pathfound = astar(bot, goal)
		route.append(pathfound)
		print(pathfound.get())
		print(pathfound.get_moves())
		start = goal

	return route

def astar_TSP(bot, nodes, start):

	graph = pathorder.connect_graph(bot, nodes, start)

	route = pathorder.permutate(graph)

	return route


# TESTING #

if __name__ == '__main__':

	start = node(pair(1,1), pair(0,1))

	test = node(pair(9,8), pair(0,1))

	obstacles = random_obstacles(8)

	print(obstacles)

	nodes = [node(pair(i[0], i [1]), pair(*(i[2]))) for i in obstacles]

	bot = robot(start, 3)

	#route = hpath_astar(bot, nodes, start)

	route = astar_TSP(bot, nodes, start)

	for r in route:
		r.print_path()