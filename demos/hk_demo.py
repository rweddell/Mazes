
from maze_algorithms.hunt_and_kill import HuntAndKill as hk
from maze_structures.grid import Grid

jeremy = hk()

grid = jeremy.on(Grid(20, 20))

img = grid.to_png()

img.save("output\hk1.png")
