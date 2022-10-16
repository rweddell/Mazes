from random import choice
from maze_algorithms.maze_algorithm import MazeAlgorithm
# from maze_algorithms import MazeAlgorithm

class AldousBroder(MazeAlgorithm):
    
    def on(self, grid):
        cell = grid.random_cell()
        unvisited = grid.size - 1
        
        while unvisited > 0:
            neighbor = choice(cell.neighbors())
            if len(neighbor.links) == 0:
                cell.link(neighbor)
                unvisited -= 1
            cell = neighbor
        return grid
