from maze_structures.color_polar import ColoredPolar
from maze_structures.color_grid import ColoredGrid
from maze_algorithms.recursive_backtrack import *
from maze_algorithms.sidewinder import Sidewinder
from maze_structures import mask, color_mask
from datetime import date

algo = RecursiveBacktracker()

grid = algo.on(ColoredGrid(20, 20))
start = grid.grid[round(grid.rows/2)][round(grid.columns/2)]
grid.set_distances(start.get_distances())
filename = f".output\color_maze{date.today()}.png"
img = grid.to_png()
img.save(filename)

circle = algo.on(ColoredPolar(8))
other = circle[round(circle.rows/2)][1]
circle.set_distances(other.get_distances())
img = circle.to_png(cellsize=20)
img.save(f'.output\color_circle{date.today()}.png')

current_mask = mask.from_png_scaled('.output\maze_img.png')
grid = algo.on(color_mask.ColoredMask(current_mask))
facestart = grid.random_cell()
grid.set_distances(facestart.get_distances())
smallimg = grid.to_png(size=10)
smallimg.save(f'.output\maze_color{date.today()}.png')
