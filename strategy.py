from griddyworld import *

from pathfinder import naive, astar

from heuristic import doppelganger

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

def astar_TSP(bot, nodes, obstacles, alt = False):
	# nodes should be a list of list: list of possible goal states for every obstacle

	# alt allows you to execute upgraded astar -> allowing it to access alternate goal states
	start = bot.pos

	print("Connecting the graphs using A-star to weigh edges")

	graph = pathorder.connect_graph(bot, nodes, start, obstacles)

	route = pathorder.permutate(graph)

	obstacle_order = list()

			
	for r in route:
		goal = r.last()
		print(goal.get())
		o_coords = goal.grid + (goal.direction)*3

		for o in obstacles:
			if o.pos.grid == o_coords:
				obstacle_order.append(o)
				break

	if alt:
		newroute = list()
		
		for r in route:
			goal = r.last()

			if not doppelganger(goal, obstacles):
				newroute.append(astar(bot, goal, obstacles, alt))

			else:
				newroute.append(r)

		return newroute, obstacle_order


	return route, obstacle_order


# TESTING #

if __name__ == '__main__':

	start = node(pair(2,2), pair(0,1))

	test = node(pair(9,8), pair(0,1))

	obstacles = random_obstacles(3)

	print(obstacles)

	# # TOY EXAMPLE #

	# obstacles = [(12, 5, (0, 1)), (16, 4, (0, -1)), (15, 12, (-1, 0)), (9, 16, (0, -1)), (8, 1, (0, 1)), (6, 15, (-1, 0)), (5, 10, (1, 0)), (2, 7, (0, 1))]
	
	obstacles = [obstacle(i+1, node(pair(v[0], v[1]), pair(*(v[2])))) for i, v in enumerate(obstacles)]

	# start = node(pair(9,6), pair(0,1))

	#obstacles = [obstacle(node(pair(7,16), pair(1,0)))]

	# # # #
	
	nodes = [o.goal_state() for o in obstacles]

	bot = robot(start, 3)

	# astar(bot, node(pair(16,1), pair(0,1)), obstacles)

	#route = hpath_astar(bot, nodes, start)

	route, obstacle_order = astar_TSP(bot, nodes, obstacles)

	for r in route:
		r.print_path()

	print([(o.ID, o.pos.get()) for o in obstacle_order])