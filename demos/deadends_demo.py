import chunk
from maze_structures.grid import Grid
from maze_algorithms.binary_tree import BinaryTree
from maze_algorithms.sidewinder import Sidewinder
from maze_algorithms.aldous_broder import AldousBroder
from maze_algorithms.wilson import Wilsons
from maze_algorithms.hunt_and_kill import HuntAndKill

algos= [BinaryTree, Sidewinder, AldousBroder, Wilsons, HuntAndKill]

tries = 100
size = 20

averages = {}
for alg in algos:
    print("Running:  " + str(alg))
    dead_counts = []
    for i in range(0, tries):
        thing = alg()
        grid = thing.on(Grid(size, size))
        dead_counts.append(grid.deadends())
    total_dead = 0
    for i in range(0, len(dead_counts)-1):
        total_dead += dead_counts[i]
    averages[alg] = round(total_dead/grid.size)

total_cells = size*size
print()
print("Average dead-ends per " + str(size) + "x" + str(size) + " maze")
print()

#sorted_algs = sorted(algorithms)

for alg in algos:
    percentage = (averages[alg]*100.0)/total_cells
    print("{} : {}/{} ({}%)".format(alg, averages[alg], total_cells, percentage))
