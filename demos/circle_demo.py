
from maze_structures.polar_grid import PolarGrid
from maze_algorithms.recursive_backtrack import RecursiveBacktracker
from datetime import date

albert = RecursiveBacktracker()
grid = albert.on(PolarGrid(8))
img = grid.to_png(cellsize=30)
today = date.today()
img.save(f'output\circle_maze_{today}.png')