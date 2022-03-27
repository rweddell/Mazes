from abc import abstractclassmethod
from maze_algorithms.maze_algorithm import MazeAlgorithm


class MazeAlgorithm:

    def __init__(self) -> None:
        pass

    @abstractclassmethod
    def on(self, grid):
        pass