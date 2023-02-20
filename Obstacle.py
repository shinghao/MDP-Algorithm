from Pair import pair
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

# Visited Obstacle images
OBSTACLE_VISTIED_IMG_FILE = pygame.image.load(
    os.path.join('Assets', 'ObstacleVisited.png'))
OBSTACLE_IMG_N_VISITED = pygame.transform.scale(
    OBSTACLE_VISTIED_IMG_FILE, (Constants.OBSTACLE_WIDTH, Constants.OBSTACLE_HEIGHT))
OBSTACLE_IMG_S_VISITED = pygame.transform.rotate(OBSTACLE_IMG_N_VISITED, 180)
OBSTACLE_IMG_E_VISITED = pygame.transform.rotate(OBSTACLE_IMG_N_VISITED, 90)
OBSTACLE_IMG_W_VISITED = pygame.transform.rotate(OBSTACLE_IMG_N_VISITED, -90)

# Obstacle direction vectors


class Obstacle:
    def __init__(self, pos: pair, dir: pair):
        self.pos = pos
        self.dir = dir
        self.visited = False

    def set_direction(self, dir):
        self.dir = dir

    def get_direction(self):
        return self.dir

    # Pair type
    def get_pos(self):
        return self.pos

    def get_pygame_coord(self):
        x, y = self.pos.get()
        x = (x + 1)
        y = (Constants.GRID_NUM - y)
        return pair(x, y)

    def get_visited(self):
        return self.visited

    def set_visited(self):
        self.visited = True

    def render_obstacle(self):
        x, y = self.get_pos().get()
        obstacle_grid_destination = (x * Constants.GRID_CELL_SIZE - 15 * Constants.UNIT,
                                     y * Constants.GRID_CELL_SIZE - 15 * Constants.UNIT)
        obs_dir = self.get_direction()

        if obs_dir.get() == Constants.N:
            obs_img = OBSTACLE_IMG_N_VISITED if self.visited else OBSTACLE_IMG_N
        elif obs_dir.get() == Constants.S:
            obs_img = OBSTACLE_IMG_S_VISITED if self.visited else OBSTACLE_IMG_S
        elif obs_dir.get() == Constants.E:
            obs_img = OBSTACLE_IMG_W_VISITED if self.visited else OBSTACLE_IMG_W
        else:
            obs_img = OBSTACLE_IMG_E_VISITED if self.visited else OBSTACLE_IMG_E

        Constants.WIN.blit(obs_img, obstacle_grid_destination)
