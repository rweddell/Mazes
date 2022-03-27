
from Algorithms.RecursiveBacktracker import RecursiveBacktracker
from Foundations.Grid import Grid

recbac = RecursiveBacktracker()

grid = recbac.on(Grid(20,20))

img = grid.to_png()
img.save('Output\recback.png')