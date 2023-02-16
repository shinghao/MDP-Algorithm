import pygame
import Constants
import Obstacle
import Environment
import Robot
import Panel
import Grid
from Pair import pair


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

        # Initialise instruction list
        self.instruction_list = []

        # Initialise grid 2d array
        self.grid = Grid.Grid(Constants.WIN, Constants.GRID_NUM,
                              Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT, Constants.GRID_WIDTH, Constants.COLOR_GRID_LINE)
        # Initialise UI panel
        self.panel = Panel.Panel(Constants.WIN)

        self.refresh_screen()

    def refresh_screen(self):
        # Draw pygame environment onto screen - grid, obstacles, robot etc
        self.environment.render_environment(self.obstacle_list)
        self.grid.render_grid()
        self.robot.render_robot()
        self.panel.render_panel()
        pygame.display.update()

    def get_obstacle_direction(self, mouse_pos):
        x = mouse_pos[0] / Constants.UNIT % 10
        y = mouse_pos[1] / Constants.UNIT % 10

        # calculate the coordinates of each face of the obstacle
        if x < 3:
            return Constants.EAST
        elif x > 7:
            return Constants.WEST
        elif y > 7:
            return Constants.SOUTH
        else:
            return Constants.NORTH

    def change_obstacle_direction(self, new_obstacle_dir, x, y):
        for obs in self.obstacle_list:
            if obs.get_pos().get() == (x, y):
                obs.set_direction(new_obstacle_dir)
                break

    def handle_obstacle_placement(self):
        if not self.can_place_obstacle:
            return
        pos = pygame.mouse.get_pos()
        x = pos[0] // Constants.GRID_CELL_SIZE
        y = pos[1] // Constants.GRID_CELL_SIZE
        obstacle_dir = self.get_obstacle_direction(pos)

        if self.grid.get_cell(x, y) == 0:
            self.grid.set_cell(x, y, 1)
            self.obstacle_list.append(
                Obstacle.Obstacle(pair(x, y), obstacle_dir))

        if self.grid.get_cell(x, y) == 1:
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
        if event.key == pygame.K_d:
            self.robot.move_right_forward()

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
        self.grid = Grid.Grid(Constants.WIN, Constants.GRID_NUM,
                              Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT, Constants.GRID_WIDTH, Constants.COLOR_GRID_LINE)
        self.refresh_screen()

    def start_pathfinding(self):
        print("Start Pathfinding!")
        self.can_place_obstacle = False
        self.can_control_robot = False
        for instruction in self.instruction_list:
            if instruction == "move_forward":
                self.robot.move_forward()
            elif instruction == "move_backward":
                self.robot.move_backward()
            elif instruction == "move_left_forward":
                self.robot.move_left_forward()
            if instruction == "move_right_forward":
                self.robot.move_right_forward()


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
