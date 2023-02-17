from griddyworld import *

def naive(bot, goal):
	movements = bot.controls()
	print("Executing naive algorithm for %s to %s" %(bot.pos.get(),goal.get()))
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
					#print(p.get())
					new_p = path() + p # copy old path
					new_p.moves
					new_p.add(newnode)
					new_p.add_move(f.__name__)
					if new_p.last().get() == goal.get():
						print("FOUND GOAL")
						bot.move(goal)
						return new_p

					else:
						explore.append(new_p)

				else: continue

			explore.remove(p) # remove object from list by reference
		# try a new path

# djikstra - idea to do it before i forget:
''' populate statespace and then solve shortest path to every node until goal state found
20 * 20 means 400 possible positions and 4 orientations mean 1600 possible states
this means computation shouldn't be too bad hopefully.
'''
