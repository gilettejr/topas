#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 16:40:27 2023

@author: robertsoncl
"""
import matplotlib.pyplot as plt
import scipy.interpolate
from astropy.modeling import models, fitting
import gc
from topas2numpy import BinnedResult
import cv2
import matplotlib.colors as mc
import numpy as np


class partrecDosePlotter:
    # import phase space from defined file
    def __init__(self, doseFilePath, nParticles, binTomm):

        # insert file generated from topas with header removed
        #x, y, z, d = np.genfromtxt(saveDir+'1000x1200Bins.csv', unpack=True, delimiter=',')

        # generate coordinates between bins for plotting
        #xi = np.linspace(x.min(), x.max(), N)
        #yi = np.linspace(y.min(), y.max(), N)
        # define how dose should be interpolated between bins
        # di = scipy.interpolate.griddata((x, y), d, (xi[None,:], yi[:,None]), method='cubic') #method: ‘linear’, ‘nearest’ or ‘cubic’
        dosemap = np.squeeze(BinnedResult(doseFilePath).data['Sum'])
        self.basicDosemap = dosemap
        self.nParticles = nParticles

    def setCharge(self, chargenC):

        # %%simulation settings
        # X in 10 bins of 0.35 cm
        # Y in 10 bins of 0.405 cm
        # Z in 1 bin  of 0.0278 cm

        # water depth for scoring  # mm
        # number of simulated particles
        nPartSim = self.nParticles
        # charge to simulate for# nC
        # electron charge
        eCharge = 1.60217663e-19  # C
        # numer of particles to estimate total dose
        target_nPart = chargenC*1e-9 / eCharge
        scaling_factor = target_nPart/nPartSim
        print(scaling_factor)
        self.dosemap = self.basicDosemap*scaling_factor
        self.chargenC = chargenC
# %%plotting

    def plotDosemap(self):
        plt.rcParams['figure.autolayout'] = True
        textsize = 10
        # plt.ioff()
        fig = plt.figure()
        #plt.contourf(xi*0.35, yi*0.405, di*scaling_factor, 100, cmap='jet' )
        plt.imshow(self.dosemap, norm=mc.Normalize(),
                   interpolation='gaussian', extent=(-17.5, 17.5, -20.25, 20.25), cmap='jet')
        #cv2.imshow("Polar Image", polar_image)
        plt.title('Film Dose, ' + str(self.chargenC)+'nC')
        plt.xlabel("X (mm)", fontsize=textsize)
        plt.ylabel("Y (mm)", fontsize=textsize)
        plt.yticks(fontsize=textsize)
        plt.xticks(fontsize=textsize)
        cbar = plt.colorbar()
        cbar.ax.set_title('Dose(Gy)', fontsize=textsize)
        cbar.ax.tick_params(labelsize=textsize)
        plt.show()

    def plotDoseSlice(self, depthmm):
        plt.rcParams['figure.autolayout'] = True
        textsize = 10
        # plt.ioff()
        fig = plt.figure()
        # plt.contourf(xi*0.35, yi*0.405, di*scaling_factor, 100, cmap='jet' )

        bindepth = 50 - int(depthmm/6)
        plt.imshow(self.dosemap[:, :, bindepth],
                   interpolation='gaussian', extent=(-200, 200, -200, 200), cmap='jet', vmax=0.4, vmin=0)
        # cv2.imshow("Polar Image", polar_image)
        plt.title('Slice at '+str(depthmm) +
                  'mm, ' + str(self.chargenC)+'nC')
        plt.xlabel("X [mm]", fontsize=textsize)
        plt.ylabel("Y [mm]", fontsize=textsize)
        plt.yticks(fontsize=textsize)
        plt.xticks(fontsize=textsize)
        cbar = plt.colorbar()
        cbar.ax.set_title('Secondary Dose [Gy]', fontsize=textsize)
        cbar.ax.tick_params(labelsize=textsize)
        plt.show()

    def plotDoseOnAxis(self):
        plt.rcParams['figure.autolayout'] = True
        textsize = 10
        # plt.ioff()
        fig, ax = plt.subplots()
        onAxis = np.flip(
            np.mean(self.dosemap[24:27, 24:27, :], axis=(0, 1)))
        onAxiserr = np.flip(
            np.std(self.dosemap[24:27, 24:27, :], axis=(0, 1)))
        # plt.contourf(xi*0.35, yi*0.405, di*scaling_factor, 100, cmap='jet' )

        ax.plot(onAxis/max(onAxis), color='k', label='150 MeV')
        # cv2.imshow("Polar Image", polar_image)
        ax.set_title('Normalised on-axis dose')
        ax.set_xlabel("Depth [mm]", fontsize=textsize)
        ax.set_ylabel("Dose [arb.]", fontsize=textsize)
# plt.close(fig)
# gc.collect()
# show transverse beam profile and energy spectrum
# fov is field of view of profile graphs
# col is the virtual collimator radius for calculation of transmission
# both in millimetres
# mean energy is calculated within collimator radius only
