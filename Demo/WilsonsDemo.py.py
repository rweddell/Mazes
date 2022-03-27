
from Algorithms.Wilsons import Wilsons
from Foundations.Grid import Grid

wilson = Wilsons()

grid = wilson.on(Grid(20, 20))

img = grid.to_png()

img.save("Output\wilson.png")