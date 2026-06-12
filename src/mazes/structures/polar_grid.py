
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

    @staticmethod
    def _sector_points(center, inner_radius, outer_radius, t0, t1):
        """Points outlining an annular sector, following both arcs.

        Filling with a straight 4-corner polygon leaves a white crescent
        between the chord and the true arc (most visible at the outer edge);
        tessellating the arcs makes the fill hug the circle so adjacent cells
        meet with no gap.
        """
        segs = max(2, int((t1 - t0) / (pi / 36)))  # ~5 degrees per segment
        pts = []
        for i in range(segs + 1):                  # inner arc, ccw -> cw
            t = t0 + (t1 - t0) * i / segs
            pts.append((center + inner_radius * cos(t),
                        center + inner_radius * sin(t)))
        for i in range(segs + 1):                  # outer arc, cw -> ccw
            t = t1 - (t1 - t0) * i / segs
            pts.append((center + outer_radius * cos(t),
                        center + outer_radius * sin(t)))
        return pts

    def to_png(self, size=40):
        """
        Creates an Image object of the grid that can be saved to a png
        :param size: cell height in pixels
        :return: Image object
        """
        # Render everything at ss x resolution, then shrink with LANCZOS so the
        # arcs and radial lines come out anti-aliased instead of jagged.
        ss = 3
        csize = size * ss                 # supersampled cell height
        margin = csize                    # keep the outer ring clear of the border
        rmax = self.rows * csize          # radius of the outermost ring
        imgsize = 2 * rmax + 2 * margin
        center = imgsize / 2
        wall_w = max(2, round(size * 0.1)) * ss
        bg = (255, 255, 255)
        wall = (0, 0, 0)
        img = Image.new('RGBA', (imgsize, imgsize), bg)
        drw = ImageDraw.Draw(img)
        for base_cell in self.each_cell():
            cell = cast(PolarCell, base_cell)
            theta = (2 * pi)/self.grid[cell.row].__len__()
            inner_radius = cell.row * csize
            outer_radius = (cell.row + 1) * csize
            theta_ccw = cell.column * theta
            theta_cw = (cell.column+1) * theta

            cx = center + inner_radius * cos(theta_cw)
            cy = center + inner_radius * sin(theta_cw)
            dx = center + outer_radius * cos(theta_cw)
            dy = center + outer_radius * sin(theta_cw)

            color = self.bg_color(cell)
            if color:
                if cell.row == 0:
                    drw.ellipse([(center-csize, center-csize), (center+csize, center+csize)], fill=color)
                else:
                    drw.polygon(self._sector_points(center, inner_radius,
                                                    outer_radius, theta_ccw,
                                                    theta_cw), fill=color)
            if cell.row > 0 and not cell.is_linked(cell.inward):
                # inner wall: arc at inner_radius spanning the cell's angular range
                r = inner_radius
                drw.arc([(center-r, center-r), (center+r, center+r)],
                        start=degrees(theta_ccw), end=degrees(theta_cw),
                        fill=wall, width=wall_w)
            if cell.row > 0 and not cell.is_linked(cell.cw):
                # clockwise wall: radial line from inner to outer corner
                drw.line([(cx, cy), (dx, dy)], fill=wall, width=wall_w)
        # outer boundary circle on top of the fills so it isn't painted over
        # (a bit thicker than the interior walls)
        drw.ellipse([(center - rmax, center - rmax), (center + rmax, center + rmax)],
                    outline=wall, width=round(wall_w * 1.5))
        final = round(imgsize / ss)
        return img.resize((final, final), Image.Resampling.LANCZOS)
