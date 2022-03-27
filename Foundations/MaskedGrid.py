from PIL import Image, ImageDraw
from Foundations.Grid import Grid
from Foundations.Cell import Cell


class MaskedGrid(Grid):

    def __init__(self, newmask):
        self.mask = newmask
        super().__init__(self.mask.rows, self.mask.columns)

    def prepare_grid(self):
        grid = [[None for y in range(self.columns)] for x in range(self.rows)]
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if self.mask.is_bit(i, j):
                    grid[i][j] = Cell(i, j)
        return grid

    def random_cell(self):
        row, col = self.mask.random_location()
        return self.grid[row][col]

    def configure_cells(self):
        for line in self.grid:
            for cell in line:
                if cell is not None:
                    row, col = cell.row, cell.column
                    if self.mask.is_bit(row, col):
                        if self.mask.is_bit(row-1, col):
                            cell.north = self.borders(row - 1, col)
                        if self.mask.is_bit(row+1, col):
                            cell.south = self.borders(row + 1, col)
                        if self.mask.is_bit(row, col+1):
                            cell.east = self.borders(row, col + 1)
                        if self.mask.is_bit(row, col-1):
                            cell.west = self.borders(row, col - 1)

    def to_png(self, size=50):
        """
        Creates a png file of maze
        :param size: 50 is default
        :return: Image object
        """
        width = size * self.columns
        height = size * self.rows
        dimensions = (width, height)
        bg = (255, 255, 255)
        wall = (0, 0, 0)
        img = Image.new('RGBA', dimensions, bg)
        drw = ImageDraw.Draw(img)
        for cell in self.each_cell():
            if cell is not None:
                x1 = cell.column * size
                x2 = (cell.column+1) * size
                y1 = cell.row * size
                y2 = (cell.row+1) * size
                color = self.bg_color(cell)
                if color:
                    if self.mask.is_bit(cell.row, cell.column):
                        drw.rectangle(((x1, y1), (x2, y2)), color)
                    else:
                        drw.rectangle(((x1, y1), (x2, y2)), bg)
                if not cell.north:
                    drw.line(((x1, y1), (x2, y1)), wall, 5)
                if not cell.west:
                    drw.line(((x1, y1), (x1, y2)), wall, 5)
                if not cell.is_linked(cell.east):
                    drw.line(((x2, y1), (x2, y2)), wall, 5)
                if not cell.is_linked(cell.south):
                    drw.line(((x1, y2), (x2, y2)), wall, 5)
        return img

