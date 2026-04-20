from PIL import Image, ImageFilter, ImageOps
from maze_structures.mask import Mask
import urllib.request
import io


def from_image_edges(img: Image.Image, max_dim: int = 80, threshold: int = 30) -> Mask:
    """
    Build a Mask from edge detection on an image.
    Edge pixels become disabled cells (False); non-edge areas are open (True).
    :param img: PIL Image
    :param max_dim: scale longest side to this many cells
    :param threshold: edge intensity cutoff (0-255)
    :return: Mask
    """
    img = img.convert('L')
    scale = max_dim / max(img.width, img.height)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    edges = img.filter(ImageFilter.FIND_EDGES)
    mask = Mask(new_h, new_w)
    pixels = edges.load()
    for row in range(new_h):
        for col in range(new_w):
            mask.set_bit(row, col, pixels[col, row] <= threshold)
    return mask


def from_image_shape(img: Image.Image, max_dim: int = 80, bg_threshold: int = 200) -> Mask:
    """
    Build a Mask from the non-background shape of an image.
    Light/white background pixels become disabled cells; the shape interior is open.
    :param img: PIL Image
    :param max_dim: scale longest side to this many cells
    :param bg_threshold: pixels brighter than this are treated as background
    :return: Mask
    """
    img = img.convert('L')
    scale = max_dim / max(img.width, img.height)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    mask = Mask(new_h, new_w)
    pixels = img.load()
    for row in range(new_h):
        for col in range(new_w):
            mask.set_bit(row, col, pixels[col, row] < bg_threshold)
    return mask


def load_image_from_path(path: str) -> Image.Image:
    return Image.open(path)


def load_image_from_url(url: str) -> Image.Image:
    with urllib.request.urlopen(url) as response:
        data = response.read()
    return Image.open(io.BytesIO(data))
