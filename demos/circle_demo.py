
from maze_structures.polar_grid import PolarGrid
from maze_algorithms.recursive_backtrack import RecursiveBacktracker

albert = RecursiveBacktracker()
grid = albert.on(PolarGrid(8))
img = grid.to_png(cellsize=30)
img.save('output\circle_maze.png')