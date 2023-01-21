import pygame
import sys
import heapq


def distance(a, b, grid, grid_size):
    dist = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    nearest_obstacle_dist = float("inf")
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == 1:
                obstacle_dist = ((i - b[0]) ** 2 + (j - b[1]) ** 2) ** 0.5
                nearest_obstacle_dist = min(
                    nearest_obstacle_dist, obstacle_dist)
    return dist + nearest_obstacle_dist


def neighbors(node):
    x, y = node
    result = []
    if x > 0:
        result.append((x - 1, y))
    if x < grid_size - 1:
        result.append((x + 1, y))
    if y > 0:
        result.append((x, y - 1))
    if y < grid_size - 1:
        result.append((x, y + 1))
    return result


pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
grid_size = 20
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
visited = set()

start, end = (0, 0), (19, 19)
path = set()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = pos[0] // (width //
                              grid_size), pos[1] // (height // grid_size)
            if not start:
                start = (x, y)
            elif not end:
                end = (x, y)
            elif grid[x][y] == 0:
                grid[x][y] = 1
            else:
                grid[x][y] = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                print("Space")

                def a_star(start, end):
                    heap = [(0, start)]
                    visited.clear()
                    came_from = {}
                    while heap:
                        (cost, current) = heapq.heappop(heap)
                        if current in visited:
                            continue
                        visited.add(current)
                        if current == end:
                            while current != start:
                                path.add(current)
                                current = came_from[current]
                            return
                        for neighbor in neighbors(current):
                            if grid[neighbor[0]][neighbor[1]] == 1:
                                continue
                            new_cost = cost + \
                                distance(current, neighbor, grid, grid_size)
                            if neighbor not in came_from or new_cost < cost:
                                came_from[neighbor] = current
                                heapq.heappush(
                                    heap, (cost + distance(current, neighbor, grid, grid_size), neighbor))
                a_star(start, end)
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0, 255, 0), (start[0] * (width // grid_size), start[1] * (
        height // grid_size), width // grid_size, height // grid_size))
    pygame.draw.rect(screen, (0, 0, 255), (end[0] * (width // grid_size), end[1] * (
        height // grid_size), width // grid_size, height // grid_size))
    # draw obstacles
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (i * (width // grid_size), j * (
                    height // grid_size), width // grid_size, height // grid_size))
    # draw grid lines
    for i in range(grid_size):
        pygame.draw.line(screen, (0, 0, 0), (i*(width//grid_size),
                         0), (i*(width//grid_size), height))
    for i in range(grid_size):
        pygame.draw.line(
            screen, (0, 0, 0), (0, i*(height//grid_size)), (width, i*(height//grid_size)))

    for node in path:
        pygame.draw.rect(screen, (255, 0, 0), (node[0] * (width // grid_size), node[1] * (
            height // grid_size), width // grid_size, height // grid_size))

    pygame.display.update()
