
from mazes.structures.grid import Grid
from mazes.algorithms.sidewinder import Sidewinder
import random


larry = Sidewinder()	
	
grid = larry.on(Grid(5, 5))

print(grid)
