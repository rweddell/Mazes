from queue import PriorityQueue as pq
from maze_structures.distances import Distances

class Cell(object):

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.links = {}

    def __str__(self):
        return "(" + str(self.row) + ", " + str(self.column) + ")"

    def __hash__(self):
        return hash(self.__str__())

    def __repr__(self):
        return "Cell" + self.__str__()

    def link(self, cell, bidi=True):
        self.links[cell] = True
        if bidi:
            cell.link(self, False)

    def unlink(self, cell, bidi=True):
        del self.links[cell]
        if bidi:
            cell.unlink(self, False)

    def list_links(self):
        return self.links

    def is_linked(self, cell):
        if cell is not None:
            return cell in self.links.keys()
        else:
            return False

    def neighbors(self):
        nlist = []
        if self.north is not None:
            nlist.append(self.north)
        if self.south is not None:
            nlist.append(self.south)
        if self.east is not None:
            nlist.append(self.east)
        if self.west is not None:
            nlist.append(self.west)
        return nlist
        
    def get_distances(self) -> list[Distances]:
        """
        Collects distances from self to all other cells in maze
        :return: list of distances
        """
        distlist = Distances(self)
        frontier = [self]
        while frontier:
            new_frontier = []
            for current in frontier:
                for cell in current.links:
                    if cell in distlist.keys():
                        pass
                    else:
                        distlist[cell] = distlist[current] + 1
                        new_frontier.append(cell)    
            frontier = new_frontier
        return distlist


class WeightedCell(Cell):

    def __init__(self, row:int, column:int) -> None:
        super().__init__(row, column)
        self.weight = 1

    def __eq__(self, other:Cell) -> bool:
        if isinstance(other, self.__class__):
            return self.weight == other.weight
        return False

    def __lt__(self, other:Cell) -> bool:
        if isinstance(other, self.__class__):
            return self.weight < other.weight
        return False

    def __str__(self) -> str:
        return 'WtCell ' + str(self.row) + ',' + str(self.column)

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __gt__(self, other:Cell) -> bool:
        if isinstance(other, self.__class__):
            return self.weight > other.weight
        return False

    def __repr__(self) -> str:
        return 'WtCell: ' + str(self.row) + ' ' + str(self.column)

    def get_distances(self) -> list[Distances]:
        weights = Distances(self)
        pending = pq()
        pending.put(self)
        while pending.qsize() >= 1:
            cell = pending.get()
            for neighbor in cell.links:
                total_wt = weights[cell] + neighbor.weight
                if not weights[neighbor] or total_wt < weights[neighbor]:
                    pending.put(neighbor)
                    weights[neighbor] = total_wt
        return weights


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
