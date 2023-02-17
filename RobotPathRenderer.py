
import pygame
import Constants
ROBOT_PATH_VAL = 2


class RobotPathRenderer:
    def __init__(self, surface, robot, grid, robot_path_color):
        self.surface = surface
        self.robot = robot
        self.grid = grid
        self.robot_path_color = robot_path_color

    def render_robot_path(self):
        pos = self.robot.get_pos().get()
        x = int(pos[0] // self.grid.get_cell_size()) + 1
        y = int(pos[1] // self.grid.get_cell_size()) + 1

        self.grid.set_cell_value(x, y, 2)

        # Robot path cell color
        for x in range(self.grid.get_cell_count()):
            for y in range(self.grid.get_cell_count()):
                if (self.grid.get_cell_value(x, y) == 2):
                    rect = pygame.Rect(
                        x * self.grid.get_cell_size(), y * self.grid.get_cell_size(), self.grid.get_cell_size(), self.grid.get_cell_size())
                    pygame.draw.rect(self.surface, self.robot_path_color, rect)
