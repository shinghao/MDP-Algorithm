import Constants
import pygame


'''
The Environment class defines and creates the simulation environment for pygame, including the grid, obstacles, starting area.
These components that make up the environment is drawn on the pygame window by calling render_environment() function that in turn calls several private helper functions
'''


class Environment:
    def __init__(self):

        # Pygame Start Rectangle Box
        self.startRect = pygame.Rect(Constants.START_X, Constants.GRID_HEIGHT - (Constants.START_Y * Constants.UNIT),
                                     Constants.START_WIDTH, Constants.START_HEIGHT)
        self.startTextRect = pygame.Rect(Constants.START_X + 6, Constants.GRID_HEIGHT - (28 * Constants.UNIT),
                                         Constants.START_WIDTH, Constants.START_HEIGHT)
        self.gridRect = pygame.Rect(
            0, 0, Constants.GRID_WIDTH, Constants.GRID_HEIGHT)
        # Initalise font
        self.font = pygame.font.Font('freesansbold.ttf', 46)

    def __draw_window(self):
        '''
        This function fills the Pygame window background white
        '''
        Constants.WIN.fill(Constants.COLOR_BG)

        # Grid background
        pygame.draw.rect(Constants.WIN, Constants.COLOR_GRID_BG,
                         self.gridRect)

    def __draw_start_box(self):
        '''
        This function uses Pygame to draw the rectangle of the starting area
        '''
        pygame.draw.rect(Constants.WIN, Constants.COLOR_START,
                         self.startRect)
        start_text = self.font.render('Start', True, Constants.WHITE, None)
        Constants.WIN.blit(start_text, self.startTextRect)

    def __draw_obstacles(self, obstacle_list):
        '''
        This function uses Pygame to draw obstacles on grid cells
        '''
        for obstacle in obstacle_list:
            obstacle.render_obstacle()

    def render_environment(self, obstacle_list):
        '''
        This function draws the environment on the pygame window - starting box, grid, obstacles
        '''
        self.__draw_window()
        self.__draw_start_box()
        self.__draw_obstacles(obstacle_list)
