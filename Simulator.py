import pygame
import Constants
import Obstacle
import Environment
import Robot
import Panel
import Grid
import RobotPathRenderer
import time
from griddyworld import pair
from PathGenerator import PathGenerator
import mapping
import obstacleRandomiser


''' Utility functions for pygame'''

# Pygame Window
WIN = pygame.display.set_mode(
    (Constants.WIN_WIDTH, Constants.WIN_HEIGHT))  # Game window


def to_pygame_coord(x, y):
    '''
    Convert real world x,y (where 0,0 is bottom left) to pygame coordinates (where 0,0 is at top left)
    '''
    return (x - 1, (Constants.GRID_NUM - y))


def add_obstacles_manually(obs_list: list):
    '''
    Convert a list of obstacle in (x,y,(direct)) format to a list of obstacle objects
    '''
    obstacle_list_result = []
    for o in obs_list:
        pos = to_pygame_coord(o[0], o[1])
        dir = o[2]
        obstacle = Obstacle.Obstacle(pos, dir, WIN)
        obstacle_list_result.append(obstacle)
    return obstacle_list_result


''' Simulator Class '''


class Sim:
    def __init__(self):
        # Activate the pygame library
        pygame.init()
        pygame.display.set_caption("MDP Algorithm Simulator")

        # Booleans
        self.can_place_obstacle = True
        self.can_control_robot = True

        # Initalise robot object
        self.robot = Robot.Robot(WIN, self, pair(
            Constants.ROBOT_START_X, Constants.ROBOT_START_Y))

        # Initalise Environment object
        self.environment = Environment.Environment(WIN)

        # Initialise obstacle list
        # Add list of obstacles here if you want to manually insert obstacles for testing
        manual_obs_list = []
        self.obstacle_list = add_obstacles_manually(manual_obs_list)

        # Initialise pathfinding object

        self.path_generator = PathGenerator()

        # Initialise instruction list and obstacle order list
        self.obstacle_list_ordered = []
        self.instruction_list = []

        # Initialise grid 2d array
        self.grid = Grid.Grid(WIN, Constants.GRID_NUM,
                              Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT, Constants.GRID_WIDTH, Constants.COLOR_GRID_LINE, Constants.COLOR_ROBOT_PATH)

        # Initialise robot path renderer
        self.robot_path_renderer = RobotPathRenderer.RobotPathRenderer(WIN,
                                                                       self.robot, self.grid, Constants.COLOR_ROBOT_PATH)

        # Initialise UI panel
        self.panel = Panel.Panel(WIN)

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
            return Constants.S
        else:
            return Constants.N

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
        # x, y = self.ToPygameXCoords(x), self.ToPygameYCoords(y)
        obstacle_dir = self.get_obstacle_direction(pos)

        if self.grid.get_cell_value(x, y) == 0:
            self.grid.set_cell_value(x, y, 1)
            self.obstacle_list.append(
                Obstacle.Obstacle(pair(x, y), pair(obstacle_dir[0], obstacle_dir[1]), WIN))

        if self.grid.get_cell_value(x, y) == 1:
            self.change_obstacle_direction(obstacle_dir, x, y)

        self.refresh_screen()

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

        elif (self.panel.check_button_pressed() == Constants.BTN_STATE_GENOBS):
            self.generate_random_obstacles()

        else:
            return

        self.refresh_screen()

    def reset(self):
        self.can_place_obstacle = True
        self.can_control_robot = True
        self.robot = Robot.Robot(WIN, self, pair(
            Constants.ROBOT_START_X, Constants.ROBOT_START_Y))
        self.obstacle_list = []
        self.obstacle_list_ordered = []
        self.instruction_list = []
        self.grid = Grid.Grid(WIN, Constants.GRID_NUM,
                              Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT, Constants.GRID_WIDTH, Constants.COLOR_GRID_LINE, Constants.COLOR_ROBOT_PATH)
        self.refresh_screen()

    def generate_random_obstacles(self):
        self.reset()
        self.obstacle_list = add_obstacles_manually(
            obstacleRandomiser.random_obstacles(Constants.NUM_OBS_GENERATED))

    def handle_instructions(self):
        count = 0
        obstacle_node_list = self.obstacle_list_ordered
        for instruction_one_path in self.instruction_list:
            for instruction in instruction_one_path.get_moves():
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

                # Keep looping until robot finish executing current movement
                while (self.robot.get_is_moving()):
                    continue

            time.sleep(0.5)
            cur_obstacle_pos = obstacle_node_list[count].get_xy_coord()
            for obs in self.obstacle_list:
                if obs.get_pygame_coord().get() == cur_obstacle_pos:
                    obs.set_visited()
                    break
            time.sleep(0.5)
            count += 1

    def pathfinding_algo(self):
        self.path_generator.generate_path(self.obstacle_list, is_sim=True)
        self.obstacle_list_ordered = self.path_generator.get_obstacles_ordered()
        self.instruction_list = self.path_generator.get_instruction_list()
        translated_instr_list = []
        for instr in self.instruction_list:
            translated_instr_list.append(
                mapping.translate(instr.get_moves()))

        # Convert list translated instructions into a single string for sending back to RPI
        instruction_str = mapping.translate_instructions_to_RPI(
            translated_instr_list)
        print(instruction_str)

    def start_pathfinding(self):
        print("Start Pathfinding!")
        self.can_place_obstacle = False
        self.can_control_robot = False
        # Take in instruction list from pathfinding gen using obstacle_list
        # Take in hamiltanion path from pathfinding gen
        self.pathfinding_algo()
        self.handle_instructions()


''' Main Function for running Simulator'''


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

            # Keyboard Input
            elif event.type == pygame.KEYUP:
                # WASD -> Control robot manually
                sim.handle_robot_control(event)

    pygame.quit()


''' Uncomment this to run simulator'''
if __name__ == "__main__":
    main()
