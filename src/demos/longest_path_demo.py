
from foundations.distance_grid import DistanceGrid


grid = DistanceGrid(5, 5)
start = grid.grid[0][0]
distances = start.distances()
newstart, distance = distances.max_path()

newdist = newstart.distances()
goal, distance2 = newdist.max_path()
grid.distances = newdist.path_to(goal)

print(grid)