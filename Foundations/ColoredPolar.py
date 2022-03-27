
from Foundations.PolarGrid import PolarGrid
from Foundations.ColoredGrid import ColoredGrid


class ColoredPolar(PolarGrid, ColoredGrid):

    def __init__(self, rows):
        PolarGrid.__init__(self, rows)
        self.farthest = None
        self.max_dist = None
        self.distlist = None

    def set_distances(self, distances):
        self.distlist = distances
        self.farthest, self.max_dist = distances.max_path()

    def bg_color(self, cell):
        distance = self.distlist[cell]
        intensity = (self.max_dist - distance) / self.max_dist
        dark = round(255 * intensity)
        bright = 128 + round(127 * intensity)
        return (bright, dark, bright)
