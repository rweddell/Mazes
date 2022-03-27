from Foundations.Grid import Grid
from Algorithms.BinaryTree import BinaryTree
from Algorithms.Sidewinder import Sidewinder
from Algorithms.AldousBroder import AldousBroder
from Algorithms.Wilsons import Wilsons
from Algorithms.HuntAndKill import HuntAndKill

algorithms = [BinaryTree, Sidewinder, AldousBroder, Wilsons, HuntAndKill]

tries = 100
size = 20

averages = {}
for alg in algorithms:
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

for alg in algorithms:
    percentage = (averages[alg]*100.0)/total_cells
    print("{} : {}/{} ({}%)".format(alg, averages[alg], total_cells, percentage))
