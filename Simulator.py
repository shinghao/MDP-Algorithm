import pygame
import os

# colors
COLOR_START = (138, 183, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_OBSTACLE_IMG = (255, 0, 0)
COLOR_OBSTACLE_COLLIDER = (200, 0, 0)

# constants
FPS = 120
UNIT = 3
GRID_NUM = 20  # number of grid squares
GRID_WIDTH, GRID_HEIGHT = 200 * UNIT, 200 * UNIT
WIN_WIDTH, WIN_HEIGHT = GRID_WIDTH, GRID_HEIGHT
ROBOT_WIDTH, ROBOT_HEIGHT = 30 * UNIT, 30 * UNIT
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40 * UNIT, 40 * UNIT
VEL = 10


# navigational area of GRID_WIDTH * GRID_HEIGHT
# nav_area = [[0 for _ in range(GRID_WIDTH) for _ in range(GRID_NUM)]]
grid = [[0 for _ in range(GRID_NUM)] for _ in range(GRID_NUM)]
pathfinding_start = False

# Images
ROBOT_IMAGE = pygame.image.load(os.path.join('Assets', 'Robot.png'))
ROBOT = pygame.transform.scale(ROBOT_IMAGE, (ROBOT_WIDTH, ROBOT_HEIGHT))
OBSTACLE_IMAGE = pygame.image.load(os.path.join('Assets', 'Obstacle.png'))
OBSTACLE = pygame.transform.scale(
    OBSTACLE_IMAGE, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Game window
pygame.display.set_caption("MDP Algorithm Simulator")  # Window name


def color_obstacle_face(mouse_pos, grid_x, grid_y):
    x = mouse_pos[0] / UNIT % 10
    y = mouse_pos[1] / UNIT % 10

    # calculate the coordinates of each face of the obstacle
    if x < 3:
        clicked_face = "left"
        # pygame.draw.line(WIN, COLOR_OBSTACLE_IMG, (0, GRID_HEIGHT - (grid_x*(GRID_HEIGHT//GRID_NUM))),
        # (GRID_WIDTH, GRID_HEIGHT - (grid_y*(GRID_HEIGHT//GRID_NUM))))
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
    # Draw grid lines
    for i in range(GRID_NUM):
        pygame.draw.line(WIN, BLACK, (i*(GRID_WIDTH//GRID_NUM),
                                      0), (i*(GRID_WIDTH//GRID_NUM), GRID_HEIGHT))
    for i in range(GRID_NUM):
        pygame.draw.line(WIN, BLACK, (0, GRID_HEIGHT - (i*(GRID_HEIGHT//GRID_NUM))),
                         (GRID_WIDTH, GRID_HEIGHT - (i*(GRID_HEIGHT//GRID_NUM))))


def draw_obstacles():
    # Draw obstacles
    for i in range(GRID_NUM):
        for j in range(GRID_NUM):
            if grid[i][j] == 1:
                # pygame.draw.rect(WIN, BLACK, (i * (GRID_WIDTH // GRID_NUM), j * (
                #     GRID_HEIGHT // GRID_NUM), GRID_WIDTH // GRID_NUM, GRID_HEIGHT // GRID_NUM))
                WIN.blit(OBSTACLE,
                         (i * (GRID_WIDTH // GRID_NUM) - 15 * UNIT,
                          j * (GRID_HEIGHT // GRID_NUM) - 15 * UNIT))


def draw_start_box():
    # Draw start area
    pygame.draw.rect(WIN, COLOR_START,
                     pygame.Rect(0, GRID_HEIGHT - (40 * UNIT), 40 * UNIT, 40*UNIT))


def draw_window():
    WIN.fill(WHITE)
    draw_start_box()
    draw_obstacles()
    draw_grid()


def main():
    robot = pygame.Rect(0, GRID_HEIGHT - (40 * UNIT),
                        ROBOT_WIDTH, ROBOT_HEIGHT)
    run = True
    pathfinding_start = False
    clock = pygame.time.Clock()
    while run:
        placed_obstacle = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Click to place obstacles
            elif event.type == pygame.MOUSEBUTTONDOWN and not pathfinding_start:
                pos = pygame.mouse.get_pos()
                x, y = pos[0] // (GRID_WIDTH //
                                  GRID_NUM), pos[1] // (GRID_HEIGHT // GRID_NUM)
                if grid[x][y] == 0:
                    grid[x][y] = 1
                    color_obstacle_face(pos, x, y)
                    placed_obstacle = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    robot.y -= VEL
                elif event.key == pygame.K_DOWN:
                    robot.y += VEL
                elif event.key == pygame.K_LEFT:
                    robot.x -= VEL
                if event.key == pygame.K_RIGHT:
                    robot.x += VEL

            # Start pathfinding

        draw_window()
        WIN.blit(ROBOT, (robot.x, robot.y))
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
