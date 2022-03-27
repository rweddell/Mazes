
from foundations.grid import Grid
from algorithms.sidewinder import Sidewinder
import random


larry = Sidewinder()	
	
grid = larry.on(Grid(5, 5))

print(grid)
