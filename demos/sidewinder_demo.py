
from maze_structures.grid import Grid
from maze_algorithms.sidewinder import Sidewinder
import random


larry = Sidewinder()	
	
grid = larry.on(Grid(5, 5))

print(grid)
