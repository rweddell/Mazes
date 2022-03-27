
from Foundations.PolarGrid import PolarGrid
from Foundations.Mask import Mask
from Foundations.MaskedGrid import MaskedGrid
from Algorithms.RecursiveBacktracker import RecursiveBacktracker as rb
from Algorithms.AldousBroder import AldousBroder

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

harry = rb()
grid = harry.on(MaskedGrid(temp))
print(grid)
img = grid.to_png()
img.save('Output\maskdemo.png')

grid = harry.on(PolarGrid(10))
#print(grid)
img = grid.to_png()
img.save('Output\\rounddemo.png')