
from mazes.structures.grid import Grid
from mazes.algorithms.hunt_and_kill import HuntAndKill as hk

jeremy = hk()

grid = jeremy.on(Grid(20, 20))

img = grid.to_png()

img.save("output\hk1.png")
