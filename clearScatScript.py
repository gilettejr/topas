#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 15:54:10 2023

@author: robertsoncl
"""
from additionScript import additionScript
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle


class clearScatScript(additionScript):
    def __init__(self):
        super(additionScript, self).__init__(home_directory="/home/robertsoncl/",
                                             input_filename="partrec_test")

        def generateClearScat(file, sigma,
                              max_height,
                              shape_radius,
                              positionmm,
                              show_shape=False,
                              N_slices=40,
                              sigma_x=0.86,
                              sigma_y=1.14,
                              sigma_px=4.17,
                              sigma_py=3.26,
                              material='"G4_NYLON-6-6"', slice_half_thickness_limit=2):
            x_di = 200
            step = x_di / N_slices
            slice_no = x_di / step
            x_old = np.arange(-100, 100, step=step)
            # define expectation value of Gaussian = 0 for symmetry
            mu = 0
            # construct gaussian profile from method argument sigma
            y = norm.pdf(x_old, mu, sigma)
            x = []
            for i in range(len(y)):
                if y[i] < 1e-12:
                    x.append(np.nan)
                else:
                    x.append(x_old[i])
            # plt.plot(x, y)
            x = np.array(x)
            x = x[np.logical_not(np.isnan(x))]
            x_new_di = x.max() - x.min()
            x_new = np.arange(x.min(), x.max(), step=x_new_di / slice_no)
            y = norm.pdf(x_new, mu, sigma)
            # scale height and normalise base to 0
            # according to method argument max_height

            y = y - min(y)
            y_scaling_factor = max_height / max(y)
            y = y * y_scaling_factor
            x = x_new

            old_radius = max(x)
            x = x * shape_radius / old_radius

            # define half_y for ease, as Topas uses half lengths
            half_y = y / 2

            i = 1
            # begin loop to create stack of cylinders following Gaussian shape
            while x[i] < 0:
                # Don't try to create 0 height widths
                # skip relevant rows
                if half_y[i] - half_y[i - 1] <= 0:
                    i = i + 1
                    continue

                else:
                    if i == 1:
                        prev_HL = 0
                    HL = (y[i] - y[i - 1]) - prev_HL
                    if HL <= 0:
                        break
                    elif HL < slice_half_thickness_limit or abs(x[i]) < 2.5:
                        i = i + 1
                        continue

                    # define slice name - required for Topas
                    sname = "slice" + str(i)
                    #file.write("d:Ge/" + sname + "/TransX = 1 mm\n")
                    file.write("d:Ge/" + sname + "/HL = " + str(HL) + " mm\n")
                    prev_HL = HL
                    # define slice as cylinder
                    file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
                    # in previously defined world
                    file.write("s:Ge/" + sname + '/Parent="World"\n')
                    # define material
                    file.write("s:Ge/" + sname +
                               "/Material=" + material + "\n")
                    # set radius of slice from horizontal slice steps
                    file.write("d:Ge/" + sname + "/Rmax = " +
                               str(abs(x[i])) + " mm\n")
                    # set inner radius of slice to 0 - slice is solid, not a hoop
                    file.write("d:Ge/" + sname + "/Rmin= 0 mm\n")
                    # define height of slice from difference between y values
                    # of points from defined Gaussian shape
                    # set position to build Gaussian pointed toward beam
                    # with distance beam_to_S2 from beam source to tip
                    # and distance S2_to_scorer from shape base
                    file.write(
                        "d:Ge/"
                        + sname
                        + "/TransZ = "
                        + str(y[i] - (max_height / 2 + positionmm))
                        + " mm\n"
                    )
            self.generateClearScat = generateClearScat

    def addBKScatterer(self, basepositionmm):
        file = self.openFile()
        bp_orig = 384.86371046497
        self.generateClearScat(file, sigma=19.52898,
                               max_height=110.0,
                               shape_radius=24.28, positionmm=basepositionmm-(bp_orig-335), N_slices=30)

    def addAl1Scatterer(self, basepositionmm):
        file = self.openFile()
        bp_orig = 0
        self.generateClearScat(file, sigma=18.52898, max_height=30.0, shape_radius=25, positionmm=basepositionmm-(
            bp_orig-381), N_slices=30, material='Aluminum', slice_half_thickness_limit=0.5)

    def addAl2Scatterer(self, basepositionmm):
        file = self.openFile()
        bp_orig = 0
        self.generateClearScat(file, sigma=18.52898, max_height=35.0, shape_radius=20, positionmm=basepositionmm-(
            bp_orig-335), N_slices=30, material='Aluminum', slice_half_thickness_limit=0.5)

    def addAl3Scatterer(self, basepositionmm):
        file = self.openFile()
        bp_orig = 0
        self.generateClearScat(file, sigma=18.52898, max_height=35.0, shape_radius=15.3, positionmm=basepositionmm-(
            bp_orig-181), N_slices=30, material='Aluminum', slice_half_thickness_limit=0.5)
