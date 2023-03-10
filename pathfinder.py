from griddyworld import *
from heuristics import euc_dist, costing

import heapq


class revisitError(Exception):
    pass


def astar(bot, goal: node, obstacles, strictness = True):
    ''' bot should already be in the correct starting position
        node is the destination grid and orientation
        obstacles refer to the list of obstacles to avoid and check for
        strictness determines if bot can move close to the boundaries - True = avoid going near bounds'''

    print("Executing A-star algorithm for %s to %s" %
          (bot.pos.get(), goal.get()))

    N_visited = [[None for i in range(0, GRID_X)] for j in range(
        0, GRID_Y)]  # visited matrix for north
    S_visited = [[None for i in range(0, GRID_X)] for j in range(
        0, GRID_Y)]  # visited matrix for south
    W_visited = [[None for i in range(0, GRID_X)] for j in range(
        0, GRID_Y)]  # visited matrix for west
    E_visited = [[None for i in range(0, GRID_X)] for j in range(
        0, GRID_Y)]  # visited matrix for east

    visited_directory = {N: N_visited,
                         S: S_visited, E: E_visited, W: W_visited}

    movements = bot.controls()

    #order movements in order of cost
    costed_movements = [(costing(f), f) for f in movements]

    #sorts and try the movements in order of cost
    ordered_movements = sorted(costed_movements, key=lambda tup: tup[0])

    start = bot.pos
    explore = list()

    p = path()
    p.add(start)

    hcost = euc_dist(start.grid.get(), goal.grid.get())
    p.update_hcost(hcost)  # heuristic

    explore.append(p)  # 1 element so don't need to heapify
    # bot.move(start)

    while explore:
        p = heapq.heappop(explore)
        bot.move(p.last())

        if p.last() == goal: 
            print("FOUND GOAL")
            return p

        for cost, f in ordered_movements:

            if f.__name__ in ['forward', 'back']:
                if bot.check_obstacle(f().grid, obstacles):
                    continue

            elif f.__name__ in ['left', 'backleft', 'right', 'backright']:
                if not bot.turning_clear(f, obstacles):
                    continue  # if not clear

            else:
                print(f"{f.__name__} is not a valid movement")
                raise Exception("Unexpected movement function received")

            newnode = f()

            # if strictness is true, do tight check, if not - do loose check
            if strictness:
                oob_check = bot.tight_oob(newnode.grid)
            else:
                oob_check = bot.oob(newnode.grid)

            # grid to visit is not out of bounds nor it has been visited (includes orientation)
            if not (oob_check) and \
                    not visited_directory[newnode.direction.get()][newnode.grid.y - 1][newnode.grid.x - 1]:
                # print(p.get(), f.__name__)
                new_p = path() + p  # copy old path
                new_p.add(newnode)
                new_p.update_hcost(
                    euc_dist(newnode.grid.get(), goal.grid.get()))
                new_p.add_move(f)
                new_p.add_cost(costing(f))

                visited_directory[newnode.direction.get()][newnode.grid.y - 1][newnode.grid.x - 1] = new_p
                heapq.heappush(explore, new_p)

            else:
                continue

    print("A-STAR COULDN'T FIND PATH")
    return None # returns Nothing because no path


def naive(bot, goal):

    print("Executing naive algorithm for %s to %s" %
          (bot.pos.get(), goal.get()))

    movements = bot.controls()
    start = bot.pos
    explore = list()
    p = path()
    p.add(start)
    explore.append(p)
    bot.move(start)

    while explore:
        for p in explore:
            for f in movements:
                bot.move(p.last())
                newnode = f()
                if not bot.oob(newnode.grid):
                    # print(p.get())
                    new_p = path() + p  # copy old path
                    new_p.add(newnode)
                    new_p.add_move(f)
                    if new_p.last().get() == goal.get():
                        print("FOUND GOAL")
                        bot.move(goal)
                        return new_p

                    else:
                        explore.append(new_p)

                else:
                    continue

            explore.remove(p)  # remove object from list by reference
        # try a new path


# djikstra - idea to do it before i forget:
''' populate statespace and then solve shortest path to every node until goal state found
20 * 20 means 400 possible positions and 4 orientations mean 1600 possible states
this means computation shouldn't be too bad hopefully.
'''

# TESTING #
if __name__ == "__main__":
    # li = list((4,2,1,5,3))

    # heapq.heapify(li)

    # heapq.heappush(li, 0)

    # lel = heapq.heappop(li)

    # print(lel)

    # print(li)

    start = node(pair(1, 1), pair(0, 1))

    test = node(pair(9, 8), pair(0, 1))

    bot = robot(start, 3)

    pathfound = astar(bot, test)
    print(pathfound.get())
    print(pathfound.get_moves())
