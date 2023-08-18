#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:47:58 2023

@author: robertsoncl
"""
from allStatPlotter import allStatPlotter
import numpy as np
import matplotlib.pyplot as plt


class thickStatPlotter(allStatPlotter):

    def plotKurtoses(self, thicknessRange):
        file_prestr = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150, 0)) + \
            str(round(0, 1))+str(1000000)
        file_poststr = 'Aluminum'+str(1000)

        dataArray = []
        for i in range(len(thicknessRange)):
            dataArray.append(self.unpackStats(
                self.folder+file_prestr+str(thicknessRange[i])+file_poststr))
        da = np.transpose(np.array(dataArray))
        # dataArray[thicknesses][sigs,sig_uncs,kurts,kurt_uncs][topas,moliere,pdg][1sig,2sig,3sig,4sig,5sig]
        fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
        print(da[1][0][3])
        ax[0].set_title('Measured Kurtosis, 2$\sigma$ cutoff')
        ax[0].errorbar(thicknessRange, da[1][0][2], yerr=da
                       [1][0][3], label='TOPAS', color='black', capsize=2)
        ax[0].errorbar(thicknessRange, da[1][1][2], yerr=da
                       [1][1][3], label='Moliere', color='blue', capsize=2)
        ax[0].errorbar(thicknessRange, da[1][2][2], yerr=da
                       [1][2][3], label='Gaussian', color='red', capsize=2)
        #ax[0].set_xlabel('Thickness [mm]')
        ax[0].set_ylabel('Beamsize [mm]')
        ax[0].grid(True)
        ax[0].legend()

        ax[1].set_title('Measured Kurtosis, 5$\sigma$ cutoff')
        ax[1].errorbar(thicknessRange, da[4][0][2], yerr=da[4]
                       [0][3], label='TOPAS', color='black', capsize=2)
        ax[1].errorbar(thicknessRange, da[4][1][2], yerr=da[4]
                       [1][3], label='Moliere', color='blue', capsize=2)
        ax[1].errorbar(thicknessRange, da[4][2][2], yerr=da[4][2][3],
                       label='Gaussian', color='red', capsize=2)
        ax[1].set_xlabel('Thickness [mm]')
        ax[1].set_ylabel('Kurtosis')
        ax[1].grid(True)

    def plotSigmas(self, thicknessRange):

        file_prestr = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150, 0)) + \
            str(round(0, 1))+str(1000000)
        file_poststr = 'Aluminum'+str(1000)
        dataArray = []
        for i in range(len(thicknessRange)):
            dataArray.append(self.unpackStats(
                self.folder+file_prestr+str(thicknessRange[i])+file_poststr))
        da = np.transpose(np.array(dataArray))
        print(np.shape(da))
        # dataArray[thicknesses][sigs,sig_uncs,kurts,kurt_uncs][topas,moliere,pdg][1sig,2sig,3sig,4sig,5sig]
        fig, ax = plt.subplots(2, 2, figsize=(8, 8), sharex=True)
        ax[0][0].set_title('Measureed Beamsize, 2$\sigma$ cutoff')
        ax[0][0].errorbar(thicknessRange, da[1][0][0], yerr=da
                          [1][0][1], label='TOPAS', color='black', capsize=2)
        ax[0][0].errorbar(thicknessRange, da[1][1][0], yerr=da
                          [1][1][1], label='Moliere', color='blue', capsize=2)
        ax[0][0].errorbar(thicknessRange, da[1][2][0], yerr=da
                          [1][2][1], label='Gaussian', color='red', capsize=2)
        #ax[0].set_xlabel('Thickness [mm]')
        ax[0][0].set_ylabel('Beamsize [mm]')
        ax[0][0].grid(True)

        ax[1][0].set_title('Measured Beamsize, 5$\sigma$ cutoff')
        ax[1][0].errorbar(thicknessRange, da[4][0][0], yerr=da[4]
                          [0][1], label='TOPAS', color='black', capsize=2)
        ax[1][0].errorbar(thicknessRange, da[4][1][0], yerr=da[4]
                          [1][1], label='Moliere', color='blue', capsize=2)
        ax[1][0].errorbar(thicknessRange, da[4][2][0], yerr=da[4][2][1],
                          label='Gaussian', color='red', capsize=2)
        ax[1][0].set_xlabel('Thickness [mm]')
        ax[1][0].set_ylabel('Beamsize [mm]')
        ax[1][0].grid(True)

        ax[0][1].set_title('Normalised Discrepancies, 2$\sigma$ cutoff')
        ax[0][1].errorbar(thicknessRange, ((da[1][0][0]-da[1][2][0])/da[1][2][0])*100, yerr=(np.sqrt(da
                          [1][0][1]**2+da[1][2][1]**2)/da[1][2][0])*100, label='TOPAS', color='black', capsize=2)
        ax[0][1].errorbar(thicknessRange, ((da[1][1][0]-da[1][2][0])/da[1][2][0])*100, yerr=(np.sqrt(da
                          [1][1][1]**2+da[1][2][1]**2)/da[1][2][0])*100, label='Moliere', color='blue', capsize=2)
        ax[0][1].errorbar(thicknessRange, ((da[1][2][0]-da[1][2][0])/da[1][2][0])*100, yerr=da
                          [1][2][1], label='Gaussian', color='red', capsize=2)
        #ax[0].set_xlabel('Thickness [mm]')
        ax[0][1].set_ylabel('Discrepancy from Gaussian [%]')
        ax[0][1].grid(True)

        ax[1][1].set_title('Normalised Discrepancies, 5$\sigma$ cutoff')
        ax[1][1].errorbar(thicknessRange, ((da[4][0][0]-da[4][2][0])/da[4][2][0])*100, yerr=(np.sqrt(da
                          [4][0][1]**2+da[4][2][1]**2)/da[4][2][0])*100, label='TOPAS', color='black', capsize=2)
        ax[1][1].errorbar(thicknessRange, ((da[4][1][0]-da[4][2][0])/da[4][2][0])*100, yerr=(np.sqrt(da
                          [4][1][1]**2+da[4][2][1]**2)/da[4][2][0]), label='Moliere', color='blue', capsize=2)
        ax[1][1].errorbar(thicknessRange, ((da[4][2][0]-da[4][2][0])/da[4][2][0])*100, yerr=da[4][2][1],
                          label='Gaussian', color='red', capsize=2)
        ax[1][1].set_xlabel('Thickness [mm]')
        ax[1][1].set_ylabel('Discrepancy from Gaussian [%]')
        ax[1][1].grid(True)
        ax[0][0].legend()

    def plotRFSigmas(self, thicknessRange):

        file_prestr = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150, 0)) + \
            str(round(0, 1))+str(1000000)
        file_poststr = 'Aluminum'+str(1000)
        dataArray = []
        RFArray = []
        for i in range(len(thicknessRange)):
            dataArray.append(self.unpackStats(
                self.folder+file_prestr+str(thicknessRange[i])+file_poststr))
            RFArray.append(self.unpackRFStats(
                self.folder+'RF/'+file_prestr+str(thicknessRange[i])+file_poststr))
        da = np.transpose(np.array(dataArray))
        rfa = np.transpose(np.array(RFArray))
        print(np.shape(da))
        # dataArray[thicknesses][sigs,sig_uncs,kurts,kurt_uncs][topas,moliere,pdg][1sig,2sig,3sig,4sig,5sig]
        fig, ax = plt.subplots(2, 2, figsize=(10, 8), sharex=True)
        ax[0][0].set_title('Measureed Beamsize, 2$\sigma$ cutoff')
        ax[0][0].errorbar(thicknessRange, da[1][0][0], yerr=da
                          [1][0][1], label='TOPAS', color='black', capsize=2)
        ax[0][0].errorbar(thicknessRange, rfa[1][0], yerr=rfa
                          [1][1], label='RF', color='blue', capsize=2)

        #ax[0].set_xlabel('Thickness [mm]')
        ax[0][0].set_ylabel('Beamsize [mm]')
        ax[0][0].grid(True)

        ax[1][0].set_title('Measured Beamsize, 5$\sigma$ cutoff')
        ax[1][0].errorbar(thicknessRange, da[4][0][0], yerr=da[4]
                          [0][1], label='TOPAS', color='black', capsize=2)
        ax[1][0].errorbar(thicknessRange, rfa[4][0], yerr=rfa[4]
                          [1], label='Moliere', color='blue', capsize=2)

        ax[1][0].set_xlabel('Thickness [mm]')
        ax[1][0].set_ylabel('Beamsize [mm]')
        ax[1][0].grid(True)

        ax[0][1].set_title('Normalised Discrepancies, 2$\sigma$ cutoff')
        ax[0][1].errorbar(thicknessRange, ((da[1][0][0]-da[1][2][0])/da[1][2][0])*100, yerr=(np.sqrt(da
                          [1][0][1]**2+da[1][2][1]**2)/da[1][2][0])*100, label='TOPAS', color='black', capsize=2)
        ax[0][1].errorbar(thicknessRange, ((rfa[1][0]-da[1][2][0])/da[1][2][0])*100, yerr=(np.sqrt(rfa
                          [1][1]**2+da[1][2][1]**2)/da[1][2][0])*100, label='Moliere', color='blue', capsize=2)

        #ax[0].set_xlabel('Thickness [mm]')
        ax[0][1].set_ylabel('Discrepancy from Gaussian [%]')
        ax[0][1].grid(True)

        ax[1][1].set_title('Normalised Discrepancies, 5$\sigma$ cutoff')
        ax[1][1].errorbar(thicknessRange, ((da[4][0][0]-da[4][2][0])/da[4][2][0])*100, yerr=(np.sqrt(da
                          [4][0][1]**2+da[4][2][1]**2)/da[4][2][0])*100, label='TOPAS', color='black', capsize=2)
        ax[1][1].errorbar(thicknessRange, ((rfa[4][0]-da[4][2][0])/da[4][2][0])*100, yerr=(np.sqrt(
                          rfa[4][1]**2+da[4][2][1]**2)/da[4][2][0]), label='Moliere', color='blue', capsize=2)

        ax[1][1].set_xlabel('Thickness [mm]')
        ax[1][1].set_ylabel('Discrepancy from Gaussian [%]')
        ax[1][1].grid(True)
        ax[0][0].legend()

    def plotRFKurtoses(self, thicknessRange):
        file_prestr = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150, 0)) + \
            str(round(0, 1))+str(1000000)
        file_poststr = 'Aluminum'+str(1000)
        dataArray = []
        RFArray = []
        for i in range(len(thicknessRange)):
            dataArray.append(self.unpackStats(
                self.folder+file_prestr+str(thicknessRange[i])+file_poststr))
            RFArray.append(self.unpackRFStats(
                self.folder+'RF/'+file_prestr+str(thicknessRange[i])+file_poststr))
        da = np.transpose(np.array(dataArray))
        rfa = np.transpose(np.array(RFArray))
        # dataArray[thicknesses][sigs,sig_uncs,kurts,kurt_uncs][topas,moliere,pdg][1sig,2sig,3sig,4sig,5sig]
        fig, ax = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

        ax[0].set_title('Measured Kurtosis, 2$\sigma$ cutoff')
        ax[0].errorbar(thicknessRange, da[1][0][2], yerr=da
                       [1][0][3], label='TOPAS', color='black', capsize=2)
        ax[0].errorbar(thicknessRange, rfa[1][2], yerr=rfa
                       [1][3], label='RF', color='blue', capsize=2)

        #ax[0].set_xlabel('Thickness [mm]')
        ax[0].set_ylabel('Beamsize [mm]')
        ax[0].grid(True)
        ax[0].legend()

        ax[1].set_title('Measured Kurtosis, 5$\sigma$ cutoff')
        ax[1].errorbar(thicknessRange, da[4][0][2], yerr=da[4]
                       [0][3], label='TOPAS', color='black', capsize=2)
        ax[1].errorbar(thicknessRange, rfa[4][2], yerr=rfa[4]
                       [3], label='RF', color='blue', capsize=2)

        ax[1].set_xlabel('Thickness [mm]')
        ax[1].set_ylabel('Kurtosis')
        ax[1].grid(True)
