
from random import choice

class RecursiveBacktracker:

    def on(self, grid, start=None):
        if start is None:
            start = grid.random_cell()
        stack = list()
        stack.append(start)
        while stack:
            current = stack[-1]
            neighbors = [neighbor for neighbor in current.neighbors() if not neighbor.links]
            if neighbors:
                neighbor = choice(neighbors)
                current.link(neighbor)
                stack.append(neighbor)
            else:
                stack.pop(-1)
        return grid
