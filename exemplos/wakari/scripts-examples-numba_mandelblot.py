from numba import autojit
import numpy as np
#from pylab import imshow, jet, show, ion
import matplotlib
matplotlib.use('agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pylab import *

@autojit
def mandel(x, y, max_iters):
   """
   Given the real and imaginary parts of a complex number,
determine if it is a candidate for membership in the Mandelb
rot
   set given a fixed number of iterations.
   """
   i = 0
   c = complex(x,y)
   z = 0.0j
   for i in range(max_iters):
       z = z*z + c
       if (z.real*z.real + z.imag*z.imag) >= 4:
           return i

   return 255

@autojit
def create_fractal(min_x, max_x, min_y, max_y, image, iters):
   height = image.shape[0]
   width = image.shape[1]

   pixel_size_x = (max_x - min_x) / width
   pixel_size_y = (max_y - min_y) / height
   for x in range(width):
       real = min_x + x * pixel_size_x
       for y in range(height):
           imag = min_y + y * pixel_size_y
           color = mandel(real, imag, iters)
           #color = 130
           image[y, x] = color

   return image

try:
    image = np.zeros((500, 750), dtype=np.uint8)
    #print create_fractal.lfunc
    result = create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20)

    # Save to file and cat out the file.
    from subprocess import call
    fname='pie.png'
    matplotlib.pyplot.imsave(fname, result)
    call(["cat",fname])
except Exception as e:
    print e
    
#jet()
#ion()
#show()
