
from Foundations.Cell import Cell
from random import randint, shuffle, choice
from PIL import Image, ImageDraw


class Grid(object):

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = self.prepare_grid()
        self.configure_cells()
        self.size = self.get_size()

    def __getitem__(self, index):
        print(index)
        print(self.rows, self.columns)
        return self.grid[index]

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.deadends() == other.deadends()
        return False

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return self.deadends() != other.deadends()
        return True
    
    def prepare_grid(self):
        grid = [[Cell(x, y) for y in range(self.columns)] for x in range(self.rows)]
        return grid

    def configure_cells(self):
        for line in self.grid:
            for cell in line:
                row, col = cell.row, cell.column
                cell.north = self.borders(row - 1, col)
                cell.south = self.borders(row + 1, col)
                cell.east = self.borders(row, col + 1)
                cell.west = self.borders(row, col - 1)

    def borders(self, row, column):
        """
        Checks to see if the cell is on the edge of the maze
        :param row:
        :param column:
        :return:
        """
        if row < 0 or row > self.rows - 1:
            return None
        if column < 0 or column > self.columns - 1:
            return None
        else:
            return self.grid[row][column]

    def random_cell(self):
        return self.grid[randint(0, self.rows-1)][randint(0, self.columns-1)]

    def get_size(self):
        return self.rows * self.columns

    def each_row(self):
        for row in self.grid:
            yield row

    def each_cell(self):
        for row in self.grid:
            for cell in row:
                yield cell
    
    def contents_of(self, cell):
        return " "
        
    def bg_color(self, cell):
        return None

    def __str__(self):
        output = "+" + "---+" * self.columns + "\n"
        for row in self.each_row():
            line = "|"
            bottom = "+"
            for cell in row:
                body = " " + self.contents_of(cell) + " "
                east_bound = "|"
                south_bound = "---"
                corner = '+'
                if cell and cell.is_linked(cell.east):
                    east_bound = " "
                line = line + body + east_bound
                if cell and cell.is_linked(cell.south):
                    south_bound = "   "
                bottom = bottom + south_bound + corner
            output = output + line + "\n" + bottom + "\n"
        return output
        
    def __repr__(self):
        return self.rows, self.columns

    def deadends(self):
        """
        :return: Count of dead ends in the maze
        """
        deads = []
        for cell in self.each_cell():
            if len(cell.links) == 1:
                deads.append(cell)
        return deads
    
    def to_png(self, size=50):
        """
        Creates a png file of maze
        :param size: 50 is default
        :return: image object
        """
        width = size * self.columns
        height = size * self.rows
        dimensions = (height, width)
        bg = (255, 255, 255)
        wall = (0, 0, 0)
        img = Image.new('RGBA', dimensions, bg)
        drw = ImageDraw.Draw(img)
        for cell in self.each_cell():
            x1 = int(cell.column * size)
            x2 = int((cell.column+1) * size)
            y1 = int(cell.row * size)
            y2 = int((cell.row+1) * size)
            color = self.bg_color(cell)
            if color:
                #print(x1, y2, x2, y2)
                drw.rectangle(((x1, y1), (x2, y2)), color)
            if not cell.north:
                drw.line(((x1, y1), (x2, y1)), wall, 5)
            if not cell.west:
                drw.line(((x1, y1), (x1, y2)), wall, 5)
            if not cell.is_linked(cell.east):
                drw.line(((x2, y1), (x2, y2)), wall, 5)
            if not cell.is_linked(cell.south):
                drw.line(((x1, y2), (x2, y2)), wall, 5)
        return img

    def braid(self, p=1.0):
        ends = self.deadends()
        shuffle(ends)
        for cell in ends:
            if len(cell.links) == 1:
                neighbors = []
                for neighbor in cell.neighbors():
                    if not cell.is_linked(neighbor):
                        neighbors.append(neighbor)
                stranger = choice(neighbors)
                cell.link(stranger)
