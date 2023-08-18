#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 13:23:10 2023

@author: robertsoncl
"""
from partrecDosePlotter import partrecDosePlotter
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import kurtosis


class s1DosePlotter:
    def plotGenericComposition(self, filestring, ddBins='auto'):
        total = partrecDosePlotter(
            filestring+'total.csv', 1000, 1.67).basicDosemap
        primary = partrecDosePlotter(
            filestring+'primary.csv', 1000, 1.67).basicDosemap
        secondary = partrecDosePlotter(
            filestring+'secondary.csv', 1000, 1.67).basicDosemap
        photon = partrecDosePlotter(
            filestring+'photon.csv', 1000, 1.67).basicDosemap

        e2 = partrecDosePlotter(filestring+'e2.csv', 1000, 1.67).basicDosemap

        p2 = partrecDosePlotter(filestring+'p2.csv', 1000, 1.67).basicDosemap

        plt.rcParams['figure.autolayout'] = True
        textsize = 10
        # plt.ioff()
        totalDose = np.sum(total)

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
        if ddBins == 'auto':
            r = setRadius(total)
        else:
            r = ddBins
        fig, ax = plt.subplots(2, 1, figsize=(8, 8))

        total = np.flip(
            np.mean(total[(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))
        primary = np.flip(
            np.mean(primary[(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))
        secondary = np.flip(
            np.mean(secondary[(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))
        photon = np.flip(
            np.mean(photon[(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))

        e2 = np.flip(
            np.mean(e2[(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))

        p2 = np.flip(
            np.mean(p2[(25-r):(25+r), (25-r):(25+r), :], axis=(0, 1)))

        # plt.contourf(xi*0.35, yi*0.405, di*scalinTTTg_factor, 100, cmap='jet' )
        depths = np.linspace(0, 300, 50)
        ax[0].plot(depths, (total)/max(total),
                   color='k', label='Total Dose')
        ax[0].plot(depths, primary/max(total), color='b', label='Primary Dose')
        ax[0].plot(depths, secondary/max(total),
                   color='red', label='Secondary Dose')
        ax[0].legend()
        # cv2.imshow("Polar Image", polar_image)
        ax[0].set_title('Normalised on-axis dose')
        ax[0].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[0].set_ylabel("Dose [arb.]", fontsize=textsize)
        ax[0].grid(True)

        ax[1].plot(depths, (photon+e2+p2)/max(total),
                   color='r', label='Secondary Dose')
        ax[1].plot(depths, photon/max(total), color='g', label='Photon Dose')
        ax[1].plot(depths, p2/max(total),
                   color='pink', label='Secondary Positron Dose')
        ax[1].plot(depths, e2/max(total),
                   color='cyan', label='Secondary Electron Dose')
        ax[1].legend()
        # cv2.imshow("Polar Image", polar_image)
        ax[1].set_title('Normalised on-axis dose')
        ax[1].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[1].set_ylabel("Dose [arb.]", fontsize=textsize)
        ax[1].grid(True)

    def plotEnergyScan(self, ddBins='auto'):
        folder = '/home/robertsoncl/dphil/s1Data/Doses/'
        filestring50 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(50.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring100 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(100.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring150 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring200 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(200.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring250 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(250.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        total50 = partrecDosePlotter(
            filestring50+'total.csv', 1000, 1.67).basicDosemap
        primary50 = partrecDosePlotter(
            filestring50+'primary.csv', 1000, 1.67).basicDosemap
        secondary50 = partrecDosePlotter(
            filestring50+'secondary.csv', 1000, 1.67).basicDosemap
        photon50 = partrecDosePlotter(
            filestring50+'photon.csv', 1000, 1.67).basicDosemap

        e250 = partrecDosePlotter(
            filestring50+'e2.csv', 1000, 1.67).basicDosemap

        p250 = partrecDosePlotter(
            filestring50+'p2.csv', 1000, 1.67).basicDosemap

        total100 = partrecDosePlotter(
            filestring100+'total.csv', 1000, 1.67).basicDosemap
        primary100 = partrecDosePlotter(
            filestring100+'primary.csv', 1000, 1.67).basicDosemap
        secondary100 = partrecDosePlotter(
            filestring100+'secondary.csv', 1000, 1.67).basicDosemap
        photon100 = partrecDosePlotter(
            filestring100+'photon.csv', 1000, 1.67).basicDosemap

        e2100 = partrecDosePlotter(
            filestring100+'e2.csv', 1000, 1.67).basicDosemap

        p2100 = partrecDosePlotter(
            filestring100+'p2.csv', 1000, 1.67).basicDosemap

        total150 = partrecDosePlotter(
            filestring150+'total.csv', 1000, 1.67).basicDosemap
        primary150 = partrecDosePlotter(
            filestring150+'primary.csv', 1000, 1.67).basicDosemap
        secondary150 = partrecDosePlotter(
            filestring150+'secondary.csv', 1000, 1.67).basicDosemap
        photon150 = partrecDosePlotter(
            filestring150+'photon.csv', 1000, 1.67).basicDosemap

        e2150 = partrecDosePlotter(
            filestring150+'e2.csv', 1000, 1.67).basicDosemap

        p2150 = partrecDosePlotter(
            filestring150+'p2.csv', 1000, 1.67).basicDosemap

        total200 = partrecDosePlotter(
            filestring200+'total.csv', 1000, 1.67).basicDosemap
        primary200 = partrecDosePlotter(
            filestring200+'primary.csv', 1000, 1.67).basicDosemap
        secondary200 = partrecDosePlotter(
            filestring200+'secondary.csv', 1000, 1.67).basicDosemap
        photon200 = partrecDosePlotter(
            filestring200+'photon.csv', 1000, 1.67).basicDosemap

        e2200 = partrecDosePlotter(
            filestring200+'e2.csv', 1000, 1.67).basicDosemap

        p2200 = partrecDosePlotter(
            filestring200+'p2.csv', 1000, 1.67).basicDosemap

        total250 = partrecDosePlotter(
            filestring250+'total.csv', 1000, 1.67).basicDosemap
        primary250 = partrecDosePlotter(
            filestring250+'primary.csv', 1000, 1.67).basicDosemap
        secondary250 = partrecDosePlotter(
            filestring250+'secondary.csv', 1000, 1.67).basicDosemap
        photon250 = partrecDosePlotter(
            filestring250+'photon.csv', 1000, 1.67).basicDosemap

        e2250 = partrecDosePlotter(
            filestring250+'e2.csv', 1000, 1.67).basicDosemap

        p2250 = partrecDosePlotter(
            filestring250+'p2.csv', 1000, 1.67).basicDosemap

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

        tso = [total50, total100, total150, total200, total250]
        pso = [primary50, primary100, primary150, primary200, primary250]
        sso = [secondary50, secondary100,
               secondary150, secondary200, secondary250]
        phso = [photon50, photon100, photon150, photon200, photon250]
        e2so = [e250, e2100, e2150, e2200, e2250]
        p2so = [p250, p2100, p2150, p2200, p2250]

        ts = [total50, total100, total150, total200, total250]
        ps = [primary50, primary100, primary150, primary200, primary250]
        ss = [secondary50, secondary100,
              secondary150, secondary200, secondary250]
        phs = [photon50, photon100, photon150, photon200, photon250]
        e2s = [e250, e2100, e2150, e2200, e2250]
        p2s = [p250, p2100, p2150, p2200, p2250]

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
        colours = ['blue', 'red', 'k', 'pink', 'cyan']
        estrings = ['50', '100', '150', '200', '250']
        es = [50, 100, 150, 200, 250]
        for i in range(len(ts)):

            ax[0][0].plot(depths, ts[i]/max(ts[4]),
                          color=colours[i], label=estrings[i]+' MeV')
            ax[0][0].set_title('Total Dose')
            ax[0][1].plot(depths, ps[i]/max(ts[4]),
                          color=colours[i], label=estrings[i]+' MeV')
            ax[0][1].set_title('Primary Dose')
            ax[0][2].plot(depths, ss[i]/max(ts[4]),
                          color=colours[i], label=estrings[i]+' MeV')
            ax[0][2].set_title('Secondary Dose')
            ax[1][0].plot(depths, e2s[i]/max(ts[4]),
                          color=colours[i], label=estrings[i]+' MeV')
            ax[1][0].set_title('Secondory e- Dose')
            ax[1][1].plot(depths, p2s[i]/max(ts[4]),
                          color=colours[i], label=estrings[i]+' MeV')
            ax[1][1].set_title('Secondary e+ Dose')
            ax[1][2].plot(depths, phs[i]/max(ts[4]),
                          color=colours[i], label=estrings[i]+' MeV')
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
        ax[0].set_xlabel('Energy [MeV]')
        ax[0].set_ylabel('Total Dose [arb.] ')
        ax[0].grid(True)
        ax[1].set_title('Summed On-axis Secondary dose percentage')
        ax[1].plot(es, axis_ratios, color='k')
        ax[1].set_xlabel('Energy [MeV]')
        ax[1].set_ylabel('Secondary/Total Dose [%]')
        ax[1].set_title('Secondary dose percentage across entire phantom')
        for i in range(len(ts)):
            ax[2].plot(depths, (ss[i]/ts[i])*100,
                       color=colours[i], label=estrings[i]+' MeV')
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
                       color=colours[i], label=estrings[i]+'MeV')
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
        ax[1].set_xlabel('Initial Beam Energy [MeV]')
        ax[1].set_ylabel('Depth in water phantom [mm]')
        ax[0].grid(True)
        ax[1].grid(True)

        # plt.ioff()

    def plotThicknessScan(self, ddBins='auto'):
        folder = '/home/robertsoncl/dphil/s1Data/Doses/'
        filestring1 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(1, 1)) + \
            'Aluminum'+str(1000)
        filestring5 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(5, 1)) + \
            'Aluminum'+str(1000)
        filestring10 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring15 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(15, 1)) + \
            'Aluminum'+str(1000)
        filestring20 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(20, 1)) + \
            'Aluminum'+str(1000)
        filestring25 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(25, 1)) + \
            'Aluminum'+str(1000)
        total1 = partrecDosePlotter(
            filestring1+'total.csv', 1000, 1.67).basicDosemap
        primary1 = partrecDosePlotter(
            filestring1+'primary.csv', 1000, 1.67).basicDosemap
        secondary1 = partrecDosePlotter(
            filestring1+'secondary.csv', 1000, 1.67).basicDosemap
        photon1 = partrecDosePlotter(
            filestring1+'photon.csv', 1000, 1.67).basicDosemap
        e21 = partrecDosePlotter(
            filestring1+'e2.csv', 1000, 1.67).basicDosemap
        p21 = partrecDosePlotter(
            filestring1+'p2.csv', 1000, 1.67).basicDosemap

        total5 = partrecDosePlotter(
            filestring5+'total.csv', 1000, 1.67).basicDosemap
        primary5 = partrecDosePlotter(
            filestring5+'primary.csv', 1000, 1.67).basicDosemap
        secondary5 = partrecDosePlotter(
            filestring5+'secondary.csv', 1000, 1.67).basicDosemap
        photon5 = partrecDosePlotter(
            filestring5+'photon.csv', 1000, 1.67).basicDosemap
        e25 = partrecDosePlotter(
            filestring5+'e2.csv', 1000, 1.67).basicDosemap
        p25 = partrecDosePlotter(
            filestring5+'p2.csv', 1000, 1.67).basicDosemap

        total10 = partrecDosePlotter(
            filestring10+'total.csv', 1000, 1.67).basicDosemap
        primary10 = partrecDosePlotter(
            filestring10+'primary.csv', 1000, 1.67).basicDosemap
        secondary10 = partrecDosePlotter(
            filestring10+'secondary.csv', 1000, 1.67).basicDosemap
        photon10 = partrecDosePlotter(
            filestring10+'photon.csv', 1000, 1.67).basicDosemap
        e210 = partrecDosePlotter(
            filestring10+'e2.csv', 1000, 1.67).basicDosemap
        p210 = partrecDosePlotter(
            filestring10+'p2.csv', 1000, 1.67).basicDosemap

        total15 = partrecDosePlotter(
            filestring15+'total.csv', 1000, 1.67).basicDosemap
        primary15 = partrecDosePlotter(
            filestring15+'primary.csv', 1000, 1.67).basicDosemap
        secondary15 = partrecDosePlotter(
            filestring15+'secondary.csv', 1000, 1.67).basicDosemap
        photon15 = partrecDosePlotter(
            filestring15+'photon.csv', 1000, 1.67).basicDosemap
        e215 = partrecDosePlotter(
            filestring15+'e2.csv', 1000, 1.67).basicDosemap
        p215 = partrecDosePlotter(
            filestring15+'p2.csv', 1000, 1.67).basicDosemap

        total20 = partrecDosePlotter(
            filestring20+'total.csv', 1000, 1.67).basicDosemap
        primary20 = partrecDosePlotter(
            filestring20+'primary.csv', 1000, 1.67).basicDosemap
        secondary20 = partrecDosePlotter(
            filestring20+'secondary.csv', 1000, 1.67).basicDosemap
        photon20 = partrecDosePlotter(
            filestring20+'photon.csv', 1000, 1.67).basicDosemap
        e220 = partrecDosePlotter(
            filestring20+'e2.csv', 1000, 1.67).basicDosemap
        p220 = partrecDosePlotter(
            filestring20+'p2.csv', 1000, 1.67).basicDosemap

        total25 = partrecDosePlotter(
            filestring25+'total.csv', 1000, 1.67).basicDosemap
        primary25 = partrecDosePlotter(
            filestring25+'primary.csv', 1000, 1.67).basicDosemap
        secondary25 = partrecDosePlotter(
            filestring25+'secondary.csv', 1000, 1.67).basicDosemap
        photon25 = partrecDosePlotter(
            filestring25+'photon.csv', 1000, 1.67).basicDosemap
        e225 = partrecDosePlotter(
            filestring25+'e2.csv', 1000, 1.67).basicDosemap
        p225 = partrecDosePlotter(
            filestring25+'p2.csv', 1000, 1.67).basicDosemap

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

        tso = [total1, total5, total10, total15, total20, total25]
        pso = [primary1, primary5, primary10, primary15, primary20, primary25]
        sso = [secondary1, secondary5, secondary10,
               secondary15, secondary20, secondary25]

        ts = [total1, total5, total10, total15, total20, total25]
        ps = [primary1, primary5, primary10, primary15, primary20, primary25]
        ss = [secondary1, secondary5, secondary10,
              secondary15, secondary20, secondary25]

        phs = [photon1, photon5, photon10, photon15, photon20, photon25]
        e2s = [e21, e25, e210, e215, e220, e225]
        p2s = [p21, p25, p210, p215, p220, p225]

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
        colours = ['blue', 'red', 'k', 'pink', 'cyan', 'orange']
        estrings = ['1', '5', '10', '15', '20', '25']
        es = [1, 5, 10, 15, 20, 25]
        for i in range(len(ts)):

            ax[0][0].plot(depths, ts[i]/max(ts[0]),
                          color=colours[i], label=estrings[i]+' mm')
            ax[0][0].set_title('Total Dose')
            ax[0][1].plot(depths, ps[i]/max(ts[0]),
                          color=colours[i], label=estrings[i]+' mm')
            ax[0][1].set_title('Primary Dose')
            ax[0][2].plot(depths, ss[i]/max(ts[0]),
                          color=colours[i], label=estrings[i]+' mm')
            ax[0][2].set_title('Secondary Dose')
            ax[1][0].plot(depths, e2s[i]/max(ts[0]),
                          color=colours[i], label=estrings[i]+' mm')
            ax[1][0].set_title('Secondory e- Dose')
            ax[1][1].plot(depths, p2s[i]/max(ts[0]),
                          color=colours[i], label=estrings[i]+' mm')
            ax[1][1].set_title('Secondary e+ Dose')
            ax[1][2].plot(depths, phs[i]/max(ts[0]),
                          color=colours[i], label=estrings[i]+' mm')
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
        ax[0].set_xlabel('Thckness [mm]')
        ax[0].set_ylabel('Total Dose [arb.] ')
        ax[0].grid(True)
        ax[1].set_title('Summed On-axis Secondary dose percentage')
        ax[1].plot(es, axis_ratios, color='k')
        ax[1].set_xlabel('Thickness [mm]')
        ax[1].set_ylabel('Secondary/Total Dose [%]')
        ax[1].set_title('On-axis secondary dose percentage')
        for i in range(len(ts)):
            ax[2].plot(depths, (ss[i]/ts[i])*100,
                       color=colours[i], label=estrings[i]+' mm')
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
                       color=colours[i], label=estrings[i]+' mm')
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
        ax[1].set_xlabel('Thickness [mm]')
        ax[1].set_ylabel('Depth in water phantom [mm]')
        # ax[1].legend()

        # plt.ioff()

    def plotTransverseEvolution(self, filestring):
        def getSliceStats(dosemap, zBin):
            x_slice = dosemap[:, 25, 50-(zBin+1)]
            y_slice = dosemap[25, :, 50-(zBin+1)]

            x_range = np.linspace(0, 300, len(x_slice))
            y_range = np.linspace(0, 300, len(y_slice))
            x_slice = x_slice*1000000000000
            x_slice = np.rint(x_slice)
            x_slice = x_slice.astype(int)

            y_slice = y_slice*1000000000000
            y_slice = np.rint(y_slice)
            y_slice = y_slice.astype(int)
            xdata = np.repeat(x_range, x_slice)
            ydata = np.repeat(y_range, y_slice)
            # meanx = np.nanquantile(
            #    xdata, 0.50, method='interpolated_inverted_cdf')
            # sigmax = meanx-np.nanquantile(xdata, 0.159,
            #                             method='interpolated_inverted_cdf')
            sigmax = np.std(xdata)
            kurtx = kurtosis(xdata)
            # meany = np.nanquantile(
            #    ydata, 0.50, method='interpolated_inverted_cdf')
            # sigmay = meany-np.nanquantile(ydata, 0.159,
            #                              method='interpolated_inverted_cdf')
            sigmay = np.std(ydata)
            kurty = kurtosis(ydata)
            return sigmax, sigmay, kurtx, kurty

        total = partrecDosePlotter(
            filestring+'total.csv', 1000, 1.67).basicDosemap
        primary = partrecDosePlotter(
            filestring+'primary.csv', 1000, 1.67).basicDosemap
        secondary = partrecDosePlotter(
            filestring+'secondary.csv', 1000, 1.67).basicDosemap
        photon = partrecDosePlotter(
            filestring+'photon.csv', 1000, 1.67).basicDosemap

        e2 = partrecDosePlotter(filestring+'e2.csv', 1000, 1.67).basicDosemap

        p2 = partrecDosePlotter(filestring+'p2.csv', 1000, 1.67).basicDosemap
        depths = np.linspace(0, 300, 50)
        tsigmax = []
        tsigmay = []

        psigmax = []
        psigmay = []

        ssigmax = []
        ssigmay = []

        phsigmax = []
        phsigmay = []

        e2sigmax = []
        e2sigmay = []

        p2sigmax = []
        p2sigmay = []

        tkurtx = []
        tkurty = []

        pkurtx = []
        pkurty = []

        skurtx = []
        skurty = []

        phkurtx = []
        phkurty = []

        e2kurtx = []
        e2kurty = []

        p2kurtx = []
        p2kurty = []

        for i in range(50):
            x, y, kx, ky = getSliceStats(total, i)
            tsigmax.append(x)
            tsigmay.append(y)
            tkurtx.append(kx)
            tkurty.append(ky)

            x, y, kx, ky = getSliceStats(primary, i)
            psigmax.append(x)
            psigmay.append(y)
            pkurtx.append(kx)
            pkurty.append(ky)

            x, y, kx, ky = getSliceStats(secondary, i)
            ssigmax.append(x)
            ssigmay.append(y)
            skurtx.append(kx)
            skurty.append(ky)

        textsize = 10
        fig, ax = plt.subplots(2, 1, figsize=(8, 8))
        ax[0].errorbar(depths, tsigmax, yerr=tkurtx,
                       color='k', label='Total Dose $\sigma_x$', capsize=2)
        ax[0].errorbar(depths, tsigmay, yerr=tkurty, color='r',
                       label='Total Dose $\sigma_y$', capsize=2)
        ax[0].legend()
        # cv2.imshow("Polar Image", polar_image)
        ax[0].set_title('Transverse Dose Profile Evolution')
        ax[0].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[0].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[0].grid(True)
        ax[1].errorbar(depths, psigmax, yerr=pkurtx,
                       color='k', label='Primary Dose $\sigma_x$', capsize=2)
        ax[1].errorbar(depths, psigmay, yerr=pkurty, color='r',
                       label='Primary Dose $\sigma_y$', capsize=2)
        ax[1].errorbar(depths, ssigmax, yerr=skurtx,
                       color='b', label='Secondary Dose $\sigma_x$', capsize=2)
        ax[1].errorbar(depths, ssigmay, yerr=skurty, color='orange',
                       label='Secondary Dose $\sigma_y$', capsize=2)
        ax[1].legend()
        # cv2.imshow("Polar Image", polar_image)
        # ax[1].set_title()
        ax[1].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[1].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[1].grid(True)
        # cv2.imshow("Polar Image", polar_image)

    def plotTransverseEnergyEvolution(self):
        def getSliceStats(dosemap, zBin):
            x_slice = dosemap[:, 25, 50-(zBin+1)]
            y_slice = dosemap[25, :, 50-(zBin+1)]

            x_range = np.linspace(0, 300, len(x_slice))
            y_range = np.linspace(0, 300, len(y_slice))
            x_slice = x_slice*1000000000000
            x_slice = np.rint(x_slice)
            x_slice = x_slice.astype(int)

            y_slice = y_slice*1000000000000
            y_slice = np.rint(y_slice)
            y_slice = y_slice.astype(int)
            xdata = np.repeat(x_range, x_slice)
            ydata = np.repeat(y_range, y_slice)
            # meanx = np.nanquantile(
            #    xdata, 0.50, method='interpolated_inverted_cdf')
            # sigmax = meanx-np.nanquantile(xdata, 0.159,
            #                             method='interpolated_inverted_cdf')
            sigmax = np.std(xdata)
            kurtx = kurtosis(xdata)
            # meany = np.nanquantile(
            #    ydata, 0.50, method='interpolated_inverted_cdf')
            # sigmay = meany-np.nanquantile(ydata, 0.159,
            #                              method='interpolated_inverted_cdf')
            sigmay = np.std(ydata)
            kurty = kurtosis(ydata)
            return sigmax, sigmay, kurtx, kurty

        folder = '/home/robertsoncl/dphil/s1Data/Doses/'
        filestring50 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(50.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring100 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(100.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring150 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring200 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(200.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring250 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(250.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        total50 = partrecDosePlotter(
            filestring50+'total.csv', 1000, 1.67).basicDosemap
        primary50 = partrecDosePlotter(
            filestring50+'primary.csv', 1000, 1.67).basicDosemap
        secondary50 = partrecDosePlotter(
            filestring50+'secondary.csv', 1000, 1.67).basicDosemap
        photon50 = partrecDosePlotter(
            filestring50+'photon.csv', 1000, 1.67).basicDosemap

        e250 = partrecDosePlotter(
            filestring50+'e2.csv', 1000, 1.67).basicDosemap

        p250 = partrecDosePlotter(
            filestring50+'p2.csv', 1000, 1.67).basicDosemap

        total100 = partrecDosePlotter(
            filestring100+'total.csv', 1000, 1.67).basicDosemap
        primary100 = partrecDosePlotter(
            filestring100+'primary.csv', 1000, 1.67).basicDosemap
        secondary100 = partrecDosePlotter(
            filestring100+'secondary.csv', 1000, 1.67).basicDosemap
        photon100 = partrecDosePlotter(
            filestring100+'photon.csv', 1000, 1.67).basicDosemap

        e2100 = partrecDosePlotter(
            filestring100+'e2.csv', 1000, 1.67).basicDosemap

        p2100 = partrecDosePlotter(
            filestring100+'p2.csv', 1000, 1.67).basicDosemap

        total150 = partrecDosePlotter(
            filestring150+'total.csv', 1000, 1.67).basicDosemap
        primary150 = partrecDosePlotter(
            filestring150+'primary.csv', 1000, 1.67).basicDosemap
        secondary150 = partrecDosePlotter(
            filestring150+'secondary.csv', 1000, 1.67).basicDosemap
        photon150 = partrecDosePlotter(
            filestring150+'photon.csv', 1000, 1.67).basicDosemap

        e2150 = partrecDosePlotter(
            filestring150+'e2.csv', 1000, 1.67).basicDosemap

        p2150 = partrecDosePlotter(
            filestring150+'p2.csv', 1000, 1.67).basicDosemap

        total200 = partrecDosePlotter(
            filestring200+'total.csv', 1000, 1.67).basicDosemap
        primary200 = partrecDosePlotter(
            filestring200+'primary.csv', 1000, 1.67).basicDosemap
        secondary200 = partrecDosePlotter(
            filestring200+'secondary.csv', 1000, 1.67).basicDosemap
        photon200 = partrecDosePlotter(
            filestring200+'photon.csv', 1000, 1.67).basicDosemap

        e2200 = partrecDosePlotter(
            filestring200+'e2.csv', 1000, 1.67).basicDosemap

        p2200 = partrecDosePlotter(
            filestring200+'p2.csv', 1000, 1.67).basicDosemap

        total250 = partrecDosePlotter(
            filestring250+'total.csv', 1000, 1.67).basicDosemap
        primary250 = partrecDosePlotter(
            filestring250+'primary.csv', 1000, 1.67).basicDosemap
        secondary250 = partrecDosePlotter(
            filestring250+'secondary.csv', 1000, 1.67).basicDosemap
        photon250 = partrecDosePlotter(
            filestring250+'photon.csv', 1000, 1.67).basicDosemap

        e2250 = partrecDosePlotter(
            filestring250+'e2.csv', 1000, 1.67).basicDosemap

        p2250 = partrecDosePlotter(
            filestring250+'p2.csv', 1000, 1.67).basicDosemap

        ts = [total50, total100, total150, total200, total250]
        ps = [primary50, primary100, primary150, primary200, primary250]
        ss = [secondary50, secondary100,
              secondary150, secondary200, secondary250]
        depths = np.linspace(0, 300, 50)
        estring = ['50', '100', '150', '200', '250']
        cstring = ['b', 'r', 'k', 'pink', 'cyan']
        textsize = 10
        fig, ax = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
        for j in range(len(ts)):

            tsigmax = []
            tsigmay = []

            psigmax = []
            psigmay = []

            ssigmax = []
            ssigmay = []

            tkurtx = []
            tkurty = []

            pkurtx = []
            pkurty = []

            skurtx = []
            skurty = []

            for i in range(50):
                x, y, kx, ky = getSliceStats(ts[j], i)
                tsigmax.append(x)
                tsigmay.append(y)
                tkurtx.append(kx)
                tkurty.append(ky)

                x, y, kx, ky = getSliceStats(ps[j], i)
                psigmax.append(x)
                psigmay.append(y)
                pkurtx.append(kx)
                pkurty.append(ky)

                x, y, kx, ky = getSliceStats(ss[j], i)
                ssigmax.append(x)
                ssigmay.append(y)
                skurtx.append(kx)
                skurty.append(ky)

            ax[0].errorbar(depths, tsigmax, yerr=tkurtx,
                           color=cstring[j], label=estring[j]+' MeV', capsize=2)

            ax[1].errorbar(depths, psigmax, yerr=pkurtx,
                           color=cstring[j], label=estring[j]+' MeV', capsize=2)

            ax[2].errorbar(depths, ssigmax, yerr=skurtx,
                           color=cstring[j], label=estring[j]+' MeV', capsize=2)
        ax[0].legend()
        # cv2.imshow("Polar Image", polar_image)
        ax[0].set_title('Transverse Total Dose Profile Evolution')
        ax[1].set_title('Transverse Primary Dose Profile Evolution')
        ax[2].set_title('Transverse Secondary Dose Profile Evolution')
        ax[0].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[0].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[0].grid(True)
        # ax[1].legend()
        # cv2.imshow("Polar Image", polar_image)
        # ax[1].set_title()
        ax[1].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[1].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[1].grid(True)

        ax[2].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[2].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[2].grid(True)

    def plotTransverseThicknessEvolution(self):
        def getSliceStats(dosemap, zBin):
            x_slice = dosemap[:, 25, 50-(zBin+1)]
            y_slice = dosemap[25, :, 50-(zBin+1)]

            x_range = np.linspace(0, 300, len(x_slice))
            y_range = np.linspace(0, 300, len(y_slice))
            x_slice = x_slice*1000000000000
            x_slice = np.rint(x_slice)
            x_slice = x_slice.astype(int)

            y_slice = y_slice*1000000000000
            y_slice = np.rint(y_slice)
            y_slice = y_slice.astype(int)
            xdata = np.repeat(x_range, x_slice)
            ydata = np.repeat(y_range, y_slice)
            # meanx = np.nanquantile(
            #    xdata, 0.50, method='interpolated_inverted_cdf')
            # sigmax = meanx-np.nanquantile(xdata, 0.159,
            #                             method='interpolated_inverted_cdf')
            sigmax = np.std(xdata)
            kurtx = kurtosis(xdata)
            # meany = np.nanquantile(
            #    ydata, 0.50, method='interpolated_inverted_cdf')
            # sigmay = meany-np.nanquantile(ydata, 0.159,
            #                              method='interpolated_inverted_cdf')
            sigmay = np.std(ydata)
            kurty = kurtosis(ydata)
            return sigmax, sigmay, kurtx, kurty

        folder = '/home/robertsoncl/dphil/s1Data/Doses/'
        filestring1 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(1, 1)) + \
            'Aluminum'+str(1000)
        filestring5 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(5, 1)) + \
            'Aluminum'+str(1000)
        filestring10 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        filestring15 = folder + 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(15, 1)) + \
            'Aluminum'+str(1000)
        filestring20 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(20, 1)) + \
            'Aluminum'+str(1000)
        filestring25 = folder+'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(25, 1)) + \
            'Aluminum'+str(1000)
        total1 = partrecDosePlotter(
            filestring1+'total.csv', 1000, 1.67).basicDosemap
        primary1 = partrecDosePlotter(
            filestring1+'primary.csv', 1000, 1.67).basicDosemap
        secondary1 = partrecDosePlotter(
            filestring1+'secondary.csv', 1000, 1.67).basicDosemap
        photon1 = partrecDosePlotter(
            filestring1+'photon.csv', 1000, 1.67).basicDosemap
        e21 = partrecDosePlotter(
            filestring1+'e2.csv', 1000, 1.67).basicDosemap
        p21 = partrecDosePlotter(
            filestring1+'p2.csv', 1000, 1.67).basicDosemap

        total5 = partrecDosePlotter(
            filestring5+'total.csv', 1000, 1.67).basicDosemap
        primary5 = partrecDosePlotter(
            filestring5+'primary.csv', 1000, 1.67).basicDosemap
        secondary5 = partrecDosePlotter(
            filestring5+'secondary.csv', 1000, 1.67).basicDosemap
        photon5 = partrecDosePlotter(
            filestring5+'photon.csv', 1000, 1.67).basicDosemap
        e25 = partrecDosePlotter(
            filestring5+'e2.csv', 1000, 1.67).basicDosemap
        p25 = partrecDosePlotter(
            filestring5+'p2.csv', 1000, 1.67).basicDosemap

        total10 = partrecDosePlotter(
            filestring10+'total.csv', 1000, 1.67).basicDosemap
        primary10 = partrecDosePlotter(
            filestring10+'primary.csv', 1000, 1.67).basicDosemap
        secondary10 = partrecDosePlotter(
            filestring10+'secondary.csv', 1000, 1.67).basicDosemap
        photon10 = partrecDosePlotter(
            filestring10+'photon.csv', 1000, 1.67).basicDosemap
        e210 = partrecDosePlotter(
            filestring10+'e2.csv', 1000, 1.67).basicDosemap
        p210 = partrecDosePlotter(
            filestring10+'p2.csv', 1000, 1.67).basicDosemap

        total15 = partrecDosePlotter(
            filestring15+'total.csv', 1000, 1.67).basicDosemap
        primary15 = partrecDosePlotter(
            filestring15+'primary.csv', 1000, 1.67).basicDosemap
        secondary15 = partrecDosePlotter(
            filestring15+'secondary.csv', 1000, 1.67).basicDosemap
        photon15 = partrecDosePlotter(
            filestring15+'photon.csv', 1000, 1.67).basicDosemap
        e215 = partrecDosePlotter(
            filestring15+'e2.csv', 1000, 1.67).basicDosemap
        p215 = partrecDosePlotter(
            filestring15+'p2.csv', 1000, 1.67).basicDosemap

        total20 = partrecDosePlotter(
            filestring20+'total.csv', 1000, 1.67).basicDosemap
        primary20 = partrecDosePlotter(
            filestring20+'primary.csv', 1000, 1.67).basicDosemap
        secondary20 = partrecDosePlotter(
            filestring20+'secondary.csv', 1000, 1.67).basicDosemap
        photon20 = partrecDosePlotter(
            filestring20+'photon.csv', 1000, 1.67).basicDosemap
        e220 = partrecDosePlotter(
            filestring20+'e2.csv', 1000, 1.67).basicDosemap
        p220 = partrecDosePlotter(
            filestring20+'p2.csv', 1000, 1.67).basicDosemap

        total25 = partrecDosePlotter(
            filestring25+'total.csv', 1000, 1.67).basicDosemap
        primary25 = partrecDosePlotter(
            filestring25+'primary.csv', 1000, 1.67).basicDosemap
        secondary25 = partrecDosePlotter(
            filestring25+'secondary.csv', 1000, 1.67).basicDosemap
        photon25 = partrecDosePlotter(
            filestring25+'photon.csv', 1000, 1.67).basicDosemap
        e225 = partrecDosePlotter(
            filestring25+'e2.csv', 1000, 1.67).basicDosemap
        p225 = partrecDosePlotter(
            filestring25+'p2.csv', 1000, 1.67).basicDosemap

        plt.rcParams['figure.autolayout'] = True
        textsize = 20

        ts = [total1, total5, total10, total15, total20, total25]
        ps = [primary1, primary5, primary10, primary15, primary20, primary25]
        ss = [secondary1, secondary5, secondary10,
              secondary15, secondary20, secondary25]

        phs = [photon1, photon5, photon10, photon15, photon20, photon25]
        e2s = [e21, e25, e210, e215, e220, e225]
        p2s = [p21, p25, p210, p215, p220, p225]
        depths = np.linspace(0, 300, 50)
        estring = ['1', '5', '10', '15', '20', '25']
        cstring = ['b', 'r', 'k', 'pink', 'cyan', 'orange']
        textsize = 10
        fig, ax = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
        for j in range(len(ts)):

            tsigmax = []
            tsigmay = []

            psigmax = []
            psigmay = []

            ssigmax = []
            ssigmay = []

            tkurtx = []
            tkurty = []

            pkurtx = []
            pkurty = []

            skurtx = []
            skurty = []

            for i in range(50):
                x, y, kx, ky = getSliceStats(ts[j], i)
                tsigmax.append(x)
                tsigmay.append(y)
                tkurtx.append(kx)
                tkurty.append(ky)

                x, y, kx, ky = getSliceStats(ps[j], i)
                psigmax.append(x)
                psigmay.append(y)
                pkurtx.append(kx)
                pkurty.append(ky)

                x, y, kx, ky = getSliceStats(ss[j], i)
                ssigmax.append(x)
                ssigmay.append(y)
                skurtx.append(kx)
                skurty.append(ky)

            ax[0].errorbar(depths, tsigmax, yerr=tkurtx,
                           color=cstring[j], label=estring[j]+' mm', capsize=2)

            ax[1].errorbar(depths, psigmax, yerr=pkurtx,
                           color=cstring[j], label=estring[j]+' mm', capsize=2)

            ax[2].errorbar(depths, ssigmax, yerr=skurtx,
                           color=cstring[j], label=estring[j]+' mm', capsize=2)
        ax[0].legend()
        # cv2.imshow("Polar Image", polar_image)
        ax[0].set_title('Transverse Total Dose Profile Evolution')
        ax[1].set_title('Transverse Primary Dose Profile Evolution')
        ax[2].set_title('Transverse Secondary Dose Profile Evolution')
        ax[0].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[0].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[0].grid(True)
        # ax[1].legend()
        # cv2.imshow("Polar Image", polar_image)
        # ax[1].set_title()
        ax[1].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[1].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[1].grid(True)

        ax[2].set_xlabel("Depth [mm]", fontsize=textsize)
        ax[2].set_ylabel("$\sigma$ [mm]", fontsize=textsize)
        ax[2].grid(True)
