
from PIL import Image
from random import randint
from typing import List, Tuple  


class Mask:

    def __init__(self, rows:int, columns:int) -> None:
        self.rows = rows
        self.columns = columns
        self.bits = [[True for i in range(self.columns)] for j in range(self.rows)]

    def is_bit(self, row:int, column:int) -> bool:
        if row in range(0, self.rows) and column in range(0, self.columns):
            return self.bits[row][column]
        else:
            return False

    def set_bit(self, row:int, column:int, value:bool=True) -> None:
        self.bits[row][column] = value

    def count(self) -> int:
        total = 0
        for row in range(self.rows):
            for col in range(self.columns):
                if self.is_bit(row, col):
                    total += 1
        return total

    def __repr__(self) -> str:
        return f"({self.rows}, {self.columns})"

    def random_location(self) -> Tuple[int, int]:
        row = randint(0, self.rows - 1)
        col = randint(0, self.columns - 1)
        while not self.is_bit(row, col):
            row = randint(0, self.rows - 1)
            col = randint(0, self.columns - 1)
        return (row, col)

    def __str__(self) -> str:
        stringy = ''
        for row in self.bits:
            for bit in row:
                if bit is True:
                    stringy += 'x'
                else:
                    stringy += ' '
            stringy += '\n'
        return stringy


def from_txt(file:str) -> Mask:
    """
    :param file(location of file):
    :return: Mask object
    """
    with open(file) as f:
        lines = f.readlines()
    rows = len(lines)
    columns = max(len(line.rstrip('\n')) for line in lines)
    mask = Mask(rows, columns)
    for i in range(rows):
        for j in range(len(lines[i].rstrip('\n'))):
            if lines[i][j] == 'x':
                mask.set_bit(i, j, False)
    return mask


def from_png(file:str) -> Mask:
    """
    Mask object based on non-black pixel values of the png
    :param file:
    :return:
    """
    img = Image.open(file)
    rows, columns = img.height, img.width
    pix = img.load()
    mask = Mask(rows, columns)
    for i in range(rows):
        for j in range(columns):
            if pix[j, i] == (0, 0, 0) and mask.is_bit(i, j):
                mask.set_bit(i, j, value=False)
    return mask


def from_png_scaled(file:str) -> Mask:
    """
    Creates a 1/10 scaled version of the png file.
    Quicker/neater than from_png.
    :param file:
    :return: Mask object
    """
    img = Image.open(file)
    rows, columns = img.height, img.width
    pix = img.load()
    smallrows = int((rows-1)/10)
    smallcols = int((columns-1)/10)
    mask = Mask(smallrows, smallcols)
    for i in range(smallrows-1):
        for j in range(smallcols-1):
            ith, jth = int(i*10), int(j*10)
            if pix[jth, ith] == (0, 0, 0) and mask.is_bit(i, j) and ith < rows and jth < columns:
                mask.set_bit(i, j, value=False)
    return mask

