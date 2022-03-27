
from foundations.grid import Grid
from algorithms.aldous_broder import AldousBroder


aldous = AldousBroder()
grid = aldous.on(Grid(10, 10))

# print(grid)

img = grid.to_png()
img.save("Output\aldous_image.png")