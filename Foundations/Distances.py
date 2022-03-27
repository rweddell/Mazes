
class Distances:

    def __init__(self, root):
        self.root = root
        self.cells = dict()
        self.cells[root] = 0
        self.max_path()
        self.max_dist = 0

    def __getitem__(self, item):
        if item in self.cells.keys():
            return self.cells[item]
        else:
            return None

    def __setitem__(self, key, value):
        self.cells[key] = value

    def keys(self):
        return list(self.cells.keys())

    # TODO: make this a static method
    def path_to(self, goal):
        current = goal
        path = Distances(self.root)
        path[current] = self.cells[current]
        while current != self.root:
            for neighbor in current.links:
                if self.cells[neighbor] < self.cells[current]:
                    path[neighbor] = self.cells[neighbor]
                    current = neighbor
                    break
        return path
    
    def max_path(self):
        """
        Finds the farthest cell from self.root
        :return: (Farthest cell, cell's distance)
        """
        max_dist = 0
        max_cell = self.root
        for cell in self.cells.keys():
            if self.cells[cell] > max_dist:
                max_cell = cell
                max_dist = self.cells[cell]
        self.max_dist = max_dist
        return max_cell, max_dist
