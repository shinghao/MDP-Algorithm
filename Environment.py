import os
import Constants
import pygame
import math
import Simulator

# activate the pygame library
pygame.init()

# Pygame Images

OBSTACLE_IMG_FILE = pygame.image.load(
    os.path.join('Assets', 'Obstacle.png'))
OBSTACLE_IMG_N = pygame.transform.scale(
    OBSTACLE_IMG_FILE, (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT))
OBSTACLE_IMG_S = pygame.transform.rotate(OBSTACLE_IMG_N, 180)
OBSTACLE_IMG_E = pygame.transform.rotate(OBSTACLE_IMG_N, 90)
OBSTACLE_IMG_W = pygame.transform.rotate(OBSTACLE_IMG_N, -90)

# Pygame Window
WIN = pygame.display.set_mode(
    (Constants.WIN_WIDTH, Constants.WIN_HEIGHT))  # Game window
pygame.display.set_caption("MDP Algorithm Simulator")  # Window name

# Pygame Start Rectangle
startRect = pygame.Rect(Constants.START_X, Constants.GRID_HEIGHT - (Constants.START_Y * Constants.UNIT),
                        Constants.START_WIDTH, Constants.START_HEIGHT)
startTextRect = pygame.Rect(Constants.START_X + 6, Constants.GRID_HEIGHT - (28 * Constants.UNIT),
                            Constants.START_WIDTH, Constants.START_HEIGHT)

# Pygame Texts
font = pygame.font.Font('freesansbold.ttf', 46)
text = font.render('Start', True, Constants.WHITE, None)


def __draw_window():
    '''
    This function fills the Pygame window background white
    '''
    WIN.fill(Constants.WHITE)


def __draw_start_box():
    '''
    This function uses Pygame to draw the rectangle of the starting area
    '''
    pygame.draw.rect(WIN, Constants.COLOR_START,
                     startRect)
    WIN.blit(text, startTextRect)


def __draw_grid():
    '''
    This function uses Pygame to draw a grid on the game window.
    Each line is calculated using the dimensions of the grid (Constants.GRID_WIDTH, Constants.GRID_HEIGHT) and the number of divisions (Constants.GRID_NUM).
    '''
    # Vertical line
    for i in range(Constants.GRID_NUM):
        pygame.draw.line(WIN, Constants.BLACK, (i * Constants.GRID_CELL_SIZE,
                                                0), (i * Constants.GRID_CELL_SIZE, Constants.GRID_HEIGHT))
    # Horizontal line
    for i in range(Constants.GRID_NUM):
        pygame.draw.line(WIN, Constants.BLACK, (0, Constants.GRID_HEIGHT - (i * Constants.GRID_CELL_SIZE)),
                         (Constants.GRID_WIDTH, Constants.GRID_HEIGHT - (i * Constants.GRID_CELL_SIZE)))


def __draw_obstacles(obstacle_list):
    '''
    This function uses Pygame to draw obstacles on grid cells that have value of `1`
    WIN.blit method is used to render the obstacle image
    '''
    for obs in obstacle_list:
        x, y = obs.get_coordinates()
        obstacle_grid_destination = (x * Constants.GRID_CELL_SIZE - 15 * Constants.UNIT,
                                     y * Constants.GRID_CELL_SIZE - 15 * Constants.UNIT)
        obs_dir = obs.get_direction()
        if obs_dir == Constants.Direction.NORTH:
            WIN.blit(OBSTACLE_IMG_N, obstacle_grid_destination)
        elif obs_dir == Constants.Direction.SOUTH:
            WIN.blit(OBSTACLE_IMG_S, obstacle_grid_destination)
        elif obs_dir == Constants.Direction.EAST:
            WIN.blit(OBSTACLE_IMG_E, obstacle_grid_destination)
        else:
            WIN.blit(OBSTACLE_IMG_W, obstacle_grid_destination)


def draw_environment(obstacle_list):
    __draw_window()
    __draw_start_box()
    __draw_grid()
    __draw_obstacles(obstacle_list)
