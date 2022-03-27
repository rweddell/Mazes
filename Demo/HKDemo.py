
from Algorithms.HuntAndKill import HuntAndKill as hk
from Foundations.Grid import Grid

jeremy = hk()

grid = jeremy.on(Grid(20, 20))

img = grid.to_png()

img.save("Output\hk1.png")
