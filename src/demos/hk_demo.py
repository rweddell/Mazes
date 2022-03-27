
from algorithms.hunt_and_kill import HuntAndKill as hk
from foundations.grid import Grid

jeremy = hk()

grid = jeremy.on(Grid(20, 20))

img = grid.to_png()

img.save("output\hk1.png")
