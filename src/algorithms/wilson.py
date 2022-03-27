
from random import choice


class Wilsons:

    def on(self, grid):
        unvisited = []
        for cell in grid.each_cell():
            unvisited.append(cell)
        first = choice(unvisited)
        unvisited.remove(first)
        while unvisited:
            cell = choice(unvisited)
            path = [cell]
            while cell in unvisited:
                cell = choice(cell.neighbors())
                try:
                    position = path.index(cell)
                    path = path[:position+1]
                except ValueError:
                    path.append(cell)
            for i in range(0, path.__len__()-1):
                path[i].link(path[i+1])
                unvisited.remove(path[i])
        return grid
