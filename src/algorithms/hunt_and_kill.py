
from random import choice

class HuntAndKill:

    def on(self, grid):
        current = grid.random_cell()
        while current:
            unvisited = [neighbor for neighbor in current.neighbors() if not neighbor.links]
            if unvisited:
                neighbor = choice(unvisited)
                current.link(neighbor)
                current = neighbor
            else:
                current = None
                for cell in grid.each_cell():
                    visited = [neighbor for neighbor in cell.neighbors() if neighbor.links]
                    if not cell.links and visited:
                        current = cell
                        tolink = choice(visited)
                        current.link(tolink)
        return grid
