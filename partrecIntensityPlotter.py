#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:42:24 2023

@author: robertsoncl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class partrecIntensityPlotter:
    # import phase space from defined file
    def __init__(self, path_to_phsp_file, particles='e'):
        def getSlices(phsp, slice_width=1):
            phsp_xslice = phsp[(phsp["Y"] < slice_width)]
            phsp_xslice = phsp_xslice[(phsp_xslice["Y"] > -slice_width)]
            phsp_yslice = phsp[(phsp["X"] < slice_width)]
            phsp_yslice = phsp_yslice[(phsp_yslice["X"] > -slice_width)]
            return phsp_xslice, phsp_yslice
        self.getSlices = getSlices

        # read Topas ASCII output file
        phase_space = pd.read_csv(
            path_to_phsp_file,
            names=["X", "Y", "Z", "PX", "PY", "E", "Weight", "PDG", "9", "10"],
            delim_whitespace=True,
        )
        phase_space["X"] = phase_space["X"] * 10
        phase_space["Y"] = phase_space["Y"] * 10
        phase_space['PX'] = phase_space['PX'] * 1000
        phase_space['PY'] = phase_space['PY'] * 1000
        # add "R" column for radial distance from origin in mm
        phase_space["R"] = np.sqrt(
            np.square(phase_space["X"]) + np.square(phase_space["Y"])
        )

        gamma_phase_space = phase_space.copy()
        positron_phase_space = phase_space.copy()
        # create DataFrame containing only electron data at patient
        electron_phase_space = phase_space.drop(
            phase_space[phase_space["PDG"] != 11].index
        )
        # create DataFrame containing only gamma data at patient
        gamma_phase_space = gamma_phase_space.drop(
            phase_space[phase_space["PDG"] != 22].index
        )

        # create DataFrame containing only gamma data at patient
        positron_phase_space = positron_phase_space.drop(
            phase_space[phase_space["PDG"] != -11].index
        )
        phsp_dict = {
            "all": phase_space,
            "e": electron_phase_space,
            "y": gamma_phase_space,
            "p": positron_phase_space
        }
        try:
            phsp = phsp_dict[particles]
        except KeyError:
            print('Particle type not found, should be one of all, e, or y')
        self.phsp = phsp
    # show transverse beam profile and energy spectrum
    # fov is field of view of profile graphs
    # col is the virtual collimator radius for calculation of transmission
    # both in millimetres
    # mean energy is calculated within collimator radius only

    def show_transverse_beam(self, fov=50, col=50):
        plt.rc("axes", labelsize=10)
        plt.rc("xtick", labelsize=8)
        plt.rc("ytick", labelsize=8)
        get_slices = self.getSlices
        phsp = self.phsp
        phsp_xslice, phsp_yslice = get_slices(phsp)
        fig, ax = plt.subplots(2, 2, figsize=(10, 10))
        ax[0, 0].hist(phsp_xslice["X"], bins=50, range=[-fov, fov], color="b")
        ax[0, 0].set_xlabel("X [mm]")
        ax[0, 0].set_ylabel("N")
        ax[0, 0].set_title("X Distribution")
        ax[0, 1].hist(phsp_yslice["Y"], bins=50, range=[-fov, fov], color="b")
        ax[0, 1].set_xlabel("Y [mm]")
        ax[0, 1].set_ylabel("N")
        ax[0, 1].set_title("Y Distribution")
        ax[1, 0].hist2d(
            phsp["X"], phsp["Y"], bins=100, range=[[-fov, fov], [-fov, fov]], cmap="jet"
        )
        ax[1, 0].set_xlabel("X [mm]")
        ax[1, 0].set_ylabel("Y [mm]")
        ax[1, 0].set_title("XY Distribution")
        ax[1, 1].hist(phsp["E"], bins=100, color="k")
        ax[1, 1].set_xlabel("E [MeV]")
        ax[1, 1].set_ylabel("N")
        ax[1, 1].set_yscale('log')

        ax[1, 1].set_title("Energy Spectrum")

        col_phsp = phsp[(phsp.R < col)]
        col_phsp = col_phsp.dropna()
        print(
            "Electron Transmission within Virtual Collimator = " +
            str(len(col_phsp["X"]) / len(phsp["X"]) * 100)
        )
        print("Mean Energy at Dump:" + str(np.mean(col_phsp["E"])))

    def showPHSP(self, fov=50, col=50):
        plt.rc("axes", labelsize=12)
        plt.rc("xtick", labelsize=8)
        plt.rc("ytick", labelsize=8)
        get_slices = self.getSlices
        phsp = self.phsp
        phsp_xslice, phsp_yslice = get_slices(phsp)
        fig, ax = plt.subplots(2, 3, figsize=(20, 8))
        ax[0, 0].hist2d(
            phsp["X"], phsp["Y"], bins=100, range=[[-fov, fov], [-fov, fov]],
        )
        ax[0, 0].set_xlabel("X [mm]")
        ax[0, 0].set_ylabel("Y [mm]")

        ax[1, 0].hist2d(
            phsp["PX"], phsp["PY"], bins=100, range=[[-1, 1], [-1, 1]],
        )

        ax[0, 1].hist2d(
            phsp["X"], phsp["PX"], bins=100, range=[[-fov, fov], [-fov, fov]],)
        ax[1, 0].set_xlabel("PX [mm]")
        ax[1, 0].set_ylabel("PY [mm]")
        ax[0, 1].set_xlabel("X [mm]")
        ax[0, 1].set_ylabel("PX [mrad]")
        ax[1, 1].hist2d(
            phsp["Y"], phsp["PY"], bins=100, range=[[-fov, fov], [-fov, fov]],)
        ax[1, 1].set_xlabel("Y [mm]")
        ax[1, 1].set_ylabel("PY [mrad]")

        ax[0, 2].hist(phsp_xslice["X"], bins=50,
                      range=[-fov, fov], color="b", density=True)
        ax[0, 2].set_xlabel("X [mm]")
        ax[0, 2].set_ylabel("Arb. Intensity")

        ax[1, 2].hist(phsp_yslice["Y"], bins=50,
                      range=[-fov, fov], color="b", density=True)
        ax[1, 2].set_xlabel("Y [mm]")
        ax[1, 2].set_ylabel("Arb. Intensity")

    def showProportions(self, fov=50, col=50):
        plt.rc("axes", labelsize=12)
        plt.rc("xtick", labelsize=8)
        plt.rc("ytick", labelsize=8)
        get_slices = self.getSlices
        phsp = self.phsp
        phsp_xslice, phsp_yslice = get_slices(phsp, 3)
        fig, ax = plt.subplots(1, 2, figsize=(15, 7))
        sig = 28.0
        ax[0].hist2d(
            phsp["X"], phsp["Y"], bins=100, range=[[-fov, fov], [-fov, fov]],
        )
        ax[0].set_xlabel("X [mm]")
        ax[0].set_ylabel("Y [mm]")

        ax[1].hist(phsp_xslice["X"], bins=50,
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
        ax[1].text(14+d, sizey2, '39%', size=size2, color='white')
        ax[1].text(42+d, sizey2, '47%', size=size2, color='white')
        ax[1].text(70+d, sizey2, '13%', size=size2)
        ax[1].text(98+d, sizey2, '1%', size=size2)
        ax[1].text(126+d, sizey2, '~0%', size=size2)
        sig1 = Circle((0, 0), radius=sig, fc='none', ec='black')
        sig2 = Circle((0, 0), radius=2*sig, fc='none', ec='red')
        sig3 = Circle((0, 0), radius=3*sig, fc='none', ec='orange')
        sig4 = Circle((0, 0), radius=4*sig, fc='none', ec='magenta')
        sig5 = Circle((0, 0), radius=5*sig, fc='none', ec='cyan')

        ax[0].add_artist(sig1)
        ax[0].add_artist(sig2)
        ax[0].add_artist(sig3)
        ax[0].add_artist(sig4)
        ax[0].add_artist(sig5)
