import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kurtosis

# base class of methods for handling and creating topas tracked beams


class automation_utils:
    # home location and thread N argument for ease when running on different pc
    def __init__(self, home_directory="/home/robertsoncl/", no_of_threads="6"):
        self.home_directory = home_directory
        self.no_of_threads = no_of_threads

    # retrieve relevant phase space coordinates from Topas output
    # process and duplicate into several useful file for further processing
    def get_X_Y(self, path_to_file, true_col_rad=5, target_col_rad=2):

        # read Topas ASCII output file
        phase_space = pd.read_csv(
            path_to_file + ".phsp",
            names=["X", "Y", "Z", "PX", "PY", "E", "Weight", "PDG", "9", "10"],
            delim_whitespace=True,
        )
        # add "R" column for radial distance from origin in mm
        phase_space["R"] = np.sqrt(
            np.square(phase_space["X"]) + np.square(phase_space["Y"])
        )
        # create DataFrame containing only electron data at patient
        electron_phase_space = phase_space.drop(
            phase_space[phase_space["PDG"] != 11].index
        )
        # create DataFrame containing only gamma data at patient
        gamma_phase_space = phase_space.drop(
            phase_space[phase_space["PDG"] != 22].index
        )
        # create DataFrame containing electron data within desired spot size(7.5cm)
        # retain based on X coordinates
        col_electron_phase_space = electron_phase_space[
            (electron_phase_space.R < true_col_rad)
        ]
        target_electron_phase_space = electron_phase_space[
            (electron_phase_space.R < target_col_rad)
        ]

        # create DataFrame containing electron data outwith desired spot size (7.5cm)
        # merge full electron frame with collimated frame
        anticol_electron_phase_space = pd.concat(
            [electron_phase_space, col_electron_phase_space]
        )
        # delete duplicates, leaving only outer electrons
        anticol_electron_phase_space = anticol_electron_phase_space.drop_duplicates(
            keep=False
        )

        col_gamma_phase_space = gamma_phase_space[(
            gamma_phase_space.R < true_col_rad)]

        # create DataFrame containing gamma data outwith desired spot size
        # merge full gamma frame with collimated frame
        anticol_gamma_phase_space = pd.concat(
            [gamma_phase_space, col_gamma_phase_space]
        )
        # delete duplicates, leaving only outer gammas
        anticol_gamma_phase_space = anticol_gamma_phase_space.drop_duplicates(
            keep=False
        )
        # retrieve required columns as class attributes for each DataFrame above
        # note multiplication of 10 for each position coordinate
        # Topas output in cm, conversion to mm carried out

        self.total_X = phase_space["X"].dropna() * 10
        # print(len(self.total_X))
        self.total_Y = phase_space["Y"].dropna() * 10
        self.total_E = phase_space["E"].dropna() * 10

        self.X = electron_phase_space["X"].dropna() * 10
        # print(len(self.X))
        self.Y = electron_phase_space["Y"].dropna() * 10
        self.E = electron_phase_space["E"].dropna()
        self.PDG = electron_phase_space["PDG"].dropna()

        self.col_X = col_electron_phase_space["X"].dropna() * 10
        self.col_Y = col_electron_phase_space["Y"].dropna() * 10
        self.col_E = col_electron_phase_space["E"].dropna()
        self.col_PDG = col_electron_phase_space["PDG"].dropna()

        self.target_X = target_electron_phase_space["X"].dropna() * 10
        self.target_Y = target_electron_phase_space["Y"].dropna() * 10
        self.target_E = target_electron_phase_space["E"].dropna()
        self.target_PDG = target_electron_phase_space["PDG"].dropna()

        self.anticol_X = anticol_electron_phase_space["X"].dropna() * 10
        self.anticol_Y = anticol_electron_phase_space["Y"].dropna() * 10
        self.anticol_E = anticol_electron_phase_space["E"].dropna()
        self.anticol_PDG = anticol_electron_phase_space["PDG"].dropna()

        self.gamma_X = gamma_phase_space["X"].dropna() * 10
        self.gamma_Y = gamma_phase_space["Y"].dropna() * 10
        self.gamma_E = gamma_phase_space["E"].dropna()
        self.gamma_PDG = gamma_phase_space["PDG"].dropna()

        self.col_gamma_X = col_gamma_phase_space["X"].dropna() * 10
        self.col_gamma_Y = col_gamma_phase_space["Y"].dropna() * 10
        self.col_gamma_E = col_gamma_phase_space["E"].dropna()
        self.col_gamma_PDG = col_gamma_phase_space["PDG"].dropna()

        self.anticol_gamma_X = anticol_gamma_phase_space["X"].dropna() * 10
        self.anticol_gamma_Y = anticol_gamma_phase_space["Y"].dropna() * 10
        self.anticol_gamma_E = anticol_gamma_phase_space["E"].dropna()
        self.anticol_gamma_PDG = anticol_gamma_phase_space["PDG"].dropna()

        self.path_to_file = path_to_file

    # plot central histograms and overall beam profile of retrieved beam coords
    def plot_transverse_beam(self, save=False):
        # plot density histogram of particle band along x axis
        def histograms_along_x_axis(x, y):
            x_along_axis = []
            x_coords = iter(x)
            y_coords = iter(y)
            interval_around_axis = 1
            interval_for_histograms = 250
            for i in y_coords:
                j = next(x_coords)
                if i < interval_around_axis and i > -interval_around_axis:
                    x_along_axis.append(j)

            plt.figure()
            plt.title("Electron Beam Profile")
            plt.xlabel("X position [mm]")
            plt.ylabel("Number of particles per bin")
            if isinstance(interval_for_histograms, float):
                plt.hist(
                    x_along_axis,
                    bins=400,
                    range=(-interval_for_histograms, interval_for_histograms),
                )
            else:
                plt.hist(x_along_axis, bins=400, range=(-50, 50))

        # plot density histogram of particle band along y axis
        def histograms_along_y_axis(y, x):
            x_along_axis = []
            x_coords = iter(x)
            y_coords = iter(y)
            interval_around_axis = 1
            interval_for_histograms = 250
            for i in y_coords:
                j = next(x_coords)
                if i < interval_around_axis and i > -interval_around_axis:
                    x_along_axis.append(j)

            plt.figure()
            plt.title("Histogram within 10 mm along Y")
            plt.xlabel("Y position [mm]")
            plt.ylabel("Number of particles per bin")
            if isinstance(interval_for_histograms, float):
                plt.hist(
                    x_along_axis,
                    bins=200,
                    range=(-interval_for_histograms, interval_for_histograms),
                )
            else:
                plt.hist(x_along_axis, bins=150, range=(-50, 50))
                print("yoot")

        # retrieve position coordinates
        X = self.X
        Y = self.Y
        E = self.E
        gamma_E = self.gamma_E
        plt.rc("axes", labelsize=10)
        plt.rc("xtick", labelsize=10)
        plt.rc("ytick", labelsize=10)
        histograms_along_x_axis(X, Y)
        histograms_along_y_axis(X, Y)
        plt.figure()
        plt.title("Electron Energy Spectrum")
        plt.hist(self.E, bins=100)
        plt.xlabel("E [MeV]")
        # plot all graphs from functions above
        plt.figure(figsize=(8, 8))
        plt.rc("axes", labelsize=25)
        plt.rc("xtick", labelsize=20)
        plt.rc("ytick", labelsize=20)
        plt.hist2d(X, Y, range=[[-50, 50], [-50, 50]], bins=200)
        plt.figure()
        plt.scatter(X, E, s=1)
        plt.xlabel("X position [mm]")
        plt.ylabel("E [MeV]")
        plt.xlim([-100, 100])
        # plt.hist2d(X, PX, range=[[-5, 5], [-10, 10]])
        if save is True:

            plt.savefig(self.path_to_file + ".png")
        # plt.xlim([-50, 50])
        # plt.ylim([-50, 50])
        plt.xlabel("X [mm]")
        plt.ylabel("Y [mm]")

        x_rms = np.sqrt(np.mean(X ** 2))
        y_rms = np.sqrt(np.mean(Y ** 2))
        print("X RMS = " + str(x_rms) + "mm")
        print("Y RMS = " + str(y_rms) + "mm")
        # cbar = plt.colorbar()
        # cbar.ax.tick_params(labelsize=15)

        print("Total Electrons from Initial Beam: " + str(len(self.X)))
        print("Total Gamma from Initial Beam: " + str(len(self.gamma_X)))
        print("Electrons Removed from Collimation " + str(len(self.anticol_X)))
        print("Electrons at Patient: " + str(len(self.col_X)))
        print("\nPhotons Removed from Collimation " +
              str(len(self.anticol_gamma_X)))
        print(str((len(self.col_X) / len(X)) * 100) +
              "% of inital beam retained")
        print("Photons at Patient: " + str(len(self.col_gamma_X)))
        # print(kurtosis(self.col_X))
        # print(kurtosis(self.col_Y))
        # plt.ylim([-122, -124])
