
from Foundations.DistanceGrid import DistanceGrid
from Foundations.WeightedCell import WeightedCell
from random import choice


class WeightedGrid(DistanceGrid):

    def __init__(self, rows, columns):
        super(DistanceGrid, self).__init__(rows, columns)

    def __str__(self):
        return 'WeightedGrid: (' + str(self.rows) + ', ' + str(self.columns) + ')'

    def __repr__(self):
        return self.__str__()

    def set_distances(self, distances):
        self.distlist = distances
        self.farthest, self.maximum = distances.max_path()

    def prepare_grid(self):
        grid = [[WeightedCell(x, y) for y in range(self.columns)] for x in range(self.rows)]
        return grid

    def bg_color(self, cell):
        if cell.weight > 1:
            return (255, 0, 0)
        elif self.distances:
            distance = self.distlist[cell] if self.distlist[cell] else None
            if distance is None:
                return None
            else:
                intensity = int(64 + 191 * (self.maximum - distance)/self.maximum)
                return (intensity, intensity, 0)

    def random_dist(self):
        cells = list(self.distlist.keys())
        return choice(cells)
