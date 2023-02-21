from griddyworld import *

from pathfinder import naive, astar

import pathorder

def hpath_astar(bot, nodes):
	start = bot.pos
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

def astar_TSP(bot, nodes, obstacles):

	start = bot.pos

	print("Connecting the graphs using A-star to weigh edges")

	graph = pathorder.connect_graph(bot, nodes, start, obstacles)

	route = pathorder.permutate(graph)

	obstacle_order = list()

	for r in route:
		goal = r.last()
		print(goal.get())
		o = goal.grid + (goal.direction)*3
		obstacle_order.append(o)

	return route, obstacle_order


# TESTING #

if __name__ == '__main__':

	start = node(pair(2,2), pair(0,1))

	test = node(pair(9,8), pair(0,1))

	obstacles = random_obstacles(3)

	print(obstacles)

	# obstacles = [obstacle(node(pair(i[0], i [1]), pair(*(i[2])))) for i in obstacles]

	# # TOY EXAMPLE #

	# obstacles = [(12, 5, (0, 1)), (16, 4, (0, -1)), (15, 12, (-1, 0)), (9, 16, (0, -1)), (8, 1, (0, 1)), (6, 15, (-1, 0)), (5, 10, (1, 0)), (2, 7, (0, 1))]
	
	obstacles = [obstacle(node(pair(i[0], i [1]), pair(*(i[2])))) for i in obstacles]

	# start = node(pair(9,6), pair(0,1))

	#obstacles = [obstacle(node(pair(7,16), pair(1,0)))]

	# # # #
	
	nodes = [o.relative_ori() for o in obstacles]

	bot = robot(start, 3)

	# astar(bot, node(pair(16,1), pair(0,1)), obstacles)

	#route = hpath_astar(bot, nodes, start)

	route, obstacle_order = astar_TSP(bot, nodes, obstacles)

	for r in route:
		r.print_path()

	print([o.get() for o in obstacle_order])