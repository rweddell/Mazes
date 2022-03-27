
from foundations.polar_grid import PolarGrid
from foundations.mask import Mask
from foundations.masked_grid import MaskedGrid
from algorithms.recursive_backtrack import RecursiveBacktracker as rb
from algorithms.aldous_broder import AldousBroder

temp = Mask(10, 10)
temp.set_bit(0, 0, value=False)
temp.set_bit(2, 2, value=False)
temp.set_bit(3, 3, value=False)
temp.set_bit(4, 4, value=False)

#Shows values of mask in table format
'''
for row in temp.bits:
    stringy = ''
    for bit in row:
        if bit is True:
            stringy += 'x'
        else:
            stringy += ' '
    print(stringy)
print()
'''

algo = rb()
grid = algo.on(MaskedGrid(temp))
print(grid)
img = grid.to_png()
img.save('output\maskdemo.png')

grid = algo.on(PolarGrid(10))
#print(grid)
img = grid.to_png()
img.save('output\rounddemo.png')