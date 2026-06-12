import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mazes.structures.grid import Grid
from mazes.structures.color_grid import ColoredGrid
from mazes.structures.masked_grid import MaskedGrid
from mazes.structures.color_polar import ColoredPolar
from mazes.structures.mask import from_png as mask_from_png
from mazes.structures.image_mask import (
    from_image_edges, from_image_shape,
    load_image_from_path, load_image_from_url
)
from mazes.algorithms.binary_tree import BinaryTree
from mazes.algorithms.sidewinder import Sidewinder
from mazes.algorithms.aldous_broder import AldousBroder
from mazes.algorithms.wilson import Wilsons as Wilson
from mazes.algorithms.hunt_and_kill import HuntAndKill
from mazes.algorithms.recursive_backtrack import RecursiveBacktracker

ALGORITHMS = {
    "Recursive Backtracker": RecursiveBacktracker,
    "Binary Tree": BinaryTree,
    "Sidewinder": Sidewinder,
    "Aldous-Broder": AldousBroder,
    "Wilson": Wilson,
    "Hunt & Kill": HuntAndKill,
}

def _hex(rgb):
    return "#%02x%02x%02x" % rgb


# slate-gray UI theme
BG = "#37474f"        # main background (blue-gray 800)
PANEL = "#455a64"     # input fields / buttons (blue-gray 700)
TEXT = "#eceff1"      # primary text
MUTED = "#90a4ae"     # secondary / disabled text
ACTIVE = "#546e7a"    # hover / active
CANVAS_BG = "#2b353d"  # preview area


IMAGE_MODES = ["Edge Detection", "Shape Mask"]
GRID_TYPES = ["Standard", "Polar (Circular)"]

# distance-gradient base colors (the hue of the farthest cells)
COLORS = [
    ("Green",  (0, 128, 0)),
    ("Blue",   (30, 60, 200)),
    ("Red",    (200, 40, 40)),
    ("Purple", (140, 40, 160)),
    ("Orange", (220, 130, 20)),
    ("Teal",   (0, 150, 150)),
]


class MazeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Generator")
        self.resizable(True, True)
        self._current_image: Image.Image | None = None
        self._source_image: Image.Image | None = None
        self._photo: ImageTk.PhotoImage | None = None
        self._base_color = COLORS[0][1]
        self._swatches: list[tk.Button] = []
        self._apply_theme()
        self._build_ui()

    def _apply_theme(self):
        self.configure(bg=BG)
        style = ttk.Style(self)
        style.theme_use("clam")  # clam honors color options on Windows; vista doesn't
        style.configure(".", background=BG, foreground=TEXT,
                        fieldbackground=PANEL, bordercolor=ACTIVE,
                        lightcolor=PANEL, darkcolor=PANEL)
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("TLabelframe", background=BG, bordercolor=ACTIVE)
        style.configure("TLabelframe.Label", background=BG, foreground=MUTED)
        style.configure("TButton", background=PANEL, foreground=TEXT,
                        bordercolor=ACTIVE, focuscolor=BG)
        style.map("TButton",
                  background=[("active", ACTIVE), ("pressed", ACTIVE)])
        style.configure("TCheckbutton", background=BG, foreground=TEXT)
        style.map("TCheckbutton", background=[("active", BG)],
                  indicatorcolor=[("selected", ACTIVE)])
        style.configure("TCombobox", fieldbackground=PANEL, background=PANEL,
                        foreground=TEXT, arrowcolor=TEXT)
        style.map("TCombobox", fieldbackground=[("readonly", PANEL)],
                  foreground=[("readonly", TEXT)])
        style.configure("TSpinbox", fieldbackground=PANEL, background=PANEL,
                        foreground=TEXT, arrowcolor=TEXT)
        style.configure("TEntry", fieldbackground=PANEL, foreground=TEXT)
        # the combobox dropdown is a tk Listbox, styled via the option database
        self.option_add("*TCombobox*Listbox.background", PANEL)
        self.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", ACTIVE)
        self.option_add("*TCombobox*Listbox.selectForeground", TEXT)

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
                  wraplength=180, foreground=MUTED
                  ).grid(row=3, column=0, columnspan=2, sticky="w")

        ttk.Button(img_frame, text="Clear image",
                   command=self._clear_image).grid(row=4, column=0, columnspan=2,
                                                    sticky="ew", pady=(4, 0))

        # color picker (distance-gradient base color)
        color_frame = ttk.LabelFrame(ctrl, text="Color", padding=6)
        color_frame.grid(row=6, column=0, sticky="ew", pady=(0, 8))
        self._colorize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(color_frame, text="Colorize", variable=self._colorize_var,
                        command=self._on_colorize_toggle
                        ).grid(row=0, column=0, columnspan=len(COLORS),
                               sticky="w", pady=(0, 4))
        for i, (name, rgb) in enumerate(COLORS):
            btn = tk.Button(color_frame, width=2, bg=_hex(rgb),
                            relief="raised", bd=2,
                            command=lambda idx=i: self._on_color(idx))
            btn.grid(row=1, column=i, padx=2)
            self._swatches.append(btn)
        self._on_color(0)  # select default

        # action buttons
        ttk.Button(ctrl, text="Generate", command=self._generate
                   ).grid(row=7, column=0, sticky="ew", pady=(4, 2))
        ttk.Button(ctrl, text="Save image…", command=self._save
                   ).grid(row=8, column=0, sticky="ew", pady=(0, 4))

        self._status_var = tk.StringVar(value="Ready.")
        ttk.Label(ctrl, textvariable=self._status_var, wraplength=200,
                  foreground=MUTED).grid(row=9, column=0, sticky="w")

        # ── right panel (preview) ─────────────────────────────────────────
        preview = ttk.Frame(self, padding=10)
        preview.grid(row=0, column=1, sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._canvas = tk.Canvas(preview, bg=CANVAS_BG, highlightthickness=0,
                                 width=600, height=600)
        self._canvas.pack(fill="both", expand=True)

    # ── event handlers ────────────────────────────────────────────────────

    def _on_grid_type_change(self, *_):
        polar = self._grid_var.get() == "Polar (Circular)"
        state = "disabled" if polar else "normal"
        self._cols_label.configure(foreground=MUTED if polar else TEXT)
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

    def _on_color(self, idx):
        self._base_color = COLORS[idx][1]
        for i, btn in enumerate(self._swatches):
            btn.configure(relief="sunken" if i == idx else "raised")

    def _on_colorize_toggle(self):
        # grey out the swatches when coloring is off
        state = "normal" if self._colorize_var.get() else "disabled"
        for btn in self._swatches:
            btn.configure(state=state)

    def _generate(self):
        try:
            self._status_var.set("Generating…")
            self.update_idletasks()
            grid = self._build_grid()
            algo = ALGORITHMS[self._algo_var.get()]()
            algo.on(grid)
            # colored grids need a distance map + base color before to_png();
            # skip it for a plain black-on-white maze (bg_color then returns None)
            if self._colorize_var.get() and isinstance(grid, ColoredGrid):
                grid.set_distances(grid.random_cell().get_distances())
                grid.set_base_color(self._base_color)
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
            return ColoredPolar(rows)

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
        img_fit.thumbnail((canvas_w, canvas_h), Image.Resampling.LANCZOS)
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
