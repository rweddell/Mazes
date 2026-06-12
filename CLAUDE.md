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

The library lives under `src/mazes/` (src layout). Install it editable so `mazes` is importable
everywhere (the repo uses `uv`; `uv run` auto-installs from `pyproject.toml`):
```bash
uv run python main.py      # editable-installs mazes, then launches the GUI
# or, with plain pip:  pip install -e .  &&  python main.py
```

**Launch the GUI** (tkinter app — the main entry point): `python main.py`
(`ui/app.py` also adds `src/` to `sys.path`, so the GUI runs without an install.)

**Run a demo:** `uv run python demos/binary_tree_demo.py` (ASCII) or `demos/color_demo.py` (PNG→`output/`).

**Dependencies:** Pillow (declared in `pyproject.toml`; `setup.py` is a thin shim). `tkinter`/`urllib` stdlib.

There is no test suite and no linter configured. Demos serve as the primary way to validate behavior.

## Architecture

The project uses a **Strategy + Inheritance** pattern split across two subpackages of `src/mazes/`
(`structures/`, `algorithms/`), with shared helpers in `mazes/utils/` (e.g. `base36`):

### `mazes/algorithms/` — Generation Algorithms

All algorithms inherit from `MazeAlgorithm` (abstract base in `maze_algorithm.py`) and implement a single method:

```python
def on(self, grid):  # carves passages by calling cell.link()
```

Algorithms: `BinaryTree`, `Sidewinder`, `AldousBroder`, `Wilson`, `HuntAndKill`, `RecursiveBacktracker`.

### `mazes/structures/` — Grid and Cell Types

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
- `ColoredPolar` — multiple-inherits `PolarGrid` + `ColoredGrid` for colorized circular mazes
- `WeightedGrid` — pairs with `WeightedCell` for Dijkstra/weighted pathfinding

**Distance tracking (`distances.py`, `distance_grid.py`):** `Distances` runs BFS (priority queue for
weighted) from a root cell, storing distances for path-finding (`path_to()`) and coloring (`ColoredGrid`).

### `ui/` — Tkinter GUI (`ui/app.py`)

`MazeApp(tk.Tk)` is a two-panel window (controls left, preview right) mapping choices via `ALGORITHMS`
/`GRID_TYPES` dicts. `_build_grid()` picks the grid (`PolarGrid`, else `MaskedGrid` from an image, else
`ColoredGrid`); `_generate()` runs `.on(grid)`, calls `grid.to_png(size=...)`, and renders — errors surface
in a `messagebox` + status label.

Typical usage (see demos): build a grid, run `Algorithm().on(grid)`, optionally set
`grid.distances` via `Distances(root).path_to(target)`, then `grid.to_png("output/maze.png")`.

### Key design details

- `cell.link(other)` carves a bidirectional passage. `cell.is_linked(other)` checks it.
- `cell.neighbors()` returns only valid (non-None) adjacent cells — safe to call on edge/polar cells.
- `Grid.__getitem__` accepts `grid[row, col]` and returns `None` for out-of-bounds (used by algorithms to avoid boundary checks).
- PNG cell size is controlled by `size` parameter in `to_png()` (default varies by grid type).
- `PolarGrid` dynamically computes row widths based on circumference; algorithms must handle variable neighbor counts.
- `wilson.py` defines the class as `Wilsons` (not `Wilson`) — import accordingly.

## Session summary (2026-06-05)

**src-layout refactor:** packages moved under `src/mazes/` (`maze_structures`→`mazes.structures`,
`maze_algorithms`→`mazes.algorithms`, `base36.py`→`mazes/utils/base36.py`); all imports rewritten across
packages, 15 demos, and `ui/app.py` (`sys.path` shim now points at `src/`). `pyproject.toml` is the single
build config (setuptools, `packages.find where=["src"]`); `setup.py` is a shim. Verified via `uv run`: build,
import smoke test, demo render, `ui.app` import. Root monoliths `big_grid.py`/`new_maze_algorithm.py` kept
(dead duplicates, per user). Prior sessions: many bug fixes + `image_mask.py` and the `ui/app.py` GUI.
