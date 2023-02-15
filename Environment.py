import os
import Constants
import pygame


# Obstacle images
OBSTACLE_IMG_FILE = pygame.image.load(
    os.path.join('Assets', 'Obstacle.png'))
OBSTACLE_IMG_N = pygame.transform.scale(
    OBSTACLE_IMG_FILE, (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT))
OBSTACLE_IMG_S = pygame.transform.rotate(OBSTACLE_IMG_N, 180)
OBSTACLE_IMG_E = pygame.transform.rotate(OBSTACLE_IMG_N, 90)
OBSTACLE_IMG_W = pygame.transform.rotate(OBSTACLE_IMG_N, -90)


'''
The Environment class defines and creates the simulation environment for pygame, including the grid, obstacles, starting area.
These components that make up the environment is drawn on the pygame window by calling render_environment() function that in turn calls several private helper functions
'''


class Environment:
    def __init__(self):

        # Activate the pygame library
        pygame.init()

        # Pygame Start Rectangle Box
        self.startRect = pygame.Rect(Constants.START_X, Constants.GRID_HEIGHT - (Constants.START_Y * Constants.UNIT),
                                     Constants.START_WIDTH, Constants.START_HEIGHT)
        self.startTextRect = pygame.Rect(Constants.START_X + 6, Constants.GRID_HEIGHT - (28 * Constants.UNIT),
                                         Constants.START_WIDTH, Constants.START_HEIGHT)

        # Initalise font
        self.font = pygame.font.Font('freesansbold.ttf', 46)

    def __draw_window(self):
        '''
        This function fills the Pygame window background white
        '''
        Constants.WIN.fill(Constants.WHITE)

    def __draw_start_box(self):
        '''
        This function uses Pygame to draw the rectangle of the starting area
        '''
        pygame.draw.rect(Constants.WIN, Constants.COLOR_START,
                         self.startRect)
        start_text = self.font.render('Start', True, Constants.WHITE, None)
        Constants.WIN.blit(start_text, self.startTextRect)

    def __draw_grid(self):
        '''
        This function uses Pygame to draw a grid on the game window.
        Each line is calculated using the dimensions of the grid (Constants.GRID_WIDTH, Constants.GRID_HEIGHT) and the number of divisions (Constants.GRID_NUM).
        '''
        # Vertical line
        for i in range(Constants.GRID_NUM):
            pygame.draw.line(Constants.WIN, Constants.BLACK, (i * Constants.GRID_CELL_SIZE,
                                                              0), (i * Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT))
        # Horizontal line
        for i in range(Constants.GRID_NUM):
            pygame.draw.line(Constants.WIN, Constants.BLACK, (0, Constants.GRID_HEIGHT - (i * Constants.GRID_CELL_SIZE)),
                             (Constants.GRID_WIDTH, Constants.GRID_HEIGHT - (i * Constants.GRID_CELL_SIZE)))

    def __draw_obstacles(self, obstacle_list):
        '''
        This function uses Pygame to draw obstacles on grid cells that have value of `1`
        Constants.WIN.blit method is used to render the obstacle image
        '''
        for obs in obstacle_list:
            x, y = obs.get_coordinates()
            obstacle_grid_destination = (x * Constants.GRID_CELL_SIZE - 15 * Constants.UNIT,
                                         y * Constants.GRID_CELL_SIZE - 15 * Constants.UNIT)
            obs_dir = obs.get_direction()
            if obs_dir == Constants.Direction.NORTH:
                Constants.WIN.blit(OBSTACLE_IMG_N, obstacle_grid_destination)
            elif obs_dir == Constants.Direction.SOUTH:
                Constants.WIN.blit(OBSTACLE_IMG_S, obstacle_grid_destination)
            elif obs_dir == Constants.Direction.EAST:
                Constants.WIN.blit(OBSTACLE_IMG_E, obstacle_grid_destination)
            else:
                Constants.WIN.blit(OBSTACLE_IMG_W, obstacle_grid_destination)

    def render_environment(self, obstacle_list):
        '''
        This function draws the environment on the pygame window - starting box, grid, obstacles
        '''
        self.__draw_window()
        self.__draw_start_box()
        self.__draw_grid()
        self.__draw_obstacles(obstacle_list)
