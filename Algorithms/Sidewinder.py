
import random

class Sidewinder():
	
	def on(self, grid):
		for line in grid.each_row():
			run = []
			for cell in line:
				run.append(cell)
				east_bound = cell.east == None
				north_bound = cell.north == None
				should_close = east_bound or (not north_bound and random.randint(0,2) == 0)
				if should_close:
					member = random.choice(run)
					if member.north != None:
						member.link(member.north)
				else:
					cell.link(cell.east)
				run.clear()
		return grid
		