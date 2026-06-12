
from mazes.structures.grid import Grid
from mazes.structures.polar_cell import PolarCell
from PIL import Image, ImageDraw
from math import cos, sin, pi, degrees
from random import randint
from typing import cast


class PolarGrid(Grid):

    def __init__(self, rows):
        super().__init__(rows, 1)

    def retrieve(self, row, column) -> PolarCell | None:
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
        for base_cell in self.each_cell():
            cell = cast(PolarCell, base_cell)
            row, col = cell.row, cell.column
            if row > 0:
                cell.cw = self.retrieve(row, col+1)
                cell.ccw = self.retrieve(row, col-1)
                ratio = self.grid[row].__len__()/self.grid[row-1].__len__()
                parent = cast(PolarCell, self.grid[row-1][int(col/ratio) if row-1 != 0 else 0])
                parent.outward.append(cell)
                cell.inward = parent
            elif row == 0:
                for neighbor in self.grid[row+1]:
                    cell.outward.append(neighbor)

    def get_size(self):
        # rows grow outward, so the real count is the sum of each ring's length
        return sum(len(ring) for ring in self.grid)

    def random_cell(self):
        row = randint(0, self.rows-1)
        col = randint(0, self.grid[row].__len__()-1)
        return self.grid[row][col]

    def to_png(self, size=40):
        """
        Creates an Image object of the grid that can be saved to a png
        :param size: cell height in pixels
        :return: Image object
        """
        imgsize = 2 * self.rows * size
        bg = (255, 255, 255)
        wall = (0, 0, 0)
        img = Image.new('RGBA', (imgsize+1, imgsize+1), bg)
        drw = ImageDraw.Draw(img)
        center = imgsize/2
        drw.ellipse([(0, 0), (imgsize+1, imgsize+1)], fill=wall, outline=wall)
        drw.ellipse([(2, 2), (imgsize-1, imgsize-1)], fill=bg, outline=wall)
        for base_cell in self.each_cell():
            cell = cast(PolarCell, base_cell)
            theta = (2 * pi)/self.grid[cell.row].__len__()
            inner_radius = cell.row * size
            outer_radius = (cell.row + 1) * size
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

            color = self.bg_color(cell)
            if color:
                if cell.row == 0:
                    drw.ellipse([(center-size, center-size), (center+size, center+size)], fill=color)
                else:
                    drw.polygon([(ax, ay), (bx, by), (dx, dy), (cx, cy)], fill=color)
            if cell.row > 0 and not cell.is_linked(cell.inward):
                # inner wall: arc at inner_radius spanning the cell's angular range
                r = inner_radius
                drw.arc([(center-r, center-r), (center+r, center+r)],
                        start=degrees(theta_ccw), end=degrees(theta_cw),
                        fill=wall, width=4)
            if cell.row > 0 and not cell.is_linked(cell.cw):
                # clockwise wall: radial line from inner to outer corner
                drw.line([(cx, cy), (dx, dy)], fill=wall, width=4)
        return img
