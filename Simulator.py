import pygame
import os
import Constants

# nav_area = [[0 for _ in range(Constants.GRID_WIDTH) for _ in range(Constants.GRID_NUM)]]
grid = [[0 for _ in range(Constants.GRID_NUM)]
        for _ in range(Constants.GRID_NUM)]
pathfinding_start = False

# Images
ROBOT_IMAGE = pygame.image.load(os.path.join('Assets', 'Robot.png'))
ROBOT = pygame.transform.scale(
    ROBOT_IMAGE, (Constants.ROBOT_WIDTH, Constants.ROBOT_HEIGHT))
OBSTACLE_IMAGE = pygame.image.load(os.path.join('Assets', 'Obstacle.png'))
OBSTACLE = pygame.transform.scale(
    OBSTACLE_IMAGE, (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT))

# Window
WIN = pygame.display.set_mode(
    (Constants.WIN_WIDTH, Constants.WIN_HEIGHT))  # Game window
pygame.display.set_caption("MDP Algorithm Simulator")  # Window name


# Determine obstacle face based on mouse clicking of obstacle
def color_obstacle_face(mouse_pos, grid_x, grid_y):
    '''
    TODO - Work in progress
    '''
    x = mouse_pos[0] / Constants.UNIT % 10
    y = mouse_pos[1] / Constants.UNIT % 10

    # calculate the coordinates of each face of the obstacle
    if x < 3:
        clicked_face = "left"
        # pygame.draw.line(WIN, COLOR_OBSTACLE_IMG, (0, Constants.GRID_HEIGHT - (grid_x*(Constants.GRID_HEIGHT//Constants.GRID_NUM))),
        # (Constants.GRID_WIDTH, Constants.GRID_HEIGHT - (grid_y*(Constants.GRID_HEIGHT//Constants.GRID_NUM))))
    elif x > 7:
        clicked_face = "right"
    elif y < 3:
        clicked_face = "top"
    elif y > 7:
        clicked_face = "bottom"
    else:
        clicked_face = "front"

    print(clicked_face)


def draw_grid():
    '''
    This function uses Pygame to draw a grid on the game window.
    Each line is calculated using the dimensions of the grid (Constants.GRID_WIDTH, Constants.GRID_HEIGHT) and the number of divisions (Constants.GRID_NUM).
    '''
    # Vertical line
    for i in range(Constants.GRID_NUM):
        pygame.draw.line(WIN, Constants.BLACK, (i*(Constants.GRID_WIDTH//Constants.GRID_NUM),
                                                0), (i*(Constants.GRID_WIDTH//Constants.GRID_NUM), Constants.GRID_HEIGHT))
    # Horizontal line
    for i in range(Constants.GRID_NUM):
        pygame.draw.line(WIN, Constants.BLACK, (0, Constants.GRID_HEIGHT - (i*(Constants.GRID_HEIGHT//Constants.GRID_NUM))),
                         (Constants.GRID_WIDTH, Constants.GRID_HEIGHT - (i*(Constants.GRID_HEIGHT//Constants.GRID_NUM))))


def draw_obstacles():
    '''
    This function uses Pygame to draw obstacles on grid cells that have value of `1`
    WIN.blit method is used to render the obstacle image
    '''
    for i in range(Constants.GRID_NUM):
        for j in range(Constants.GRID_NUM):
            if grid[i][j] == 1:
                # pygame.draw.rect(WIN, Constants.BLACK, (i * (Constants.GRID_WIDTH // Constants.GRID_NUM), j * (
                #     Constants.GRID_HEIGHT // Constants.GRID_NUM), Constants.GRID_WIDTH // Constants.GRID_NUM, Constants.GRID_HEIGHT // Constants.GRID_NUM))
                WIN.blit(OBSTACLE,
                         (i * (Constants.GRID_WIDTH // Constants.GRID_NUM) - 15 * Constants.UNIT,
                          j * (Constants.GRID_HEIGHT // Constants.GRID_NUM) - 15 * Constants.UNIT))


def draw_start_box():
    '''
    This function uses Pygame to draw the rectangle of the starting area
    '''
    pygame.draw.rect(WIN, Constants.COLOR_START,
                     pygame.Rect(0, Constants.GRID_HEIGHT - (40 * Constants.UNIT), 40 * Constants.UNIT, 40*Constants.UNIT))


def draw_window():
    '''
    This function fills the Pygame window background white
    '''
    WIN.fill(Constants.WHITE)


def draw_robot(robot):
    '''
    This function uses WIN.blit method to render the robot image based on it's position
    '''
    WIN.blit(ROBOT, (robot.x, robot.y))


def handle_obstacle_placement():
    pos = pygame.mouse.get_pos()
    x, y = pos[0] // (Constants.GRID_WIDTH //
                      Constants.GRID_NUM), pos[1] // (Constants.GRID_HEIGHT // Constants.GRID_NUM)
    if grid[x][y] == 0:
        grid[x][y] = 1
        color_obstacle_face(pos, x, y)


def handle_robot_movement(event, robot):
    if event.key == pygame.K_UP:
        robot.y -= Constants.VEL
    elif event.key == pygame.K_DOWN:
        robot.y += Constants.VEL
    elif event.key == pygame.K_LEFT:
        robot.x -= Constants.VEL
    if event.key == pygame.K_RIGHT:
        robot.x += Constants.VEL


def main():
    # Spawn robot at initial position
    robot = pygame.Rect(0, Constants.GRID_HEIGHT - (40 * Constants.UNIT),
                        Constants.ROBOT_WIDTH, Constants.ROBOT_HEIGHT)
    run = True
    pathfinding_start = False
    clock = pygame.time.Clock()
    while run:
        clock.tick(Constants.FPS)
        # Handle player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not pathfinding_start:
                handle_obstacle_placement()
            elif event.type == pygame.KEYUP:
                handle_robot_movement(event, robot)

            # Start pathfinding
        draw_window()
        draw_start_box()
        draw_obstacles()
        draw_grid()
        draw_robot(robot)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
