import pygame


class Grid:
    def __init__(self, surface, cell_count, cell_size, grid_height, grid_width, grid_line_color, robot_path_color):
        self.surface = surface
        self.cell_count = cell_count
        self.cell_size = cell_size
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.grid_line_color = grid_line_color
        self.robot_path_color = robot_path_color

        self.grid = [[0 for _ in range(self.cell_count)]
                     for _ in range(self.cell_count)]

    def get_cell_size(self):
        return self.cell_size

    def get_cell_count(self):
        return self.cell_count

    def get_cell_value(self, x: int, y: int):
        return self.grid[x][y]

    def set_cell_value(self, x: int, y: int, value: int):
        self.grid[x][y] = value

    def render_grid(self):
        '''
        This function uses Pygame to draw a grid on the game window.
        Each line is calculated using the dimensions of the grid (grid_width, grid_height) and the number of divisions (Constants.GRID_NUM).
        '''

        # Vertical line
        for i in range(self.cell_count + 1):
            pygame.draw.line(self.surface, self.grid_line_color, (i * self.cell_size,
                                                                  0), (i * self.cell_size, self.grid_height))
        # Horizontal line
        for i in range(self.cell_count + 1):
            pygame.draw.line(self.surface, self.grid_line_color, (0, self.grid_height - (i * self.cell_size)),
                             (self.grid_width, self.grid_height - (i * self.cell_size)))
