from maze_structures.grid import Grid
from maze_algorithms.aldous_broder import AldousBroder
from datetime import date

aldous = AldousBroder()
grid = aldous.on(Grid(10, 10))

# print(grid)

img = grid.to_png()
img.save(f"Output\aldous_image_{date.today()}.png")