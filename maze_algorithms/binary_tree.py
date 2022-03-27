from random import choice
from maze_algorithms.maze_algorithm import MazeAlgorithm


class BinaryTree(MazeAlgorithm):

    def on(self, grid):
        for row in grid.grid:
            for cell in row:
                near = []
                if cell.north is not None:
                    near.append(cell.north)
                if cell.east is not None:
                    near.append(cell.east)
                if near:
                    chosen = choice(near)
                    cell.link(chosen)
        return grid
