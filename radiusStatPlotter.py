#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:46:00 2023

@author: robertsoncl
"""
from allStatPlotter import allStatPlotter
import numpy as np
import matplotlib.pyplot as plt


class radiusStatPlotter(allStatPlotter):

    def plotKurtoses(self, radiusRange):
        file_prestr = 'flat'
        file_poststr = str(round(0.0001, 1))+str(round(150, 0)) + \
            str(round(0, 1))+str(1000000)+'10Aluminum'+str(1000)
        print(file_poststr)
        dataArray = []
        for i in range(len(radiusRange)):
            dataArray.append(self.unpackStats(
                self.folder+file_prestr+str(round(radiusRange[i], 1))+file_poststr))
        da = np.transpose(np.array(dataArray))
        # dataArray[thicknesses][sigs,sig_uncs,kurts,kurt_uncs][topas,moliere,pdg][1sig,2sig,3sig,4sig,5sig]
        fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
        print(da[1][0][3])
        ax[0].set_title('Measured Kurtosis, 2$\sigma$ cutoff')
        ax[0].errorbar(radiusRange, da[1][0][2], yerr=da
                       [1][0][3], label='TOPAS', color='black', capsize=2)
        ax[0].errorbar(radiusRange, da[1][1][2], yerr=da
                       [1][1][3], label='Moliere', color='blue', capsize=2)
        ax[0].errorbar(radiusRange, da[1][2][2], yerr=da
                       [1][2][3], label='Gaussian', color='red', capsize=2)
        #ax[0].set_xlabel('Initial Beam Radius [mm]')
        ax[0].set_ylabel('Beamsize [mm]')
        ax[0].grid(True)

        ax[1].set_title('Measured Kurtosis, 5$\sigma$ cutoff')
        ax[1].errorbar(radiusRange, da[4][0][2], yerr=da[4]
                       [0][3], label='TOPAS', color='black', capsize=2)
        ax[1].errorbar(radiusRange, da[4][1][2], yerr=da[4]
                       [1][3], label='Moliere', color='blue', capsize=2)
        ax[1].errorbar(radiusRange, da[4][2][2], yerr=da[4][2][3],
                       label='Gaussian', color='red', capsize=2)
        ax[1].set_xlabel('Initial Beam Radius [mm]')
        ax[1].set_ylabel('Kurtosis')
        ax[1].grid(True)

        ax[0].legend()

    def plotSigmas(self, radiusRange):

        file_prestr = 'flat'
        file_poststr = str(round(0.0001, 1))+str(round(150, 0)) + \
            str(round(0, 1))+str(1000000)+'10Aluminum'+str(1000)
        print(file_poststr)
        dataArray = []
        for i in range(len(radiusRange)):
            dataArray.append(self.unpackStats(
                self.folder+file_prestr+str(round(radiusRange[i], 1))+file_poststr))
        da = np.transpose(np.array(dataArray))
        print(np.shape(da))
        # dataArray[thicknesses][sigs,sig_uncs,kurts,kurt_uncs][topas,moliere,pdg][1sig,2sig,3sig,4sig,5sig]
        fig, ax = plt.subplots(2, 2, figsize=(8, 8), sharex=True)
        ax[0][0].set_title('Measureed Beamsize, 2$\sigma$ cutoff')
        ax[0][0].errorbar(radiusRange, da[1][0][0], yerr=da
                          [1][0][1], label='TOPAS', color='black', capsize=2)
        ax[0][0].errorbar(radiusRange, da[1][1][0], yerr=da
                          [1][1][1], label='Moliere', color='blue', capsize=2)
        ax[0][0].errorbar(radiusRange, da[1][2][0], yerr=da
                          [1][2][1], label='Gaussian', color='red', capsize=2)
        #ax[0].set_xlabel('Initial Beam Radius [mm]')
        ax[0][0].set_ylabel('Beamsize [mm]')
        ax[0][0].grid(True)

        ax[1][0].set_title('Measured Beamsize, 5$\sigma$ cutoff')
        ax[1][0].errorbar(radiusRange, da[4][0][0], yerr=da[4]
                          [0][1], label='TOPAS', color='black', capsize=2)
        ax[1][0].errorbar(radiusRange, da[4][1][0], yerr=da[4]
                          [1][1], label='Moliere', color='blue', capsize=2)
        ax[1][0].errorbar(radiusRange, da[4][2][0], yerr=da[4][2][1],
                          label='Gaussian', color='red', capsize=2)
        ax[1][0].set_xlabel('Initial Beam Radius [mm]')
        ax[1][0].set_ylabel('Beamsize [mm]')
        ax[1][0].grid(True)

        ax[0][1].set_title('Normalised Discrepancies, 2$\sigma$ cutoff')
        ax[0][1].errorbar(radiusRange, ((da[1][0][0]-da[1][2][0])/da[1][2][0])*100, yerr=(np.sqrt(da
                          [1][0][1]**2+da[1][2][1]**2)/da[1][2][0])*100, label='TOPAS', color='black', capsize=2)
        ax[0][1].errorbar(radiusRange, ((da[1][1][0]-da[1][2][0])/da[1][2][0])*100, yerr=(np.sqrt(da
                          [1][1][1]**2+da[1][2][1]**2)/da[1][2][0])*100, label='Moliere', color='blue', capsize=2)
        ax[0][1].errorbar(radiusRange, ((da[1][2][0]-da[1][2][0])/da[1][2][0])*100, yerr=da
                          [1][2][1], label='Gaussian', color='red', capsize=2)
        #ax[0].set_xlabel('Initial Beam Radius [mm]')
        ax[0][1].set_ylabel('Discrepancy from Gaussian [%]')
        ax[0][1].grid(True)

        ax[1][1].set_title('Normalised Discrepancies, 5$\sigma$ cutoff')
        ax[1][1].errorbar(radiusRange, ((da[4][0][0]-da[4][2][0])/da[4][2][0])*100, yerr=(np.sqrt(da
                          [4][0][1]**2+da[4][2][1]**2)/da[4][2][0])*100, label='TOPAS', color='black', capsize=2)
        ax[1][1].errorbar(radiusRange, ((da[4][1][0]-da[4][2][0])/da[4][2][0])*100, yerr=(np.sqrt(da
                          [4][1][1]**2+da[4][2][1]**2)/da[4][2][0]), label='Moliere', color='blue', capsize=2)
        ax[1][1].errorbar(radiusRange, ((da[4][2][0]-da[4][2][0])/da[4][2][0])*100, yerr=da[4][2][1],
                          label='Gaussian', color='red', capsize=2)
        ax[1][1].set_xlabel('Initial Beam Radius [mm]')
        ax[1][1].set_ylabel('Discrepancy from Gaussian [%]')
        ax[1][1].grid(True)
        ax[0][0].legend()
