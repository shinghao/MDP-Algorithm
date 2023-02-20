from griddyworld import *

from pathfinder import naive, astar

import pathorder

start = node(pair(1,1), pair(0,1))

test = node(pair(9,8), pair(0,1))

obstacles = random_obstacles(8)

print(obstacles)

nodes = [node(pair(i[0], i [1]), pair(*(i[2]))) for i in obstacles]

order = pathorder.greedy(nodes, start.grid.get())

for g in order:
	print (g.get())

bot = robot(start, 3)

for goal in order:
	pathfound = astar(bot,goal)
	print(pathfound.get())
	print(pathfound.get_moves())
	start = goal

# bot = robot(start, 3)

# pathfound = astar(bot, test)
# print(pathfound.get())
# print(pathfound.get_moves())