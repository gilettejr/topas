#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# file_name.py
# Python 3.8.3
"""
Author: Joseph Bateman
Created: Wed Jun 16 16:56:02 2021
Modified: Wed Jun 16 16:56:02 2021

Description
-------------

"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

# number of points for plotting/interpolation

N = 10008

# insert file generated from topas with header removed
x, y, z = np.genfromtxt(r'dosemap.csv', unpack=True, delimiter=',')

xi = np.linspace(x.min(), x.max(), N)
yi = np.linspace(y.min(), y.max(), N)
zi = scipy.interpolate.griddata(
    (x, y), z, (xi[None, :], yi[:, None]), method='cubic')

fig = plt.figure()
plt.contourf(xi, yi, zi, 20, cmap='jet')
plt.title("Dose Map")
plt.xlabel("Width (cm)")
plt.ylabel("Height (cm)")
plt.colorbar(label='Dose(Gy)')
plt.show()
