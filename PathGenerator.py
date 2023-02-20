from Pair import pair
from griddyworld import *
from pathfinder import astar
import pathorder

START_X, START_Y = 2, 3
START_DIR_X, START_DIR_Y = 0, 1


class PathGenerator:
    def __init__(self):
        self.obstacles_nodes = []

    def get_obstacles_nodes(self):
        return self.obstacles_nodes

    def GeneratePath(self, obstacle_list):
        start = node(pair(START_X, START_Y),
                     pair(START_DIR_X, START_DIR_Y))

        self.obstacles_nodes = []

        for i in obstacle_list:
            self.obstacles_nodes.append(
                node(i.get_pygame_coord(), i.get_direction()))

        order = pathorder.greedy(self.obstacles_nodes, start.grid.get())
        bot = robot(start, 3)

        instruction_list = []

        for goal in order:
            target = obstacle(goal).relative_ori()
            pathfound = astar(bot, target)
            print(pathfound.get())
            print(pathfound.get_moves())
            instruction_list.append(pathfound.get_moves())
            start = goal

        print("Finish pathfinding algo!")
        return instruction_list
