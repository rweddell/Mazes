from abc import abstractclassmethod
from random import choice


class MazeAlgorithm:

    @abstractclassmethod
    def on(self, grid):
        pass
