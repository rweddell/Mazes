
from mazes.algorithms.recursive_backtrack import RecursiveBacktracker
from mazes.structures.grid import Grid

recbac = RecursiveBacktracker()

grid = recbac.on(Grid(20,20))

img = grid.to_png()
img.save('output\recback.png')