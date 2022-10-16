from maze_structures.cell import Cell
from random import randint, shuffle, choice
from PIL import Image, ImageDraw


class Grid:

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


class DistanceGrid(Grid):

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.farthest = None
        self.maximum = None
        self.distlist = {}

    def distances(self, distances):
        self.distlist = distances
        self.farthest, self.maximum = distances.max_path()

    def contents_of(self, cell):
        if self.distlist and cell in self.distlist.keys():
            return Base36.encode(self.distlist[cell])
        else:
            return super().contents_of(cell)


class WeightedGrid(DistanceGrid):

    def __init__(self, rows, columns):
        super(DistanceGrid, self).__init__(rows, columns)

    def __str__(self):
        return 'WeightedGrid: (' + str(self.rows) + ', ' + str(self.columns) + ')'

    def __repr__(self):
        return self.__str__()

    def set_distances(self, distances):
        self.distlist = distances
        self.farthest, self.maximum = distances.max_path()

    def prepare_grid(self):
        grid = [[WeightedCell(x, y) for y in range(self.columns)] for x in range(self.rows)]
        return grid

    def bg_color(self, cell):
        if cell.weight > 1:
            return (255, 0, 0)
        elif self.distances:
            distance = self.distlist[cell] if self.distlist[cell] else None
            if distance is None:
                return None
            else:
                intensity = int(64 + 191 * (self.maximum - distance)/self.maximum)
                return (intensity, intensity, 0)

    def random_dist(self):
        cells = list(self.distlist.keys())
        return choice(cells)


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


class PolarGrid(Grid):

    def __init__(self, rows):
        super().__init__(rows, 1)

    def retrieve(self, row, column):
        """
        Connects the ends of rows in a PolarGrid to the beginnings
        :param row:
        :param column:
        :return: beginning/end of row or None
        """
        if -2 < column < self.grid[row].__len__()+1:
            return self.grid[row][column % self.grid[row].__len__()]
        return None

    def prepare_grid(self):
        rowlist = []
        row_ht = 1.0/self.rows
        rowlist.append([PolarCell(0, 0)])
        for row in range(1, self.rows):
            radius = float(row/self.rows)
            circumference = 2*pi*radius
            prev_count = rowlist[row-1].__len__()
            est_cell_w = circumference/prev_count
            ratio = round(est_cell_w/row_ht)
            cells = prev_count*ratio
            rowlist.append([PolarCell(row, col) for col in range(cells)])
        return rowlist

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column
            if row > 0:
                cell.cw = self.retrieve(row, col+1)
                cell.ccw = self.retrieve(row, col-1)
                ratio = self.grid[row].__len__()/self.grid[row-1].__len__()
                if row-1 != 0:
                    parent = self.grid[row-1][int(col/ratio)]
                else:
                    parent = self.grid[row-1][0]
                parent.outward.append(cell)
                cell.inward = parent
            elif row == 0:
                cell.cw = self.retrieve(row, col+1)
                cell.cw = self.retrieve(row+1, col+1)
                for neighbor in self.grid[row+1]:
                    cell.outward.append(neighbor)

    def random_cell(self):
        row = randint(0, self.rows-1)
        col = randint(0, self.grid[row].__len__()-1)
        return self.grid[row][col]

    def to_png(self, cellsize=40):
        """
        Creates an Image object of the grid that can be saved to a png
        :param cellsize: height of cell
        :return: Image object
        """
        imgsize = 2 * self.rows * cellsize
        bg = (255, 255, 255)
        wall = (0, 0, 0)
        img = Image.new('RGBA', (imgsize+1, imgsize+1), bg)
        drw = ImageDraw.Draw(img)
        center = imgsize/2
        # TODO: tweak the ellipse to make thicker lines. White fill/black png background?
        drw.ellipse([(0, 0), (imgsize+1, imgsize+1)], fill=wall, outline=wall)
        drw.ellipse([(2, 2), (imgsize-1, imgsize-1)], fill=bg, outline=wall)
        for cell in self.each_cell():
            theta = (2 * pi)/self.grid[cell.row].__len__()
            inner_radius = cell.row * cellsize
            outer_radius = (cell.row + 1) * cellsize
            theta_ccw = cell.column * theta
            theta_cw = (cell.column+1) * theta

            ax = center + round(inner_radius * cos(theta_ccw))
            ay = center + round(inner_radius * sin(theta_ccw))
            bx = center + round(outer_radius * cos(theta_ccw))
            by = center + round(outer_radius * sin(theta_ccw))
            cx = center + round(inner_radius * cos(theta_cw))
            cy = center + round(inner_radius * sin(theta_cw))
            dx = center + round(outer_radius * cos(theta_cw))
            dy = center + round(outer_radius * sin(theta_cw))
            # Trying to get the "peak" at point between cw and ccw
            # midx = center + round((outer_radius * cos(theta_ccw)+((bx - dx)/2))*1.2)
            # midy = center + round((outer_radius * sin(theta_ccw)+((by - dy)/2))*1.2)
            color = self.bg_color(cell)
            if color:
                if cell.row == 0:
                    drw.ellipse([(center-cellsize, center-cellsize), (center+cellsize, center+cellsize)], fill=color)
                else:
                    drw.polygon([(ax, ay), (bx, by), (dx, dy), (cx, cy)], fill=color)
                    # TODO: Get rid of that last bit of white around the center of the circle
                    #drw.chord([(cx, cy), (dx, dy)], 0, 90, fill=color)
            if not cell.is_linked(cell.inward):
                # TODO: Understand the trig to get ImageDraw.arc to work.
                # might not be possible with PIL.ImageDraw due to bounding boxes
                #drw.arc([(bx, by), (dx, dy)], ax, cx, fill=wall)
                drw.line([(ax, ay), (cx, cy)], fill=wall, width=4)
            if not cell.is_linked(cell.cw):
                drw.line([(cx, cy), (dx, dy)], fill=wall, width=4)
        return img


class ColoredGrid(Grid):

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.farthest = None
        self.max_dist = None
        self.distlist = None

    def set_distances(self, distances):
        self.distlist = distances
        self.farthest, self.max_dist = distances.max_path()

    def bg_color(self, cell):
        distance = self.distlist[cell]
        intensity = (self.max_dist - distance)/self.max_dist
        dark = round(255 * intensity)
        bright = 128 + round(127 * intensity)
        return (dark, bright, dark)


class ColoredPolar(PolarGrid, ColoredGrid):

    def __init__(self, rows):
        PolarGrid.__init__(self, rows)
        self.farthest = None
        self.max_dist = None
        self.distlist = None

    def set_distances(self, distances):
        self.distlist = distances
        self.farthest, self.max_dist = distances.max_path()

    def bg_color(self, cell):
        distance = self.distlist[cell]
        intensity = (self.max_dist - distance) / self.max_dist
        dark = round(255 * intensity)
        bright = 128 + round(127 * intensity)
        return (bright, dark, bright)


class ColoredMask(MaskedGrid, ColoredGrid):

    def __init__(self, newmask):
        self.mask = newmask
        super().__init__(newmask)
        self.farthest = None
        self.max_dist = None
        self.distlist = None
