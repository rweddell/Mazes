
from foundations.polar_grid import PolarGrid
from algorithms.recursive_backtrack import RecursiveBacktracker

albert = RecursiveBacktracker()
grid = albert.on(PolarGrid(8))
img = grid.to_png(cellsize=30)
img.save('output\circle_maze.png')