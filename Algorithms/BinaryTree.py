
import random


class BinaryTree():

    def on(self, grid):
        for row in grid.grid:
            for cell in row:
                near = []
                if cell.north is not None:
                    near.append(cell.north)
                if cell.east is not None:
                    near.append(cell.east)
                if near:
                    chosen = random.choice(near)
                    cell.link(chosen)
        return grid
