from mazes.structures.grid import Grid

class ColoredGrid(Grid):

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.farthest = None
        self.max_dist = None
        self.distlist = None
        # gradient endpoint for the farthest cell; near cells fade toward white
        self.base_color = (0, 128, 0)

    def set_distances(self, distances):
        self.distlist = distances
        self.farthest, self.max_dist = distances.max_path()

    def set_base_color(self, rgb):
        self.base_color = rgb

    def bg_color(self, cell) -> tuple[int, int, int] | None:
        if self.distlist is None:
            return None
        distance = self.distlist[cell]
        intensity = (self.max_dist - distance) / self.max_dist
        r, g, b = self.base_color
        # intensity 1 (at the root) → white; intensity 0 (farthest) → base_color
        return (round(r + (255 - r) * intensity),
                round(g + (255 - g) * intensity),
                round(b + (255 - b) * intensity))
