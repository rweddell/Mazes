from abc import abstractclassmethod
from random import choice


class MazeAlgorithm:

    @abstractclassmethod
    def on(self, grid):
        pass


class AldousBroder(MazeAlgorithm):
    
    def on(self, grid):
        cell = grid.random_cell()
        unvisited = grid.size - 1
        
        while unvisited > 0:
            neighbor = choice(cell.neighbors())
            if len(neighbor.links) == 0:
                cell.link(neighbor)
                unvisited -= 1
            cell = neighbor
        return grid


class BinaryTree(MazeAlgorithm):

    def on(self, grid):
        for row in grid.grid:
            for cell in row:
                near = []
                if cell.north:
                    near.append(cell.north)
                if cell.east:
                    near.append(cell.east)
                if near:
                    chosen = choice(near)
                    cell.link(chosen)
        return grid


class HuntAndKill(MazeAlgorithm):

    def on(self, grid):
        current = grid.random_cell()
        while current:
            unvisited = [neighbor for neighbor in current.neighbors() if not neighbor.links]
            if unvisited:
                neighbor = choice(unvisited)
                current.link(neighbor)
                current = neighbor
            else:
                current = None
                for cell in grid.each_cell():
                    visited = [neighbor for neighbor in cell.neighbors() if neighbor.links]
                    if not cell.links and visited:
                        current = cell
                        tolink = choice(visited)
                        current.link(tolink)
        return grid


class RecursiveBacktracker(MazeAlgorithm):

    def on(self, grid, start=None):
        if start is None:
            start = grid.random_cell()
        stack = list()
        stack.append(start)
        while stack:
            current = stack[-1]
            neighbors = [neighbor for neighbor in current.neighbors() if not neighbor.links]
            if neighbors:
                neighbor = choice(neighbors)
                current.link(neighbor)
                stack.append(neighbor)
            else:
                stack.pop(-1)
        return grid


class Sidewinder(MazeAlgorithm):
	
	def on(self, grid):
		for line in grid.each_row():
			run = []
			for cell in line:
				run.append(cell)
				east_bound = cell.east == None
				north_bound = cell.north == None
				should_close = east_bound or (not north_bound and randint(0,2) == 0)
				if should_close:
					member = choice(run)
					if member.north != None:
						member.link(member.north)
				else:
					cell.link(cell.east)
				run.clear()
		return grid


class Wilsons(MazeAlgorithm):

    def on(self, grid):
        unvisited = []
        for cell in grid.each_cell():
            unvisited.append(cell)
        first = choice(unvisited)
        unvisited.remove(first)
        while unvisited:
            cell = choice(unvisited)
            path = [cell]
            while cell in unvisited:
                cell = choice(cell.neighbors())
                try:
                    position = path.index(cell)
                    path = path[:position+1]
                except ValueError:
                    path.append(cell)
            for i in range(0, path.__len__()-1):
                path[i].link(path[i+1])
                unvisited.remove(path[i])
        return grid
       