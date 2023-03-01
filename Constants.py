# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLOR_START = (52, 152, 219)
COLOR_GRID_BG = (199, 236, 255)
COLOR_GRID_LINE = BLACK
COLOR_BG = (223, 230, 233)
COLOR_BTN_START = (106, 176, 76)
COLOR_BTN_RESET = (235, 77, 75)
COLOR_BTN_GENOBS = (230, 126, 34)
COLOR_ROBOT_PATH = (223, 230, 233)

# Constants
FPS = 120  # Frames per second
UNIT = 3  # Multiplier to allow window space to be bigger

# Grid Dimensions
GRID_NUM = 20  # number of grid squares
GRID_WIDTH, GRID_HEIGHT = 200 * UNIT, 200 * UNIT
GRID_CELL_SIZE = GRID_WIDTH // GRID_NUM

# Robot
ROBOT_WIDTH, ROBOT_HEIGHT = 30 * UNIT, 30 * UNIT
ROBOT_START_X, ROBOT_START_Y = 0, GRID_HEIGHT - 40 * UNIT
ROBOT_START_ANGLE = 0
ROBOT_VEL = 0.3  # Velocity - speed of robot
ROBOT_TURN_RADIUS = 30 * UNIT

# Obstacle
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40 * UNIT, 40 * UNIT

# Starting box
START_X, START_Y = 0, 40
START_WIDTH, START_HEIGHT = 40 * UNIT, 40 * UNIT

# Dimensions of Pygame window
WIN_WIDTH, WIN_HEIGHT = 1000, GRID_HEIGHT

# DIRECTIONS
NORTH = 0
SOUTH = 180
EAST = -90
WEST = 90

N, E, S, W = (0, 1), (1, 0), (0, -1), (-1, 0)

# Buttons
BTN_WIDTH, BTN_HEIGHT = 60 * UNIT, 14 * UNIT

BTN_GENOBS_X, BTN_GENOBS_Y = (
    WIN_WIDTH - GRID_WIDTH - BTN_WIDTH) / 2 + GRID_WIDTH, WIN_HEIGHT - 70 * UNIT
BTN_START_X, BTN_START_Y = (
    WIN_WIDTH - GRID_WIDTH - BTN_WIDTH) / 2 + GRID_WIDTH, WIN_HEIGHT - 50 * UNIT
BTN_RESET_X, BTN_RESET_Y = (
    WIN_WIDTH - GRID_WIDTH - BTN_WIDTH) / 2 + GRID_WIDTH, WIN_HEIGHT - 30 * UNIT

BTN_FONT_SIZE = 20

# Button States
BTN_STATE_START = "START"
BTN_STATE_RESET = "RESTART"
BTN_STATE_GENOBS = "GENERATEOBSTACLE"

# Number of random obstacles generated
NUM_OBS_GENERATED = 4
