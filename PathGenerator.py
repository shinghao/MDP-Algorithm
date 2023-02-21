from griddyworld import *
from strategy import astar_TSP
import pathorder

START_X, START_Y = 2, 3
START_DIR_X, START_DIR_Y = 0, 1


class PathGenerator:
    def __init__(self):
        self.obstacles = []

    def get_obstacles(self):
        return self.obstacles

    def generate_path(self, obstacle_list):
        start = node(pair(START_X, START_Y),
                     pair(START_DIR_X, START_DIR_Y))

        self.obstacles = []

        # Convert simulator's obstacle_list Obstacle objects into griddyworld.obstacle object
        for i in obstacle_list:
            self.obstacles.append(obstacle(
                node(i.get_pygame_coord(), i.get_direction())))

        bot = robot(start, 3)

        # Get target positions
        target_pos_list = [o.relative_ori() for o in self.obstacles]

        instruction_list = []
        instruction_list = astar_TSP(
            bot, target_pos_list, self.obstacles)

        print("Finish pathfinding algo!")
        return instruction_list
