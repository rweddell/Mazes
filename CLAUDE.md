# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## DEVELOPMENT NOTES FOR CLAUDE:

- when the user enters a prompt, always make a plan first, and then implement the plan in the most efficient way.
- the application should be designed with a clean and intuitive user interface, making it easy for users to navigate and customize their experience
- code should be well-structured and modular, allowing for easy maintenance and future enhancements (frontend and backend should be separated by directory)
- the application should handle errors gracefully, providing informative messages to the user in case of issues with
- update the README.md with new or changes features when appropriate
- update CLAUDE.md with a short summary of changes after every session and keep the file less than 100 lines long, compressing the previous summary if necessary
- ensure that the application is compatible with multiple operating systems, including Windows, macOS, and Linux
- IMPORTANT: keep token usage in mind and avoid unnecessary verbosity in code and comments, while still maintaining clarity and readability.
- TODO.txt file holds user feedback that should be addressed if the file exists and contains information.

## Project Overview

Python implementation of maze generation algorithms and visualizations from the book *Mazes for Programmers* by Jamis Buck. Outputs mazes as ASCII text or PNG images.

## Commands

**Install:**
```bash
python setup.py install
```

**Run a demo:**
```bash
python demos/binary_tree_demo.py   # ASCII output
python demos/color_demo.py         # PNG output to output/
```

**Dependencies** (not in setup.py — install manually):
```bash
pip install Pillow
```

There is no test suite and no linter configured. Demos serve as the primary way to validate behavior.

## Architecture

The project uses a **Strategy + Inheritance** pattern split across two packages:

### `maze_algorithms/` — Generation Algorithms

All algorithms inherit from `MazeAlgorithm` (abstract base in `maze_algorithm.py`) and implement a single method:

```python
def on(self, grid):  # carves passages by calling cell.link()
```

Algorithms: `BinaryTree`, `Sidewinder`, `AldousBroder`, `Wilson`, `HuntAndKill`, `RecursiveBacktracker`.

### `maze_structures/` — Grid and Cell Types

**Cell hierarchy:**
- `Cell` — base; holds N/S/E/W neighbor references and a `linked` set for carved passages
- `WeightedCell` — adds weight for Dijkstra pathfinding
- `PolarCell` — adds CW/CCW/inward/outward neighbors for circular mazes

**Grid hierarchy:**
- `Grid` — base; 2D array of `Cell`, implements `str()` (ASCII) and `to_png()` (PIL image)
- `DistanceGrid` — overrides ASCII rendering to show numeric distances
- `ColoredGrid` — overrides PNG rendering to colorize cells by distance intensity
- `MaskedGrid` — uses a `Mask` object to disable cells (supports image or text masks)
- `PolarGrid` — circular coordinate grid; row widths grow outward

**Distance tracking (`distances.py`, `distance_grid.py`):**  
`Distances` runs BFS (or priority queue for weighted) from a root cell and stores distances. Used for path-finding (`path_to()`) and coloring (`ColoredGrid`).

### Typical usage pattern (from demos):

```python
grid = ColoredGrid(10, 10)
RecursiveBacktracker().on(grid)
grid.distances = Distances(grid[0, 0]).path_to(grid[grid.rows-1, grid.columns-1])
grid.to_png("output/maze.png")
```

### Key design details

- `cell.link(other)` carves a bidirectional passage. `cell.is_linked(other)` checks it.
- `cell.neighbors()` returns only valid (non-None) adjacent cells — safe to call on edge/polar cells.
- `Grid.__getitem__` accepts `grid[row, col]` and returns `None` for out-of-bounds (used by algorithms to avoid boundary checks).
- PNG cell size is controlled by `size` parameter in `to_png()` (default varies by grid type).
- `PolarGrid` dynamically computes row widths based on circumference; algorithms must handle variable neighbor counts.
- `wilson.py` defines the class as `Wilsons` (not `Wilson`) — import accordingly.

## Session summary (2026-04-19)

**Bug fixes:** removed debug prints from `Grid.__getitem__`; fixed swapped PIL dimensions in `Grid.to_png`; fixed `Mask.__init__` off-by-one (was subtracting 1 from rows/cols); fixed `Mask.random_location` IndexError; fixed `from_txt` double file open; fixed duplicate `cell.cw` assignment in `PolarGrid.configure_cells`; fixed `PolarGrid.to_png` parameter renamed from `cellsize` to `size`; fixed `wilson.py` broken import; added `cast(PolarCell, ...)` to resolve Pyright errors in `polar_grid.py`.

**New features:** `maze_structures/image_mask.py` — edge-detection and shape-mask generation from PIL images or URLs; `ui/app.py` — tkinter GUI (algorithm picker, grid type, size inputs, image upload/URL, preview canvas, save dialog); `main.py` now launches the UI.
