
"""
Creates a simple solution to a maze using 
Dijkstra's algorithm.

Becomes really ugle with grids larger than 5x5
because of ASCII representation depending on length
of path/solution
"""

from Foundations.DistanceGrid import DistanceGrid
from Algorithms.AldousBroder import AldousBroder
from Algorithms.RecursiveBacktracker import RecursiveBacktracker as rb

larry = rb()

grid = larry.on(DistanceGrid(10, 10))
 
start = grid.grid[0][0]
distances = start.get_distances()

grid.distlist = distances
print(grid.__str__())

print("Path from NW to SE")
grid.distlist = distances.path_to(grid[grid.rows-1][grid.columns-1])

print(grid.__str__())
