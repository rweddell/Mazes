from maze_algorithms.wilson import Wilsons
from maze_structures.grid import Grid

wilson = Wilsons()

grid = wilson.on(Grid(20, 20))

img = grid.to_png()

img.save("output\wilson.png")