
from Foundations.ColoredGrid import ColoredGrid
from Foundations.MaskedGrid import MaskedGrid

class ColoredMask(MaskedGrid, ColoredGrid):

    def __init__(self, newmask):
        self.mask = newmask
        super().__init__(newmask)
        self.farthest = None
        self.max_dist = None
        self.distlist = None
