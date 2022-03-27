
from PIL import Image
from random import randint


class Mask:

    def __init__(self, rows, columns):
        self.rows = rows-1
        self.columns = columns-1
        self.bits = [[True for i in range(self.columns)] for j in range(self.rows)]

    def is_bit(self, row, column):
        if row in range(0, self.rows) and column in range(0, self.columns):
            return self.bits[row][column]
        else:
            return False

    def set_bit(self, row, column, value=True):
        self.bits[row][column] = value

    def count(self):
        total = 0
        for row in self.rows:
            for col in row:
                if self.is_bit(row, col):
                    total += 1
        return total

    def __repr__(self):
        return self.rows, self.columns

    def random_location(self):
        row = randint(0, self.rows)
        col = randint(0, self.columns)
        while not self.is_bit(row, col):
            row = randint(0, self.rows)
            col = randint(0, self.columns)
        return row, col

    def __str__(self):
        stringy = ''
        for row in self.bits:
            for bit in row:
                if bit is True:
                    stringy += 'x'
                else:
                    stringy += ' '
            stringy += '\n'
        return stringy


def from_txt(file):
    """
    :param file(location of file):
    :return: Mask object
    """
    with open(file) as f:
        lines = f.readlines()
    f.close()
    text = open(file, 'r')
    rows = sum(1 for line in text)
    columns = len(lines[1])
    mask = Mask(rows, columns)
    for i in range(rows-1):
        for j in range(columns-1):
            if lines[i][j] is 'x':
                mask.set_bit(i, j, False)
    return mask


def from_png(file):
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


def from_png_scaled(file):
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
