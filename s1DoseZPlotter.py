#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:06:55 2023

@author: robertsoncl
"""
from partrecDosePlotter import partrecDosePlotter
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import kurtosis

import sys
sys.path.append('/home/robertsoncl/dphil/rf-track-2.1.6/')


class s1DoseZPlotter:
    def plotZScan(self, ddBins='auto'):
        from moliere_dist import camscat
        element_list = ['Lithium', 'Carbon', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Calcium', 'Titanium', 'Chromium',
                        'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Silver', 'Tantalum', 'Tungsten', 'Platinum', 'Gold', 'Lead']
        folder = '/home/robertsoncl/dphil/s1Data/Doses/'
        filestrings = []
        for i in element_list:
            scat = camscat()
            new_thick = scat.convertPDGMaterial(150.0, 'Aluminum', 10, i)
            filestrings.append(folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) +
                               str(round(0, 1))+str(10000)+str(round(new_thick, 1)) +
                               i+str(1000))

        ts = []
        ps = []
        sso = []
        tso = []
        ps = []
        ss = []
        phs = []
        e2s = []
        p2s = []

        for i in filestrings:
            ts.append(partrecDosePlotter(
                i+'total.csv', 100, 1.67).basicDosemap)
            tso.append(partrecDosePlotter(
                i+'total.csv', 100, 1.67).basicDosemap)
            sso.append(partrecDosePlotter(
                i+'secondary.csv', 100, 1.67).basicDosemap)
            ps.append(partrecDosePlotter(
                i+'primary.csv', 100, 1.67).basicDosemap)
            ss.append(partrecDosePlotter(
                i+'secondary.csv', 100, 1.67).basicDosemap)
            phs.append(partrecDosePlotter(
                i+'photon.csv', 100, 1.67).basicDosemap)
            e2s.append(partrecDosePlotter(i+'e2.csv', 100, 1.67).basicDosemap)
            p2s.append(partrecDosePlotter(i+'p2.csv', 100, 1.67).basicDosemap)

        plt.rcParams['figure.autolayout'] = True
        textsize = 20
        # plt.ioff()

        def setRadius(total):
            totalDose = np.sum(total)
            for i in range(len(total[:, 0, 0])):
                encapsulated = np.sum(total[(25-i):(25+i), (25-i):(25+i), :])
                if encapsulated > totalDose/2:
                    j = i-1
                    encapsulatedlower = np.sum(
                        total[(25-j):(25+j), (25-j):(25+j), :])
                    if np.abs(encapsulated-totalDose/2) < np.abs(encapsulatedlower-totalDose/2):
                        rad = i
                    else:
                        rad = j
                    break
            return rad

        rs = []
        for i in range(len(ts)):
            if ddBins == 'auto':
                r = setRadius(ts[i])
            else:
                r = ddBins

            ts[i] = np.flip(
                np.mean(ts[i][(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))
            ps[i] = np.flip(
                np.mean(ps[i][(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))
            ss[i] = np.flip(
                np.mean(ss[i][(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))
            phs[i] = np.flip(
                np.mean(phs[i][(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))

            e2s[i] = np.flip(
                np.mean(e2s[i][(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))

            p2s[i] = np.flip(
                np.mean(p2s[i][(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))
        fig, ax = plt.subplots(2, 3, figsize=(20, 16), sharex=True)
        # plt.contourf(xi*0.35, yi*0.405, di*scalinTTTg_factor, 100, cmap='jet' )
        depths = np.linspace(0, 300, 50)
        estrings = element_list
        es = [3, 6, 11, 12, 13, 14, 20, 22, 24, 26,
              27, 28, 29, 30, 47, 73, 74, 78, 79, 82]
        for i in range(len(ts)):

            ax[0][0].plot(depths, ts[i]/max(ts[4]),
                          label=estrings[i])
            ax[0][0].set_title('Total Dose')
            ax[0][1].plot(depths, ps[i]/max(ts[4]),
                          label=estrings[i])
            ax[0][1].set_title('Primary Dose')
            ax[0][2].plot(depths, ss[i]/max(ts[4]),
                          label=estrings[i])
            ax[0][2].set_title('Secondary Dose')
            ax[1][0].plot(depths, e2s[i]/max(ts[4]),
                          label=estrings[i])
            ax[1][0].set_title('Secondory e- Dose')
            ax[1][1].plot(depths, p2s[i]/max(ts[4]),
                          label=estrings[i])
            ax[1][1].set_title('Secondary e+ Dose')
            ax[1][2].plot(depths, phs[i]/max(ts[4]),
                          label=estrings[i])
            ax[1][2].set_title('Secondary Photon Dose')

        ax[0][0].legend()
        # cv2.imshow("Polar Image", polar_image)

        ax[1][0].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[1][1].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[1][2].set_xlabel("Depth [mm]", fontsize=textsize)

        ax[0][0].set_ylabel("Dose [arb.]", fontsize=textsize)
        ax[1][0].set_ylabel("Dose [arb.]", fontsize=textsize)
        for i in ax:
            for j in i:

                j.grid(True)
        fig, ax = plt.subplots(3, 1, figsize=(8, 8))
        full_ratios = []
        axis_ratios = []
        phdoses = []
        for i in range(len(ts)):
            full_ratios.append((np.sum(sso[i])/np.sum(tso[i]))*100)
            axis_ratios.append((np.sum(ss[i])/np.sum(ts[i]))*100)
            phdoses.append(np.sum)
        ax[0].plot(es, full_ratios, color='k')
        ax[0].set_title('Secondary dose percentage Across full phantom')
        ax[0].set_xlabel('Z')
        ax[0].set_ylabel('Total Dose [arb.] ')
        ax[0].grid(True)
        ax[1].set_title('Summed On-axis Secondary dose percentage')
        ax[1].plot(es, axis_ratios, color='k')
        ax[1].set_xlabel('Z')
        ax[1].set_ylabel('Secondary/Total Dose [%]')
        ax[2].set_title('Secondary dose percentage across entire phantom')
        for i in range(len(ts)):
            ax[2].plot(depths, (ss[i]/ts[i])*100,
                       label=estrings[i])
        ax[2].set_title('On-axis secondary dose percentage')
        ax[2].set_ylabel('On-axis Secondary/Total Dose Ratio [%]')
        ax[2].set_xlabel('Depth [mm]')
        ax[1].grid(True)
        ax[2].grid(True)
        ax[2].legend()

        fig, ax = plt.subplots(1, 2)
        peak_loc = []
        half_loc = []
        for i in range(len(ts)):

            ax[0].plot(depths, ts[i]/max(ts[i]),
                       label=estrings[i])
            peak_loc.append(depths[ts[i] == max(ts[i])])
            #half_loc.append(depths[ts[i] < max(ts[i])*0.7])
            ax[0].set_title('Total Normalised Dose')
        ax[1].scatter(es, peak_loc, marker='x',
                      label='On-axis peak dose depth', color='k')
        #ax[1].plot(es, half_loc, label='On-axis half-dose depth', color='r')
        ax[1].set_title(
            'Peak Dose Depths on-axis')
        ax[0].set_xlabel('Depth [mm]')
        ax[0].set_ylabel('Dose[arb.]')
        ax[0].legend()
        ax[1].set_xlabel('Z')
        ax[1].set_ylabel('Depth in water phantom [mm]')
        ax[0].grid(True)
        ax[1].grid(True)
