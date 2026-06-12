from random import choice
from mazes.algorithms.maze_algorithm import MazeAlgorithm


class BinaryTree(MazeAlgorithm):

    def on(self, grid):
        for row in grid.grid:
            for cell in row:
                near = self._candidates(cell)
                if near:
                    chosen = choice(near)
                    cell.link(chosen)
        return grid

    @staticmethod
    def _candidates(cell):
        """North/East on a rectangular grid; inward/clockwise on a polar grid.

        On a polar ring the clockwise neighbor wraps back to column 0, which
        would let a ring close into a loop. Excluding that wrap leaves one
        "seam" cell per ring forced inward — the polar analog of the east edge.
        """
        if hasattr(cell, 'inward'):  # polar cell
            near = []
            if cell.inward is not None:
                near.append(cell.inward)
            if cell.cw is not None and cell.cw.column > cell.column:
                near.append(cell.cw)
            return near
        near = []
        if cell.north is not None:
            near.append(cell.north)
        if cell.east is not None:
            near.append(cell.east)
        return near
