
from algorithms.wilson import Wilsons
from foundations.grid import Grid

wilson = Wilsons()

grid = wilson.on(Grid(20, 20))

img = grid.to_png()

img.save("output\wilson.png")