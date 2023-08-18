import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.signal import savgol_filter
from sklearn.neighbors import KernelDensity
import os, sys
import seaborn as sns


class topas_beam:
    def __init__(self, path_to_file):

        phase_space = pd.read_csv(
            path_to_file,
            names=["X", "Y", "Z", "PX", "PY", "PZ", "E", "2", "3", "4"],
            delim_whitespace=True,
        )
        self.X = phase_space["X"] * 10
        self.Y = phase_space["Y"] * 10
        self.E = phase_space["E"]
        self.phase_space = phase_space

    def plot_transverse_beam(self):
        dataframe = self.phase_space

        def histograms_along_x_axis(x, y):
            x_along_axis = []
            x_coords = iter(x)
            y_coords = iter(y)
            interval_around_axis = 10.0
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
                plt.hist(x_along_axis, bins=200)

        def histograms_along_y_axis(y, x):
            x_along_axis = []
            x_coords = iter(x)
            y_coords = iter(y)
            interval_around_axis = 10.0
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
                plt.hist(x_along_axis, bins=200)

        X = dataframe["X"] * 10
        Z = dataframe["Z"] * 10
        Y = dataframe["Y"] * 10
        PX = dataframe["PX"]
        PY = dataframe["PY"]
        plt.figure()
        plt.scatter(X, Y, s=1)
        histograms_along_x_axis(X, Y)
        histograms_along_y_axis(X, Y)
        self.X = X
        self.Y = Y
        # plt.ylim([-122, -124])

    def get_density_line(self, bins, min_x=-100, max_x=100):
        half_bin = (max_x - min_x) / (bins * 2)
        X = self.X
        Y = self.Y
        # best fit of data
        plt.figure()
        plt.hist(X, bins=bins)
        plt.figure()
        plt.hist(Y, bins=bins)
        plt.xlabel("X [mm]")
        X_n = np.histogram(X, bins=bins)[0]
        X_bins = np.arange(
            min_x + half_bin, max_x + half_bin, step=(max_x - min_x) / bins
        )
        shape_y = X_n
        shape_x = X_bins
        smoothed_y = savgol_filter(shape_y, 21, 2)
        smoothed_y = smoothed_y - min(smoothed_y)
        fig, ax = plt.subplots()
        ax.set_xlabel("X [mm]")
        ax.plot(shape_x, shape_y, color="red")
        ax.plot(shape_x, smoothed_y, color="black")
        ax.set_xlim([-30, 30])
        return shape_x, smoothed_y


# create swept out 3d shape in topas from x,y input
def construct_topas_shape(x, y, max_height):
    beam_to_S2 = 1
    S2_to_scorer = 500
    max_y = max(y)
    scaling_factor = max_height / max_y
    y = y * scaling_factor
    x_width = (x[len(x) - 1] - x[0]) / len(x)
    half_y = y / 2
    half_x_width = x_width / 2
    indices = np.arange(0, len(x), step=1)
    xincrements = indices * x_width
    file = open("/home/robertsoncl/topas/scattering_foil/gaussian3d.txt", "w")
    file.write("i:Ts/NumberOfThreads=6\n")
    file.write("d:Ge/World/HLX = 5.0 m\n")
    file.write("d:Ge/World/HLY = 5.0 m\n")
    file.write("d:Ge/World/HLZ = 5.0 m\n")

    file.write('s:Ge/World/Material = "Vacuum"\n')
    halfy = y
    # start loop here
    # topas code to construct 2d gaussian

    i = 1
    while x[i] < 0:
        if half_y[i] - half_y[i - 1] <= 0:
            i = i + 1
            continue
        else:
            sname = "slice" + str(i)

            file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
            file.write("s:Ge/" + sname + '/Parent="World"\n')
            file.write("s:Ge/" + sname + '/Material="Lead"\n')
            # set radius of cylinder
            file.write("d:Ge/" + sname + "/Rmax = " + str(abs(x[i])) + " mm\n")
            file.write("d:Ge/" + sname + "/Rmin= 0 mm\n")
            file.write(
                "d:Ge/" + sname + "/HL = " + str(half_y[i] - half_y[i - 1]) + " mm\n"
            )
            file.write(
                "d:Ge/"
                + sname
                + "/TransZ = "
                + str(y[i] - (max_height + beam_to_S2))
                + " mm\n"
            )
            # file.write("s:Ge/" + sname + '/DrawingStyle = "WireFrame"\n')
            i = i + 1
    file.write('s:So/S1_source/Type = "PhaseSpace"\n')
    file.write('s:So/S1_source/Component = "World"\n')
    file.write('s:So/S1_source/PhaseSpaceFileName = "S1_beam"\n')
    file.write('b:So/S1_source/PhaseSpacePreCheck = "True"\n')
    file.write("u:So/S1_source/PhaseSpaceScaleZPosBy = 0.\n")
    # file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
    # file.write("i:Gr/ViewA/WindowSizeX      = 1024\n")
    # file.write("i:Gr/ViewA/WindowSizeY      = 768\n")
    # file.write('b:Gr/ViewA/IncludeAxes      = "True"\n')
    # file.write("d:Gr/ViewA/Theta = 45. deg\n")
    # file.write("d:Gr/ViewA/Phi = 45. deg\n")
    # file.write("u:Gr/ViewA/Zoom = 100.\n")
    file.write('b:Ts/PauseBeforeQuit = "True"\n')
    file.write('b:Ge/CheckForOverlaps = "False" \n')
    file.write('b:Ge/QuitIfOverlapDetected = "False"\n')
    file.write('s:Ge/ScorerSurface/Type="TsBox"\n')
    file.write('s:Ge/ScorerSurface/Parent = "World"\n')
    file.write('s:Ge/ScorerSurface/Material="Vacuum"\n')
    file.write("d:Ge/ScorerSurface/HLX = 1 m\n")
    file.write("d:Ge/ScorerSurface/HLY = 1 m\n")
    file.write("d:Ge/ScorerSurface/HLZ = 0.1 mm\n")
    file.write(
        "d:Ge/ScorerSurface/TransZ = "
        + str(-(max_height + beam_to_S2 + S2_to_scorer))
        + " mm\n"
    )
    file.write('s:Sc/S2_beam/Quantity = "PhaseSpace"\n')
    file.write('s:Sc/S2_beam/Surface = "ScorerSurface/ZPlusSurface"\n')
    file.write('s:Sc/S2_beam/OutputType = "ASCII"\n')
    file.write('s:Sc/S2_beam/IfOutputFileAlreadyExists = "Overwrite"\n')
    file.write('sv:Gr/OnlyIncludeParticlesNamed = 1 "e-"\n')
    file.close()


def main():
    S1_beam = topas_beam("S1_beam.phsp")
    x, y = S1_beam.get_density_line(bins=100, min_x=-100, max_x=100)
    # construct_topas_shape(x, y, max_height=1)
    # S2_beam = topas_beam("S2_beam.phsp")
    # x, y = S2_beam.get_density_line(bins=300, min_x=-1000, max_x=1000)


# main()
