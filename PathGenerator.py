from griddyworld import *
from strategy import astar_TSP
import pathorder

START_X, START_Y = 2, 3
START_DIR_X, START_DIR_Y = 0, 1


class PathGenerator:
    def __init__(self):
        self.obstacle_orderd = []
        self.instruction_list = []

    def get_obstacles_ordered(self):
        return self.obstacle_orderd

    def get_instruction_list(self):
        return self.instruction_list

    def generate_path(self, obstacle_list):
        start = node(pair(START_X, START_Y),
                     pair(START_DIR_X, START_DIR_Y))

        # Convert simulator's obstacle_list Obstacle objects into griddyworld.obstacle object
        obstacles_griddyworld = []
        for i in obstacle_list:
            obstacles_griddyworld.append(obstacle(
                node(i.get_pygame_coord(), i.get_direction())))

        bot = robot(start, 3)

        # Get target positions
        target_pos_list = [o.relative_ori() for o in obstacles_griddyworld]

        self.instruction_list, self.obstacle_orderd = astar_TSP(
            bot, target_pos_list, obstacles_griddyworld)

        print("Finish pathfinding algo!")
