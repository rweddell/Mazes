
from queue import PriorityQueue as pq
from Foundations.Cell import Cell
from Foundations.Distances import Distances


class WeightedCell(Cell):

    def __init__(self, row, column):
        super().__init__(row, column)
        self.weight = 1

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.weight == other.weight
        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.weight < other.weight
        return False

    def __str__(self):
        return 'WtCell ' + str(self.row) + ',' + str(self.column)

    def __hash__(self):
        return hash(self.__str__())

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.weight > other.weight
        return False

    def __repr__(self):
        return 'WtCell: ' + str(self.row) + ' ' + str(self.column)

    def get_distances(self):
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
