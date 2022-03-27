
import maze_structures.base36 as Base36
from maze_structures.grid import Grid


class DistanceGrid(Grid):

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.farthest = None
        self.maximum = None
        self.distlist = {}

    def distances(self, distances):
        self.distlist = distances
        self.farthest, self.maximum = distances.max_path()

    def contents_of(self, cell):
        if self.distlist and cell in self.distlist.keys():
            return Base36.encode(self.distlist[cell])
        else:
            return super().contents_of(cell)
