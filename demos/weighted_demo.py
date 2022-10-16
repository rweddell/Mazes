from maze_structures.weighted_grid import WeightedGrid
from maze_algorithms.recursive_backtrack import RecursiveBacktracker as rb

chester = rb()
grid = chester.on(WeightedGrid(10, 10))

grid.braid(0.5)
print('braided')

start, finish = grid[0][0], grid[grid.rows-1][grid.columns-1]
print('started')
dists = start.get_distances()
grid.set_distances(dists)

img = grid.to_png()
img.save('output\weightedmaze.png')
print('done with one')

lava = grid.random_dist()
lava.weight = 50
print('made lava')

grid.set_distances(start.get_distances().path_to(finish))
print('got distances')

img2 = grid.to_png()
img2.save('output\astar.png')
