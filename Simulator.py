import pygame
import Constants
import Obstacle
import Environment
import Robot
import Panel
import Grid
import RobotPathRenderer
import time
from Pair import pair
from griddyworld import *
from pathfinder import naive
import pathorder


class Sim:
    def __init__(self):
        # Activate the pygame library
        pygame.init()
        pygame.display.set_caption("MDP Algorithm Simulator")

        # Booleans
        self.can_place_obstacle = True
        self.can_control_robot = True

        # Initalise robot object
        self.robot = Robot.Robot(Constants.WIN, self, pair(
            Constants.ROBOT_START_X, Constants.ROBOT_START_Y))

        # Initalise Environment object
        self.environment = Environment.Environment()

        # Initialise obstacle list
        self.obstacle_list = []

        # Initialise pathfinding object

        # Initialise instruction list
        self.instruction_list = []

        # Initialise grid 2d array
        self.grid = Grid.Grid(Constants.WIN, Constants.GRID_NUM,
                              Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT, Constants.GRID_WIDTH, Constants.COLOR_GRID_LINE, Constants.COLOR_ROBOT_PATH)

        # Initialise robot path renderer
        self.robot_path_renderer = RobotPathRenderer.RobotPathRenderer(Constants.WIN,
                                                                       self.robot, self.grid, Constants.COLOR_ROBOT_PATH)

        # Initialise UI panel
        self.panel = Panel.Panel(Constants.WIN)

        self.refresh_screen()

    def refresh_screen(self):
        # Draw pygame environment onto screen - grid, obstacles, robot etc
        self.environment.render_environment(self.obstacle_list)
        self.grid.render_grid()
        # self.robot_path_renderer.render_robot_path()
        self.robot.render_robot()
        self.panel.render_panel()
        pygame.display.update()

    def get_obstacle_direction(self, mouse_pos):
        x = mouse_pos[0] / Constants.UNIT % 10
        y = mouse_pos[1] / Constants.UNIT % 10

        # calculate the coordinates of each face of the obstacle
        if x < 3:
            return Constants.W
        elif x > 7:
            return Constants.E
        elif y > 7:
            return Constants.N
        else:
            return Constants.S

    def change_obstacle_direction(self, new_obstacle_dir, x, y):
        for obs in self.obstacle_list:
            if obs.get_pos().get() == (x, y):
                obs.set_direction(
                    pair(new_obstacle_dir[0], new_obstacle_dir[1]))
                break

    def handle_obstacle_placement(self):
        if not self.can_place_obstacle:
            return
        pos = pygame.mouse.get_pos()
        x = pos[0] // Constants.GRID_CELL_SIZE
        y = pos[1] // Constants.GRID_CELL_SIZE
        obstacle_dir = self.get_obstacle_direction(pos)

        if self.grid.get_cell_value(x, y) == 0:
            self.grid.set_cell_value(x, y, 1)
            self.obstacle_list.append(
                Obstacle.Obstacle(pair(x, y), pair(obstacle_dir[0], obstacle_dir[1])))

        if self.grid.get_cell_value(x, y) == 1:
            self.change_obstacle_direction(obstacle_dir, x, y)

    def handle_robot_control(self, event):
        if not self.can_control_robot:
            return
        if event.key == pygame.K_w:
            self.robot.move_forward()
        elif event.key == pygame.K_s:
            self.robot.move_backward()
        elif event.key == pygame.K_a:
            self.robot.move_left_forward()
        elif event.key == pygame.K_d:
            self.robot.move_right_forward()
        elif event.key == pygame.K_z:
            self.robot.move_left_backward()
        elif event.key == pygame.K_x:
            self.robot.move_right_backward()

    def handle_button_press(self):
        if (self.panel.check_button_pressed() == Constants.BTN_STATE_START):
            self.start_pathfinding()

        elif (self.panel.check_button_pressed() == Constants.BTN_STATE_RESET):
            self.reset()

    def reset(self):
        self.can_place_obstacle = True
        self.can_control_robot = True
        self.robot = Robot.Robot(Constants.WIN, self, pair(
            Constants.ROBOT_START_X, Constants.ROBOT_START_Y))
        self.obstacle_list = []
        self.instruction_list = []
        self.grid = Grid.Grid(Constants.WIN, Constants.GRID_NUM,
                              Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT, Constants.GRID_WIDTH, Constants.COLOR_GRID_LINE, Constants.COLOR_ROBOT_PATH)
        self.refresh_screen()

    def capture_obstacle_image(self):
        print("Capture obstacle image!")

    def handle_instructions(self):
        for instruction_one_path in self.instruction_list:
            for instruction in instruction_one_path:
                if instruction == "forward":
                    self.robot.move_forward()
                elif instruction == "back":
                    self.robot.move_backward()
                elif instruction == "left":
                    self.robot.move_left_forward()
                elif instruction == "right":
                    self.robot.move_right_forward()
                elif instruction == "backleft":
                    self.robot.move_left_backward()
                elif instruction == "backright":
                    self.robot.move_right_backward()
                elif instruction == "capture_obstacle_image":
                    self.capture_obstacle_image()

                # Keep looping until robot finish executing current movement
                while (self.robot.get_is_moving()):
                    continue
            time.sleep(4)

    def pathfinding_algo(self):

        start = node(pair(1, 1), pair(0, 1))

        nodes = []
        for i in self.obstacle_list:
            nodes.append(node(i.get_pos(), i.get_direction()))
            print("hi", i.get_pos().get(), i.get_direction().get())

        order = pathorder.greedy(nodes, start.grid.get())
        bot = robot(start, 3)
        for goal in order:
            pathfound = naive(bot, goal)
            print(pathfound.get())
            print(pathfound.get_moves())
            self.instruction_list.append(pathfound.get_moves())
            start = goal
        print("Finish pathfinding algo!")

    def start_pathfinding(self):
        print("Start Pathfinding!")
        self.can_place_obstacle = False
        self.can_control_robot = False
        # Take in instruction list from pathfinding gen using obstacle_list
        # Take in hamiltanion path from pathfinding gen
        self.pathfinding_algo()
        self.handle_instructions()


def main():

    simulator_run = True

    clock = pygame.time.Clock()

    sim = Sim()

    while simulator_run:
        clock.tick(Constants.FPS)

        # Handle player inputs
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                simulator_run = False
            # Mouse Input
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] < Constants.GRID_WIDTH and pos[1] < Constants.GRID_HEIGHT):
                    sim.handle_obstacle_placement()
                else:
                    sim.handle_button_press()
                sim.refresh_screen()
            # Keyboard Input
            elif event.type == pygame.KEYUP:
                # WASD -> Control robot manually
                sim.handle_robot_control(event)

    pygame.quit()


if __name__ == "__main__":
    main()
