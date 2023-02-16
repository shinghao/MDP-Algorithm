import pygame
import math
import Constants
import Obstacle
import Environment
import Robot
from Pair import pair


class Sim:
    def __init__(self):
        # Initalise robot object
        self.robot = Robot.Robot(Constants.WIN, self, pair(
            Constants.ROBOT_START_X, Constants.ROBOT_START_Y))

        # Initalise Environment object
        self.environment = Environment.Environment()

        # Initialise obstacle list
        self.obstacle_list = []

        # Initialise grid 2d array
        self.grid = [[0 for _ in range(Constants.GRID_NUM)]
                     for _ in range(Constants.GRID_NUM)]

        self.refresh_screen()

    def get_robot(self):
        return self.robot

    def get_environment(self):
        return self.environment

    def refresh_screen(self):
        # Draw pygame environment onto screen - grid, obstacles, robot etc
        self.environment.render_environment(self.obstacle_list)
        self.robot.render_robot()
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
            if obs.get_coordinates() == (x, y):
                obs.set_direction(new_obstacle_dir)
                break

    def handle_obstacle_placement(self):
        pos = pygame.mouse.get_pos()
        x = pos[0] // Constants.GRID_CELL_SIZE
        y = pos[1] // Constants.GRID_CELL_SIZE
        obstacle_dir = self.get_obstacle_direction(pos)
        if self.grid[x][y] == 0:
            self.grid[x][y] = 1
            self.obstacle_list.append(Obstacle.Obstacle(x, y, obstacle_dir))
        if self.grid[x][y] == 1:
            self.change_obstacle_direction(obstacle_dir, x, y)

    def handle_robot_control(self, event, robot):
        if event.key == pygame.K_w:
            robot.move_forward()
        elif event.key == pygame.K_s:
            robot.move_backward()
        elif event.key == pygame.K_a:
            robot.move_left_forward()
        if event.key == pygame.K_d:
            robot.move_right_forward()


def main():

    simulator_run = True
    can_place_obstacle = True
    can_control_robot = True
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
            elif event.type == pygame.MOUSEBUTTONDOWN and can_place_obstacle:
                sim.handle_obstacle_placement()
                sim.refresh_screen()
            # Keyboard Input
            elif event.type == pygame.KEYUP:
                # WASD -> Control robot manually
                if can_control_robot:
                    sim.handle_robot_control(event, sim.get_robot())
                # 'SPACE' -> Start pathfinding - Disable obstacle placement and robot manual movement
                if event.key == pygame.K_SPACE:
                    can_place_obstacle = False
                    can_control_robot = False
                    print("Start pathfinding!")

        # Draw pygame environment onto screen - grid, obstacles, robot etc

    pygame.quit()


if __name__ == "__main__":
    main()
