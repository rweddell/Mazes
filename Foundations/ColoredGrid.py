
from Foundations.Grid import Grid

class ColoredGrid(Grid):

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.farthest = None
        self.max_dist = None
        self.distlist = None

    def set_distances(self, distances):
        self.distlist = distances
        self.farthest, self.max_dist = distances.max_path()

    def bg_color(self, cell):
        distance = self.distlist[cell]
        intensity = (self.max_dist - distance)/self.max_dist
        dark = round(255 * intensity)
        bright = 128 + round(127 * intensity)
        return (dark, bright, dark)
