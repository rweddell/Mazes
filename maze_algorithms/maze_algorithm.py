from abc import abstractclassmethod


class MazeAlgorithm:

    def __init__(self) -> None:
        pass

    @abstractclassmethod
    def on(self, grid):
        pass