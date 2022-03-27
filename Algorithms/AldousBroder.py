
import random


class AldousBroder:
    
    def on(self, grid):
        cell = grid.random_cell()
        unvisited = grid.size - 1
        
        while unvisited > 0:
            neighbor = random.choice(cell.neighbors())
            if len(neighbor.links) is 0:
                cell.link(neighbor)
                unvisited -= 1
            cell = neighbor
        return grid
