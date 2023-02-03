import pygame
import math
import Constants
import Obstacle
import Environment
import Robot
import RobotRenderer

# Initialise grid 2d array
grid = [[0 for _ in range(Constants.GRID_NUM)]
        for _ in range(Constants.GRID_NUM)]
pathfinding_start = False

# Initialise obstacle list
obstacle_list = []


def to_pygame_y_coord(y_coordinate):
    '''
    Convert y-coordinates into pygame y-coordinates.
    This is required as pygame takes the top left of the window as the origin (0,0)
    while we are using the bottom left of the window as the origin
    '''
    return Constants.WIN_HEIGHT - y_coordinate


def get_obstacle_direction(mouse_pos):
    x = mouse_pos[0] / Constants.UNIT % 10
    y = mouse_pos[1] / Constants.UNIT % 10

    # calculate the coordinates of each face of the obstacle
    if x < 3:
        return Constants.Direction.EAST
    elif x > 7:
        return Constants.Direction.WEST
    elif y > 7:
        return Constants.Direction.SOUTH
    else:
        return Constants.Direction.NORTH


def change_obstacle_direction(new_obstacle_dir, x, y):
    for obs in obstacle_list:
        if obs.get_coordinates() == (x, y):
            obs.set_direction(new_obstacle_dir)
            break


def handle_obstacle_placement():
    pos = pygame.mouse.get_pos()
    x = pos[0] // Constants.GRID_CELL_SIZE
    y = pos[1] // Constants.GRID_CELL_SIZE
    obstacle_dir = get_obstacle_direction(pos)
    if grid[x][y] == 0:
        grid[x][y] = 1
        obstacle_list.append(Obstacle.Obstacle(x, y, obstacle_dir))
    if grid[x][y] == 1:
        change_obstacle_direction(obstacle_dir, x, y)


def handle_robot_control(event, robot):
    if event.key == pygame.K_w:
        robot.move_forward()
    elif event.key == pygame.K_s:
        robot.move_backward()
    elif event.key == pygame.K_a:
        robot.move_left_forward()
    if event.key == pygame.K_d:
        robot.move_right_forward()


def print_obstacles():
    for obs in obstacle_list:
        print(obs.get_coordinates(),
              obs.get_direction().name)


def main():
    # initalise robot object and renderer
    robot = Robot.Robot(Environment.WIN)
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

        # Draw pygame environment onto screen - grid, obstacles, robot etc
        Environment.draw_environment(obstacle_list)
        robot.render_robot()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
