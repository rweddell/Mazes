
from Foundations.PolarGrid import PolarGrid
from Algorithms.RecursiveBacktracker import RecursiveBacktracker

albert = RecursiveBacktracker()
grid = albert.on(PolarGrid(6))
img = grid.to_png(cellsize=30)
img.save('Output\circlemaze.png')