
from Foundations.Cell import *

class PolarCell(Cell):

    def __init__(self, row, column):
        super().__init__(row, column)
        self.outward = []
        self.cw = None
        self.ccw = None
        self.inward = None

    def get_cw(self):
        return self.cw

    def get_ccw(self):
        return self.ccw

    def set_cw(self, value):
        self.cw = value

    def set_ccw(self, value):
        self.ccw = value

    def set_inward(self, value):
        self.inward = value

    def get_inward(self):
        return self.inward

    def neighbors(self):
        nlist = []
        if self.cw: nlist.append(self.cw)
        if self.ccw: nlist.append(self.ccw)
        if self.inward: nlist.append(self.inward)
        nlist += self.outward
        return nlist
