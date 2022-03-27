
from foundations.mask import *
from foundations.masked_grid import MaskedGrid
from algorithms.recursive_backtrack import RecursiveBacktracker

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
smallimage.save('output\shrunken_maschii.png')
