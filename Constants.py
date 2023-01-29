# Colors
COLOR_START = (138, 183, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_OBSTACLE_IMG = (255, 0, 0)
COLOR_OBSTACLE_COLLIDER = (200, 0, 0)

# Constants
FPS = 120  # Frames per second
UNIT = 3  # Multiplier to allow window space to be bigger
VEL = 10  # Velocity - speed of robot

# Dimensions
GRID_NUM = 20  # number of grid squares
GRID_WIDTH, GRID_HEIGHT = 200 * UNIT, 200 * UNIT  # Dimensions of grid
GRID_CELL_SIZE = GRID_WIDTH // GRID_NUM

WIN_WIDTH, WIN_HEIGHT = GRID_WIDTH, GRID_HEIGHT  # Dimensions of Pygame window

ROBOT_WIDTH, ROBOT_HEIGHT = 30 * UNIT, 30 * UNIT  # Dimensions of robot
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40 * UNIT, 40 * UNIT  # Dimensions of obstacles

START_X, START_Y = 0, 40
START_WIDTH, START_HEIGHT = 40, 40
