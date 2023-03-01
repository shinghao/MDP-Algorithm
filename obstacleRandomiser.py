import math
import random
import Constants

LEGAL_DIST_BTW_OBS = 7
LEGAL_DIST_FROM_BORDER = 6


def random_obstacles(n):

    directions = [Constants.N, Constants.E, Constants.S, Constants.W]
    obstacles = list()
    illegal = list()

    # Start box + 3 above startbox is illegal for obstacles
    for i in range(1, 5):
        for j in range(1, 8):
            for d in directions:
                illegal.append((i, j, d))

    for i in range(0, n):
        new = False
        for t in range(1, 20):
            x = random.choice(range(1, Constants.GRID_NUM))
            y = random.choice(range(1, Constants.GRID_NUM))
            z = random.choice(directions)

            # Skip if position already occupied or is already deemed illegal
            if any((x, y) == (o[0], o[1]) for o in obstacles) or (x, y, z) in illegal:
                print("Illegal -", (x, y, z))
                continue

            # Add x,y,z combination to illegal list
            illegal.append((x, y, z))

            x_dir = x + z[0] * LEGAL_DIST_FROM_BORDER
            y_dir = y + z[1] * LEGAL_DIST_FROM_BORDER

            # Illegal 1 - If obstacle is <= 3 blocks from border and facing direction of border
            if not 1 <= x_dir <= Constants.GRID_NUM or not 1 <= y_dir <= Constants.GRID_NUM:
                print("Illegal -", (x, y, z), x_dir, y_dir,
                      "obstacle is <= 6 blocks from border and facing direction of border")
                continue

            valid = True

            # Illegal 2 - If obstacle <= 6 blocks from any other obstacle and facing direction of obstacle
            for a, b, c in obstacles:
                if not abs(x - a) >= abs(z[0] * LEGAL_DIST_BTW_OBS) or not abs(y - b) >= abs(z[1] * LEGAL_DIST_BTW_OBS):
                    valid = False
                    break

                    # If valid -> Add to obstacle list
            if valid:
                obstacles.append((x, y, z))
                new = True

    print(obstacles)
    return obstacles


""" def random_obstacles(n):

	obstacles = list()
	selected = list()

	for i in range(0, n):

		new = False

		while not new:
			x = random.choice(range(1, GRID_X))
			y = random.choice(range(1, GRID_Y))
			z = random.choice([N, E, S, W])
			if (x, y) not in selected:
				selected.append((x, y))
				check = pair(x, y) + pair(*z)*3
				if not 0 < check.x <= 17 or not 0 < check.y <= 17:
					# this obstacle is illegal
					continue

				else:
					clear = True
					for a, b, c in obstacles:

						for i in range(0, 5):
							# no new obstacle within 5 units of an obstacle's image facing direction
							check = pair(a, b) + pair(*c)*i
							if abs(check.x - x) <= 1 and abs(check.y - y) <= 1:
								clear = False
								break

						if (clear == False):
							break

						# check that no obstacles within this new obstacle line of sight also
						for i in range(0, 5):
							# no new obstacle within 5 units of an obstacle's image facing direction
							check = pair(x, y) + pair(*z)*i
							if abs(check.x - a) <= 1 and abs(check.y - b) <= 1:
								clear = False
								break

						if (clear == False):
							break

					if clear:
						obstacles.append((x, y, z))
						new = True
	print(obstacles)
	return obstacles
 """
