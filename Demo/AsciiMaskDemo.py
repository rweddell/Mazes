
from Foundations.Mask import *
from Foundations.MaskedGrid import MaskedGrid
from Algorithms.RecursiveBacktracker import RecursiveBacktracker

recback = RecursiveBacktracker()

mask = from_txt('Output\masktext.txt')
grid = recback.on(MaskedGrid(mask))
img = grid.to_png()
img.save('Output\mascii.png')

'''
mask = from_png('Output\mazeimg.png')
grid = recback.on(MaskedGrid(mask))
img = grid.to_png(size=10)
img.save('Output\pngmask.png')
'''

smallmask = from_png_scaled('Output\mazeimg.png')
smallgrid = recback.on(MaskedGrid(smallmask))
smallimage = smallgrid.to_png(size=10)
smallimage.save('Output\shrunken.png')
