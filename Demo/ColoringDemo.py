
from Foundations.ColoredPolar import ColoredPolar
from Foundations.ColoredGrid import ColoredGrid
from Algorithms.RecursiveBacktracker import *
from Algorithms.Sidewinder import Sidewinder
from Foundations import Mask, ColoredMask

george = RecursiveBacktracker()

grid = george.on(ColoredGrid(20, 20))
start = grid.grid[round(grid.rows/2)][round(grid.columns/2)]
grid.set_distances(start.get_distances())
filename = "Output\coloredmaze.png"
img = grid.to_png()
img.save(filename)

circle = george.on(ColoredPolar(8))
other = circle[round(circle.rows/2)][1]
circle.set_distances(other.get_distances())
img = circle.to_png(cellsize=20)
img.save('Output\colorcircle.png')

mask = Mask.from_png_scaled('Output\mazeimg.png')
grid = george.on(ColoredMask.ColoredMask(mask))
facestart = grid.random_cell()
grid.set_distances(facestart.get_distances())
smallimg = grid.to_png(size=10)
smallimg.save('Output\mazecolor.png')
