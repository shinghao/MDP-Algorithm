import pygame


class Grid:
    def __init__(self, surface, cell_count, cell_size, grid_height, grid_width, grid_color):
        self.surface = surface
        self.cell_count = cell_count
        self.cell_size = cell_size
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.grid_color = grid_color

        self.grid = [[0 for _ in range(self.cell_count)]
                     for _ in range(self.cell_count)]

    def get_cell(self, x, y):
        return self.grid[x][y]

    def set_cell(self, x, y, value):
        self.grid[x][y] = value

    def render_grid(self):
        '''
        This function uses Pygame to draw a grid on the game window.
        Each line is calculated using the dimensions of the grid (grid_width, grid_height) and the number of divisions (Constants.GRID_NUM).
        '''

        # Vertical line
        for i in range(self.cell_count + 1):
            pygame.draw.line(self.surface, self.grid_color, (i * self.cell_size,
                                                             0), (i * self.cell_size, self.grid_height))
        # Horizontal line
        for i in range(self.cell_count + 1):
            pygame.draw.line(self.surface, self.grid_color, (0, self.grid_height - (i * self.cell_size)),
                             (self.grid_width, self.grid_height - (i * self.cell_size)))
