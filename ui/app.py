import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from maze_structures.grid import Grid
from maze_structures.color_grid import ColoredGrid
from maze_structures.masked_grid import MaskedGrid
from maze_structures.polar_grid import PolarGrid
from maze_structures.mask import from_png as mask_from_png
from maze_structures.image_mask import (
    from_image_edges, from_image_shape,
    load_image_from_path, load_image_from_url
)
from maze_algorithms.binary_tree import BinaryTree
from maze_algorithms.sidewinder import Sidewinder
from maze_algorithms.aldous_broder import AldousBroder
from maze_algorithms.wilson import Wilsons as Wilson
from maze_algorithms.hunt_and_kill import HuntAndKill
from maze_algorithms.recursive_backtrack import RecursiveBacktracker

ALGORITHMS = {
    "Recursive Backtracker": RecursiveBacktracker,
    "Binary Tree": BinaryTree,
    "Sidewinder": Sidewinder,
    "Aldous-Broder": AldousBroder,
    "Wilson": Wilson,
    "Hunt & Kill": HuntAndKill,
}

IMAGE_MODES = ["Edge Detection", "Shape Mask"]
GRID_TYPES = ["Standard", "Polar (Circular)"]


class MazeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Generator")
        self.resizable(True, True)
        self._current_image: Image.Image | None = None
        self._source_image: Image.Image | None = None
        self._photo: ImageTk.PhotoImage | None = None
        self._build_ui()

    def _build_ui(self):
        # ── left panel (controls) ──────────────────────────────────────────
        ctrl = ttk.Frame(self, padding=10)
        ctrl.grid(row=0, column=0, sticky="ns")

        ttk.Label(ctrl, text="Algorithm").grid(row=0, column=0, sticky="w")
        self._algo_var = tk.StringVar(value="Recursive Backtracker")
        ttk.Combobox(ctrl, textvariable=self._algo_var,
                     values=list(ALGORITHMS), state="readonly", width=22
                     ).grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(ctrl, text="Grid type").grid(row=2, column=0, sticky="w")
        self._grid_var = tk.StringVar(value="Standard")
        self._grid_cb = ttk.Combobox(ctrl, textvariable=self._grid_var,
                                     values=GRID_TYPES, state="readonly", width=22)
        self._grid_cb.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        self._grid_var.trace_add("write", self._on_grid_type_change)

        # size
        size_frame = ttk.LabelFrame(ctrl, text="Size", padding=6)
        size_frame.grid(row=4, column=0, sticky="ew", pady=(0, 8))
        ttk.Label(size_frame, text="Rows").grid(row=0, column=0, sticky="w")
        self._rows_var = tk.IntVar(value=20)
        ttk.Spinbox(size_frame, from_=5, to=200, textvariable=self._rows_var,
                    width=6).grid(row=0, column=1, padx=4)
        self._cols_label = ttk.Label(size_frame, text="Cols")
        self._cols_label.grid(row=1, column=0, sticky="w")
        self._cols_var = tk.IntVar(value=20)
        self._cols_spin = ttk.Spinbox(size_frame, from_=5, to=200,
                                      textvariable=self._cols_var, width=6)
        self._cols_spin.grid(row=1, column=1, padx=4)

        # image source
        img_frame = ttk.LabelFrame(ctrl, text="Image source (optional)", padding=6)
        img_frame.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(img_frame, text="Mode").grid(row=0, column=0, sticky="w")
        self._img_mode_var = tk.StringVar(value="Edge Detection")
        ttk.Combobox(img_frame, textvariable=self._img_mode_var,
                     values=IMAGE_MODES, state="readonly", width=16
                     ).grid(row=0, column=1, sticky="ew")

        self._url_var = tk.StringVar()
        ttk.Label(img_frame, text="URL").grid(row=1, column=0, sticky="w", pady=(4, 0))
        ttk.Entry(img_frame, textvariable=self._url_var, width=20
                  ).grid(row=1, column=1, sticky="ew", pady=(4, 0))

        ttk.Button(img_frame, text="Browse file…",
                   command=self._browse_image).grid(row=2, column=0, columnspan=2,
                                                     sticky="ew", pady=(6, 0))
        self._img_path_var = tk.StringVar(value="")
        ttk.Label(img_frame, textvariable=self._img_path_var,
                  wraplength=180, foreground="gray"
                  ).grid(row=3, column=0, columnspan=2, sticky="w")

        ttk.Button(img_frame, text="Clear image",
                   command=self._clear_image).grid(row=4, column=0, columnspan=2,
                                                    sticky="ew", pady=(4, 0))

        # action buttons
        ttk.Button(ctrl, text="Generate", command=self._generate
                   ).grid(row=6, column=0, sticky="ew", pady=(4, 2))
        ttk.Button(ctrl, text="Save image…", command=self._save
                   ).grid(row=7, column=0, sticky="ew", pady=(0, 4))

        self._status_var = tk.StringVar(value="Ready.")
        ttk.Label(ctrl, textvariable=self._status_var, wraplength=200,
                  foreground="steelblue").grid(row=8, column=0, sticky="w")

        # ── right panel (preview) ─────────────────────────────────────────
        preview = ttk.Frame(self, padding=10)
        preview.grid(row=0, column=1, sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._canvas = tk.Canvas(preview, bg="#f0f0f0", width=600, height=600)
        self._canvas.pack(fill="both", expand=True)

    # ── event handlers ────────────────────────────────────────────────────

    def _on_grid_type_change(self, *_):
        polar = self._grid_var.get() == "Polar (Circular)"
        state = "disabled" if polar else "normal"
        self._cols_label.configure(foreground="gray" if polar else "black")
        self._cols_spin.configure(state=state)

    def _browse_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                       ("All files", "*.*")])
        if path:
            self._img_path_var.set(os.path.basename(path))
            self._source_image = load_image_from_path(path)
            self._url_var.set("")
            self._status_var.set(f"Loaded: {os.path.basename(path)}")

    def _clear_image(self):
        self._source_image = None
        self._img_path_var.set("")
        self._url_var.set("")
        self._status_var.set("Image cleared.")

    def _generate(self):
        try:
            self._status_var.set("Generating…")
            self.update_idletasks()
            grid = self._build_grid()
            algo = ALGORITHMS[self._algo_var.get()]()
            algo.on(grid)
            cell_px = max(4, min(20, 600 // max(getattr(grid, 'rows', 20),
                                                  getattr(grid, 'columns', 20))))
            img = grid.to_png(size=cell_px)
            self._current_image = img
            self._show_image(img)
            self._status_var.set("Done.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            self._status_var.set("Error — see dialog.")

    def _build_grid(self) -> Grid:
        rows = self._rows_var.get()
        cols = self._cols_var.get()
        grid_type = self._grid_var.get()
        img_mode = self._img_mode_var.get()

        # polar ignores image source and columns
        if grid_type == "Polar (Circular)":
            return PolarGrid(rows)

        # load image if provided
        img = self._load_source_image()

        if img is not None:
            if img_mode == "Edge Detection":
                mask = from_image_edges(img, max_dim=max(rows, cols))
            else:
                mask = from_image_shape(img, max_dim=max(rows, cols))
            return MaskedGrid(mask)

        return ColoredGrid(rows, cols)

    def _load_source_image(self):
        url = self._url_var.get().strip()
        if url:
            self._status_var.set("Fetching URL…")
            self.update_idletasks()
            return load_image_from_url(url)
        if self._source_image is not None:
            return self._source_image
        return None

    def _show_image(self, img: Image.Image):
        canvas_w = self._canvas.winfo_width() or 600
        canvas_h = self._canvas.winfo_height() or 600
        img_fit = img.copy()
        img_fit.thumbnail((canvas_w, canvas_h), Image.LANCZOS)
        self._photo = ImageTk.PhotoImage(img_fit)
        self._canvas.delete("all")
        self._canvas.create_image(canvas_w // 2, canvas_h // 2,
                                   anchor="center", image=self._photo)

    def _save(self):
        if self._current_image is None:
            messagebox.showinfo("Nothing to save", "Generate a maze first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")])
        if path:
            self._current_image.save(path)
            self._status_var.set(f"Saved: {os.path.basename(path)}")


def run():
    app = MazeApp()
    app.mainloop()


if __name__ == "__main__":
    run()
