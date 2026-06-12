from mazes.structures.polar_grid import PolarGrid
from mazes.structures.color_grid import ColoredGrid


class ColoredPolar(PolarGrid, ColoredGrid):
    """Circular grid that colors cells by distance.

    PolarGrid.to_png handles the circular rendering; set_distances, bg_color
    and base_color come from ColoredGrid via the MRO.
    """

    def __init__(self, rows):
        # PolarGrid.__init__ -> super() resolves to ColoredGrid (sets distlist,
        # base_color) -> Grid, so the colored fields are initialized too.
        PolarGrid.__init__(self, rows)
