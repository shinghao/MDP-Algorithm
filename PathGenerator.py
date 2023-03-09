from griddyworld import *
from strategy import astar_TSP

START_X, START_Y = 2, 2
SIM_START_X, SIM_START_Y = 2, 3
START_DIR_X, START_DIR_Y = 0, 1


class PathGenerator:
    def __init__(self):
        self.obstacle_orderd = []
        self.instruction_list = []

    def get_obstacles_ordered(self):
        return self.obstacle_orderd

    def get_instruction_list(self):
        return self.instruction_list

    def generate_path(self, obstacle_list, is_sim):

        obstacles_griddyworld = []

        # Simulator format
        if (is_sim):
            start = node(pair(SIM_START_X, SIM_START_Y),
                         pair(START_DIR_X, START_DIR_Y))
            id = 1
            for i in obstacle_list:
                # Convert simulator's obstacle_list Obstacle objects into griddyworld.obstacle object
                obstacles_griddyworld.append(obstacle(id,
                                                      node(i.get_pygame_coord(), i.get_direction())))
                id += 1
        else:
            start = node(pair(START_X, START_Y),
                         pair(START_DIR_X, START_DIR_Y))
            obstacles_griddyworld = [
                obstacle(i[0], node(pair(i[1], i[2]), pair(*(i[3])))) for i in obstacle_list]

        bot = robot(start, F_LEFT=pair(*F_LEFT), F_RIGHT=pair(*F_RIGHT),
                    B_LEFT=pair(*B_LEFT), B_RIGHT=pair(*B_RIGHT))

        # Get target positions
        target_pos_list = [o.goal_state() for o in obstacles_griddyworld]

        self.instruction_list, self.obstacle_orderd = astar_TSP(
            bot, target_pos_list, obstacles_griddyworld)

        print("HIHIHIHIH")
        totcost = 0
        for i in self.instruction_list:
            print(i.last().get(), i.cost)
            totcost += (i.cost)

        print(totcost)

        print("Finish pathfinding algo!")
