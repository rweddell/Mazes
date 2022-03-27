
from algorithms.recursive_backtrack import RecursiveBacktracker
from foundations.grid import Grid

recbac = RecursiveBacktracker()

grid = recbac.on(Grid(20,20))

img = grid.to_png()
img.save('output\recback.png')