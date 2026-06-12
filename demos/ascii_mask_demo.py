
from mazes.structures.mask import *
from mazes.structures.masked_grid import MaskedGrid
from mazes.algorithms.recursive_backtrack import RecursiveBacktracker
from datetime import date

recback = RecursiveBacktracker()

mask = from_txt('Output\masktext.txt')
grid = recback.on(MaskedGrid(mask))
img = grid.to_png()
img.save('output\mascii.png')

'''
mask = from_png('Output\mazeimg.png')
grid = recback.on(MaskedGrid(mask))
img = grid.to_png(size=10)
img.save('Output\pngmask.png')
'''

smallmask = from_png_scaled('output\mazeimg.png')
smallgrid = recback.on(MaskedGrid(smallmask))
smallimage = smallgrid.to_png(size=10)
smallimage.save(f'output\shrunken_maschii_{date.today()}.png')
