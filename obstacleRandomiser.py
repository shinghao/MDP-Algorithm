import random
import Constants

LEGAL_DIST_BTW_OBS = 6
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

    while len(obstacles) < n:
        x = random.randint(1, Constants.GRID_NUM)
        y = random.randint(1, 20)
        dir = random.choice(directions)

        # Skip if position already occupied or is already deemed illegal
        if any((x, y) == (o[0], o[1]) for o in obstacles) or (x, y, dir) in illegal:
            print("Illegal -", (x, y, dir))
            continue

        # Add x,y,dir combination to illegal list
        illegal.append((x, y, dir))

        x_dir = x + dir[0] * LEGAL_DIST_FROM_BORDER
        y_dir = y + dir[1] * LEGAL_DIST_FROM_BORDER

        # Illegal 1 - If obstacle is <= 6 blocks from border and facing direction of border
        if not 1 <= x_dir <= Constants.GRID_NUM or not 1 <= y_dir <= Constants.GRID_NUM:
            print("Illegal -", (x, y, dir), x_dir, y_dir,
                  "obstacle facing border and <= 6 blocks from border")
            continue

        # Illegal 2 - If obstacle is at border and not facing away from border
        if not 1 < x + dir[0] < 20 or not 1 < y + dir[1] < 20:
            print("Illegal -", (x, y, dir),
                  "obstacle at border and not facing away from border")
            continue

        # Illegal 3 - Check if there are any obstacles in the direction of the obstacle
        if dir == Constants.N:
            if any((x, y+i) in [(o[0], o[1]) for o in obstacles] for i in range(1, 7)):
                print("Illegal -", (x, y, dir),
                      "obstacle facing another obstacle")
                continue
        elif dir == Constants.S:
            if any((x, y-i) in [(o[0], o[1]) for o in obstacles] for i in range(1, 7)):
                print("Illegal -", (x, y, dir),
                      "obstacle facing another obstacle")
                continue
        elif dir == Constants.E:
            if any((x+i, y) in [(o[0], o[1]) for o in obstacles] for i in range(1, 7)):
                print("Illegal -", (x, y, dir),
                      "obstacle facing another obstacle")
                continue
        elif dir == Constants.W:
            if any((x-i, y) in [(o[0], o[1]) for o in obstacles] for i in range(1, 7)):
                print("Illegal -", (x, y, dir),
                      "obstacle facing another obstacle")
                continue

        legal = True
        # check to see if this newly generated obstacle will block any currently exisitng obstacles

        for o in obstacles:
            if o[2] == Constants.N:
                if x == o[0] and y > o[1] and y - o[1] <= LEGAL_DIST_BTW_OBS:
                    print("Illegal -", (x, y, dir),
                          "obstacle facing another obstacle")
                    legal = False
                    continue

            elif o[2] == Constants.S:
                if x == o[0] and y < o[1] and o[1] - y <= LEGAL_DIST_BTW_OBS:
                    print("Illegal -", (x, y, dir),
                          "obstacle facing another obstacle")
                    legal = False
                    continue

            elif o[2] == Constants.E:
                if y == o[1] and x > o[0] and x - o[0] <= LEGAL_DIST_BTW_OBS:
                    print("Illegal -", (x, y, dir),
                          "obstacle facing another obstacle")
                    legal = False
                    continue

            elif o[2] == Constants.W:
                if y == o[1] and x < o[0] and o[0] - x <= LEGAL_DIST_BTW_OBS:
                    print("Illegal -", (x, y, dir),
                          "obstacle facing another obstacle")
                    legal = False
                    continue

        if legal:
            obstacles.append((x, y, dir))

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
			dir = random.choice([N, E, S, W])
			if (x, y) not in selected:
				selected.append((x, y))
				check = pair(x, y) + pair(*dir)*3
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
							check = pair(x, y) + pair(*dir)*i
							if abs(check.x - a) <= 1 and abs(check.y - b) <= 1:
								clear = False
								break

						if (clear == False):
							break

					if clear:
						obstacles.append((x, y, dir))
						new = True
	print(obstacles)
	return obstacles
 """
