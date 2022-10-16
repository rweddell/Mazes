
from maze_structures.polar_grid import PolarGrid
from maze_algorithms.recursive_backtrack import RecursiveBacktracker
from datetime import date

polly = PolarGrid(8)
albert = RecursiveBacktracker()
grid = albert.on(polly)
img = grid.to_png(cellsize=30)
today = date.today()
img.save(f'output\circle_maze_{today}.png')