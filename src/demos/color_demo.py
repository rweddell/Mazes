
from foundations.color_polar import ColoredPolar
from foundations.color_grid import ColoredGrid
from algorithms.recursive_backtrack import *
from algorithms.sidewinder import Sidewinder
from foundations import mask, color_mask

algo = RecursiveBacktracker()

grid = algo.on(ColoredGrid(20, 20))
start = grid.grid[round(grid.rows/2)][round(grid.columns/2)]
grid.set_distances(start.get_distances())
filename = "output\color_maze.png"
img = grid.to_png()
img.save(filename)

circle = algo.on(ColoredPolar(8))
other = circle[round(circle.rows/2)][1]
circle.set_distances(other.get_distances())
img = circle.to_png(cellsize=20)
img.save('output\color_circle.png')

current_mask = mask.from_png_scaled('output\maze_img.png')
grid = algo.on(color_mask.ColoredMask(current_mask))
facestart = grid.random_cell()
grid.set_distances(facestart.get_distances())
smallimg = grid.to_png(size=10)
smallimg.save('output\maze_color.png')
