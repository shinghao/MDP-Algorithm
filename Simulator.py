import pygame
import os
import Constants
import Obstacle

# activate the pygame library
pygame.init()

# Initialise grid 2d array
grid = [[0 for _ in range(Constants.GRID_NUM)]
        for _ in range(Constants.GRID_NUM)]
pathfinding_start = False

# Initialise obstacle list
obstacle_list = []

# Pygame Images
ROBOT_IMG_FILE = pygame.image.load(os.path.join('Assets', 'Robot.png'))
ROBOT_IMG = pygame.transform.scale(
    ROBOT_IMG_FILE, (Constants.ROBOT_WIDTH, Constants.ROBOT_HEIGHT))
OBSTACLE_IMG_FILE = pygame.image.load(os.path.join('Assets', 'Obstacle.png'))
OBSTACLE_IMG_N = pygame.transform.scale(
    OBSTACLE_IMG_FILE, (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT))
OBSTACLE_IMG_S = pygame.transform.rotate(OBSTACLE_IMG_N, 180)
OBSTACLE_IMG_E = pygame.transform.rotate(OBSTACLE_IMG_N, 90)
OBSTACLE_IMG_W = pygame.transform.rotate(OBSTACLE_IMG_N, -90)

# Pygame Window
WIN = pygame.display.set_mode(
    (Constants.WIN_WIDTH, Constants.WIN_HEIGHT))  # Game window
pygame.display.set_caption("MDP Algorithm Simulator")  # Window name

# Pygame objects
robot = pygame.Rect(0, Constants.GRID_HEIGHT - (40 * Constants.UNIT),
                    Constants.ROBOT_WIDTH, Constants.ROBOT_HEIGHT)
startRect = pygame.Rect(Constants.START_X, Constants.GRID_HEIGHT - (Constants.START_Y * Constants.UNIT),
                        Constants.START_WIDTH * Constants.UNIT, Constants.START_HEIGHT * Constants.UNIT)
startTextRect = pygame.Rect(Constants.START_X + 6, Constants.GRID_HEIGHT - (28 * Constants.UNIT),
                            Constants.START_WIDTH * Constants.UNIT, Constants.START_HEIGHT * Constants.UNIT)

# Pygame Texts
font = pygame.font.Font('freesansbold.ttf', 46)
text = font.render('Start', True, Constants.WHITE, None)

# Determine obstacle face based on mouse clicking of obstacle


def draw_grid():
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


def draw_obstacles():
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


def draw_start_box():
    '''
    This function uses Pygame to draw the rectangle of the starting area
    '''
    pygame.draw.rect(WIN, Constants.COLOR_START,
                     startRect)
    WIN.blit(text, startTextRect)


def draw_window():
    '''
    This function fills the Pygame window background white
    '''
    WIN.fill(Constants.WHITE)


def draw_robot(robot):
    '''
    This function uses WIN.blit method to render the robot image based on it's position
    '''
    WIN.blit(ROBOT_IMG, (robot.x, robot.y))


def get_obstacle_direction(mouse_pos):
    x = mouse_pos[0] / Constants.UNIT % 10
    y = mouse_pos[1] / Constants.UNIT % 10

    # calculate the coordinates of each face of the obstacle
    if x < 3:
        clicked_face = "East"
        return Constants.Direction.EAST
    elif x > 7:
        clicked_face = "West"
        return Constants.Direction.WEST
    elif y > 7:
        clicked_face = "South"
        return Constants.Direction.SOUTH
    else:
        clicked_face = "North"
        return Constants.Direction.NORTH
    print(clicked_face)


def handle_obstacle_placement():
    pos = pygame.mouse.get_pos()
    x = pos[0] // Constants.GRID_CELL_SIZE
    y = pos[1] // Constants.GRID_CELL_SIZE
    obstacle_dir = get_obstacle_direction(pos)
    if grid[x][y] == 0:
        grid[x][y] = 1
        obstacle_list.append(Obstacle.Obstacle(x, y, obstacle_dir))
    if grid[x][y] == 1:
        for obs in obstacle_list:
            if obs.get_coordinates() == (x, y):
                obs.set_direction(obstacle_dir)
                break


def handle_robot_control(event, robot):
    if event.key == pygame.K_UP:
        robot.y -= Constants.VEL
    elif event.key == pygame.K_DOWN:
        robot.y += Constants.VEL
    elif event.key == pygame.K_LEFT:
        robot.x -= Constants.VEL
    if event.key == pygame.K_RIGHT:
        robot.x += Constants.VEL


def print_obstacles():
    for obs in obstacle_list:
        print(obs.get_coordinates(),
              obs.get_direction().name)


def main():
    # Spawn robot at initial position

    simulator_run = True
    can_place_obstacle = True
    can_control_robot = True
    clock = pygame.time.Clock()
    while simulator_run:
        clock.tick(Constants.FPS)
        # Handle player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulator_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and can_place_obstacle:
                handle_obstacle_placement()
            elif event.type == pygame.KEYUP:
                # Control robot manually
                if can_control_robot:
                    handle_robot_control(event, robot)
                # Start pathfinding - Disable obstacle placement and robot manual movement
                if event.key == pygame.K_SPACE:
                    print_obstacles()
                    can_place_obstacle = False
                    can_control_robot = False
                    print("Start pathfinding!")

        draw_window()
        draw_start_box()
        draw_obstacles()
        draw_grid()
        draw_robot(robot)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
