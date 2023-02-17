from griddyworld import *

from pathfinder import naive

import pathorder

test = node(pair(1,1), pair(1,0))

obstacles = random_obstacles(8)

print(obstacles)

nodes = [node(pair(i[0], i [1]), pair(*(i[2]))) for i in obstacles]

order = pathorder.greedy(nodes, test.grid.get())

for g in order:
	print (g.get())

start = test

bot = robot(test, 3)

for goal in order:
	pathfound = naive(bot,goal)
	print(pathfound.get())
	print(pathfound.get_moves())
	start = goal