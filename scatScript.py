#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:53:59 2023

@author: robertsoncl
"""
from additionScript import additionScript
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle


class scatScript(additionScript):
    def addFlatScatterer(self, thickness, material, position=2):
        file = self.openFile()
        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/S1/Material=" + '"' + material + '"' + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  100  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(thickness / 2) + " mm\n")
        # set position of scatterer so that the edge is on the origin
        file.write("d:Ge/S1/TransZ = -" +
                   str(position+thickness / 2) + " mm\n")
        file.close()
        self.s1_geometry = thickness

    # position here refers to downstream face of scatterer (don't ask me why)
    # convolution factor = 1 for standard Gaussian scatterer
    def addGaussianScatterer(self, max_thickness, radius, convolution_factor, N_slices, material, position, show_shape=False, thickness_limit=False):
        file = self.openFile()

        s2_sigma = radius/2
        # define spread of gaussian shape
        # and precision (number of slices in shape) with step argument
        # x = np.arange(-half_width, half_width, step=1)
        step = radius / (N_slices)
        x = np.arange(-(radius+step), 0, step=step)
        # construct gaussian profile from method argument sigma
        # convolution factor "warps" shape
        y = norm.pdf(x, 0, s2_sigma * convolution_factor)
        # plt.plot(x, y)
        # scale for input amplitude
        y = y - min(y)
        y_scaling_factor = max_thickness / max(y)
        y = y * y_scaling_factor
        if show_shape is True:
            plt.plot(np.append(x, -np.flip(x, 0)), np.append(y, np.flip(y)))
            plt.xlabel('r[mm]')
            plt.ylabel('h[mm]')
        # scale height and normalise base to 0
        # according to method argument max_height
        slice_radius = []
        slice_thickness = []
        slice_position = []

        # begin loop to create stack of cylinders following Gaussian shape
        for i in range(1, len(y)):
            # Don't try to create 0 height widths
            # skip relevant rows
            L = y[i] - y[i - 1]
            if thickness_limit is False or L > thickness_limit:
                HL = L / 2

                slice_radius.append(abs(x[i]))
                slice_thickness.append(L)

                # define slice name - required for Topas
                sname = "slice" + str(i)
                file.write("d:Ge/" + sname + "/HL = " + str(HL) + " mm\n")
                prev_HL = HL
                # define slice as cylinder
                file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
                # in previously defined world
                file.write("s:Ge/" + sname + '/Parent="World"\n')
                # define material

                file.write("s:Ge/" + sname + "/Material=" +
                           '"' + material + '"' + "\n")
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
                    + "/TransZ = -"
                    + str(position - y[i - 1] - L / 2)
                    + " mm\n"
                )
                slice_position.append(position - y[i - 1] - L / 2)

            # increment to begin next slice until shape completion
            i = i + 1
        s2_geometry = pd.DataFrame(
            {'slice_radius': slice_radius, 'slice_thickness': slice_thickness, 'slice_position': slice_position})
        file.close()
        self.s2_geometry = s2_geometry

    def displayScatterers(self):
        s2_geometry = self.s2_geometry
        fig, ax = plt.subplots(2, 1, figsize=(7, 6))
        ax[0].set_xlim([-25, 25])
        ax[0].set_ylim([-2, self.s1_geometry*5])
        ax[0].set_ylabel('z [mm]')
        ax[0].set_xlabel('r [mm]')
        s1_xy = [-10, 0]
        s1 = Rectangle(s1_xy, 20,
                       self.s1_geometry, fc='None', ec='k')
        ax[0].add_patch(s1)
        ax[0].annotate('S1, L='+str(self.s1_geometry) +
                       'mm', [-20, 0])

        for i in self.s2_geometry.index:
            s2_xy = np.array([-s2_geometry['slice_radius'].at[i],
                              s2_geometry['slice_position'].at[i]-s2_geometry['slice_thickness'].at[i]/2])
            s2_slice = Rectangle(s2_xy,
                                 2*s2_geometry['slice_radius'].at[i], s2_geometry['slice_thickness'].at[i], fc='None', ec='k')
            ax[1].add_patch(s2_slice)
            an_string = 'Slice '+str(i+1)+', r='+str(round(s2_geometry['slice_radius'].at[i], 3))+'mm, L='+str(
                round(s2_geometry['slice_thickness'].at[i], 3))+'mm'
            ax[1].annotate(
                an_string, s2_xy-np.array([max(s2_geometry['slice_radius'])*1.5, 0]), fontsize=9, color='k')
        ax[1].set_xlim(-max(s2_geometry['slice_radius'])*2-1,
                       max(s2_geometry['slice_radius'])*2)
        ax[1].set_ylim(min(s2_geometry['slice_position'])-1,
                       max(s2_geometry['slice_position'])+1)
        ax[1].set_ylabel('z [mm]')
        ax[1].set_xlabel('r [mm]')
