
from Foundations.Distances import Distances

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
        
    def get_distances(self):
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
