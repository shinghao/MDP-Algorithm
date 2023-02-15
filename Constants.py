from enum import Enum
import pygame

# Colors
COLOR_START = (138, 183, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constants
FPS = 120  # Frames per second
UNIT = 3  # Multiplier to allow window space to be bigger

# Grid Dimensions
GRID_NUM = 20  # number of grid squares
GRID_WIDTH, GRID_HEIGHT = 200 * UNIT, 200 * UNIT
GRID_CELL_SIZE = GRID_WIDTH // GRID_NUM

# Dimensions of Pygame window
WIN_WIDTH, WIN_HEIGHT = GRID_WIDTH, GRID_HEIGHT

# Robot
ROBOT_WIDTH, ROBOT_HEIGHT = 30 * UNIT, 30 * UNIT
ROBOT_START_X, ROBOT_START_Y = 0, GRID_HEIGHT - 40 * UNIT
ROBOT_START_ANGLE = 0
ROBOT_VEL = 10  # Velocity - speed of robot
ROBOT_TURN_RADIUS = 30 * UNIT

# Obstacle
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40 * UNIT, 40 * UNIT

# Starting box
START_X, START_Y = 0, 40
START_WIDTH, START_HEIGHT = 40 * UNIT, 40 * UNIT

# Pygame Window
WIN = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT))  # Game window


class Direction(Enum):
    '''Direction Enum'''
    NORTH = 0
    SOUTH = 180
    EAST = -90
    WEST = 90
