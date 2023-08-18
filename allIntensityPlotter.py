import pandas as pd
import matplotlib.pyplot as plt
from allIntensityReader import allIntensityReader
from matplotlib.ticker import FormatStrFormatter
import numpy as np


class allIntensityPlotter(allIntensityReader):

    def plotComparisons(self, xfov=50, pxfov=100):
        t = self.topasPhsp
        m = self.molPhsp
        p = self.pdgPhsp
        tx, ty = self.getSlices(t)
        mx, my = self.getSlices(m)
        px, py = self.getSlices(p)
        fig, ax = plt.subplots(3, 3, sharex=True, figsize=(8, 8))
        bins1d = 50
        bins2d = 50
        ax[0, 0].hist2d(t['X'], t['Y'], bins=bins2d, range=[
                        [-xfov, xfov], [-xfov, xfov]])
        ax[0, 0].set_title('TOPAS')
        ax[0, 1].set_title('Moliere')
        ax[0, 2].set_title('Gaussian')
        ax[0, 1].hist2d(m['X'], m['Y'], bins=bins2d, range=[
                        [-xfov, xfov], [-xfov, xfov]])
        ax[0, 2].hist2d(p['X'], p['Y'], bins=bins2d, range=[
                        [-xfov, xfov], [-xfov, xfov]])
        ax[0, 0].set_ylabel('Y [mm]')

        ax[1, 0].hist2d(t['X'], t['PX'], bins=bins2d, range=[
                        [-xfov, xfov], [-pxfov, pxfov]])
        ax[1, 1].hist2d(m['X'], m['PX'], bins=bins2d, range=[
                        [-xfov, xfov], [-pxfov, pxfov]])
        ax[1, 2].hist2d(p['X'], p['PX'], bins=bins2d, range=[
                        [-xfov, xfov], [-pxfov, pxfov]])
        ax[1, 0].set_ylabel('PX [mrad]')
        ax[2, 0].set_xlabel('X [mm]')
        ax[2, 1].set_xlabel('X [mm]')
        ax[2, 2].set_xlabel('X [mm]')
        ax[2, 0].hist(tx['X'], bins=bins1d, color='b',
                      range=[-xfov, xfov],)
        ax[2, 1].hist(mx['X'], bins=bins1d, color='b',
                      range=[-xfov, xfov],)
        ax[2, 2].hist(px['X'], bins=bins1d, color='b',
                      range=[-xfov, xfov],)

        ax[2, 0].set_ylabel('Arb. Intensity')

    def plotTOPASPDGProportions(self, fov=50, col=50):
        plt.rc("axes", labelsize=12)
        plt.rc("xtick", labelsize=8)
        plt.rc("ytick", labelsize=8)
        get_slices = self.getSlices
        t = self.topasPhsp
        m = self.molPhsp
        p = self.pdgPhsp
        sig = np.std(p['X'])
        div = len(t['R'])/100
        print(len(t['R']))
        Nt1 = len(t[(t["R"] < sig)]['X'])/div
        Nt2 = len(t[(t["R"] < 2*sig)]['X'])/div
        Nt3 = len(t[(t["R"] < 3*sig)]['X'])/div
        Nt4 = len(t[(t["R"] < 4*sig)]['X'])/div
        Nt5 = len(t[(t["R"] < 5*sig)]['X'])/div

        Nm1 = len(m[(m["R"] < sig)]['X'])/div
        Nm2 = len(m[(m["R"] < 2*sig)]['X'])/div
        Nm3 = len(m[(m["R"] < 3*sig)]['X'])/div
        Nm4 = len(m[(m["R"] < 4*sig)]['X'])/div
        Nm5 = len(m[(m["R"] < 5*sig)]['X'])/div

        tx, ty = get_slices(t, 3)
        mx, my = get_slices(m, 3)
        fig, ax = plt.subplots(1, 2, figsize=(15, 7))
        sig = 28.0
        ax[0].hist(tx["X"], bins=50,
                   range=[0, fov], color="b", density=True)
        ax[0].set_xlabel("R [mm]")
        ax[0].set_ylabel("Arb. Intensity")

        ax[0].plot([sig, sig], [0, 0.03], color='black', linewidth=3)
        ax[0].plot([2*sig, 2*sig], [0, 0.03], color='red', linewidth=3)
        ax[0].plot([3*sig, 3*sig], [0, 0.03], color='orange', linewidth=3)
        ax[0].plot([4*sig, 4*sig], [0, 0.03], color='pink', linewidth=3)
        ax[0].plot([5*sig, 5*sig], [0, 0.03], color='cyan', linewidth=3)
        ax[0].set_xlim([0, fov])
        ax[0].set_ylim([0, 0.034])
        ax[0].set_title('TOPAS')

        ax[1].hist(mx['X'], bins=50,
                   range=[0, fov], color="b", density=True)
        ax[1].plot([sig, sig], [0, 0.03], color='black', linewidth=3)
        ax[1].plot([2*sig, 2*sig], [0, 0.03], color='red', linewidth=3)
        ax[1].plot([3*sig, 3*sig], [0, 0.03], color='orange', linewidth=3)
        ax[1].plot([4*sig, 4*sig], [0, 0.03], color='pink', linewidth=3)
        ax[1].plot([5*sig, 5*sig], [0, 0.03], color='cyan', linewidth=3)
        ax[1].set_xlabel("R [mm]")
        ax[1].set_ylabel("Arb. Intensity")
        ax[1].set_xlim([0, fov])
        ax[1].set_ylim([0, 0.034])
        ax[1].set_title('Moliere')

        c = 7
        size = 25
        sizey = 0.031
        ax[0].text(14+c, sizey, ' $\sigma$', size=size)
        ax[0].text(42+c, sizey, '2$\sigma$', size=size)
        ax[0].text(70+c, sizey, '3$\sigma$', size=size)
        ax[0].text(98+c, sizey, '4$\sigma$', size=size)
        ax[0].text(126+c, sizey, '5$\sigma$', size=size)
        sizey2 = 0.002
        size2 = 15
        d = -5
        ax[0].text(14+d, sizey2, str(round((Nt1), 1)) +
                   '%', size=size2, color='white')
        ax[0].text(42+d, sizey2, str(round((Nt2-Nt1), 1)) +
                   '%', size=size2, color='white')
        ax[0].text(70+d, sizey2, str(round((Nt3-Nt2), 1))+'%', size=size2)
        ax[0].text(98+d, sizey2, str(round((Nt4-Nt3), 1))+'%', size=size2)
        ax[0].text(126+d, sizey2, str(round((Nt5-Nt4), 1))+'%', size=size2)

        c = 7
        size = 25
        sizey = 0.031
        ax[1].text(14+c, sizey, ' $\sigma$', size=size)
        ax[1].text(42+c, sizey, '2$\sigma$', size=size)
        ax[1].text(70+c, sizey, '3$\sigma$', size=size)
        ax[1].text(98+c, sizey, '4$\sigma$', size=size)
        ax[1].text(126+c, sizey, '5$\sigma$', size=size)

        sizey2 = 0.002
        size2 = 15
        d = -4
        ax[1].text(14+d, sizey2, str(round((Nm1), 1)) +
                   '%', size=size2, color='white')
        ax[1].text(42+d, sizey2, str(round((Nm2-Nm1), 1)) +
                   '%', size=size2, color='white')
        ax[1].text(70+d, sizey2, str(round((Nm3-Nm2), 1))+'%', size=size2)
        ax[1].text(98+d, sizey2, str(round((Nm4-Nm3), 1))+'%', size=size2)
        ax[1].text(126+d, sizey2, str(round((Nm5-Nm4), 1))+'%', size=size2)
