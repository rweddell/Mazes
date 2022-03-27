
from Foundations.Grid import Grid
from Foundations.Polarcell import PolarCell
from PIL import Image, ImageDraw
from math import *
from random import randint


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
