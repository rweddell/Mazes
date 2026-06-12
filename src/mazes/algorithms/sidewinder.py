from random import randint, choice
from mazes.algorithms.maze_algorithm import MazeAlgorithm

class Sidewinder(MazeAlgorithm):

	def on(self, grid):
		for line in grid.each_row():
			run = []
			for cell in line:
				run.append(cell)
				forward, up = self._directions(cell)
				east_bound = forward is None
				north_bound = up is None
				should_close = east_bound or (not north_bound and randint(0, 2) == 0)
				if should_close:
					member = choice(run)
					_, member_up = self._directions(member)
					if member_up is not None:
						member.link(member_up)
				else:
					cell.link(forward)
				run.clear()
		return grid

	@staticmethod
	def _directions(cell):
		"""Return (forward, up) for a cell.

		Rectangular grids use east/north; polar grids use clockwise/inward.
		A polar ring's clockwise neighbor wraps back to column 0, so that wrap
		is treated as no-forward (the seam), mirroring a rectangular east edge.
		"""
		if hasattr(cell, 'inward'):  # polar cell
			cw = cell.cw if (cell.cw is not None and cell.cw.column > cell.column) else None
			return cw, cell.inward
		return cell.east, cell.north
