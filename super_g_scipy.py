
import numpy as np


def super_g(xy, amplitude, x_mean, y_mean, x_stddev, y_stddev, power):
    #print(amplitude, x_mean, y_mean, x_stddev, y_stddev, power)
    """Two dimensional Gaussian function"""
    x, y = xy
    xstd2 = x_stddev**2
    ystd2 = y_stddev**2
    xdiff = x - x_mean
    ydiff = y - y_mean
    xdiff2 = xdiff**2
    ydiff2 = ydiff**2
    exponent = np.divide(xdiff2, 2*xstd2)+np.divide(ydiff2, 2*ystd2)
    g = amplitude*np.exp(-(exponent**power))
    #print(amplitude, x_mean, y_mean, x_stddev, y_stddev, power)
    return g.ravel()

