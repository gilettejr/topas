from automation_utils import automation_utils
import numpy as np
import os
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

# class of methods used for optimising S2 shape and sizes
class gaussian_optimiser_utils(automation_utils):
    # import beam profile from 'S1_beam'
    # create 3d gaussian shape from input arguments in topas
    # send beam through shape and into scorer, save phsp distribution
    def run_through_gaussian_foil(
        self,
        sigma,
        max_height,
        beam_to_S2,
        shape_radius=False,
        show_shape=False,
        filename="scattering_foil/gaussian3d.txt",
        input_filename='"S1beam"',
    ):
        # set radius of desired beam profile
        # should be the same as S1_source radius
        beam_to_S2 = beam_to_S2 - 1
        # angle = 0.0530
        # initial_beam_rad = 1
        # half_width = beam_to_S2 * np.tan(angle) + initial_beam_rad

        # half_width = 1.0
        # max_height = 2.0
        # sigma = 1

        # define spread of gaussian shape
        # and precision (number of slices in shape) with step argument
        # x = np.arange(-half_width, half_width, step=1)
        x_di = 200
        step = 5
        slice_no = x_di / step
        x_old = np.arange(-100, 100, step=5)
        # define expectation value of Gaussian = 0 for symmetry
        mu = 0
        # construct gaussian profile from method argument sigma
        y = norm.pdf(x_old, mu, sigma)
        x = []
        for i in range(len(y)):
            if y[i] < 1e-6:
                x.append(np.nan)
            else:
                x.append(x_old[i])
        # plt.plot(x, y)
        x = np.array(x)
        x = x[np.logical_not(np.isnan(x))]
        x_new_di = x.max() - x.min()
        x_new = np.arange(x.min(), x.max(), step=x_new_di / slice_no)
        y = norm.pdf(x_new, mu, sigma)
        # scale height and normalise base to 0
        # according to method argument max_height

        y = y - min(y)
        y_scaling_factor = max_height / max(y)
        y = y * y_scaling_factor
        x = x_new

        if shape_radius is not False:
            old_radius = max(x)
            x = x * shape_radius / old_radius

        # define distance in mm from beam source to gaussian foil
        S2_to_scorer = 2500 - beam_to_S2 - max_height
        # define half_y for ease, as Topas uses half lengths
        half_y = y / 2
        if show_shape is True:
            shape_frame = pd.DataFrame({"X": x, "Y": y})
            title = (
                str(round(sigma, 2))
                + "_"
                + str(round(max_height, 2))
                + "_"
                + str(round(beam_to_S2, 2))
            )
            shape_frame.to_parquet(title)
            plt.plot(x, y)
            plt.xlabel("R [mm]")
            plt.ylabel("Z [mm]")
        # create new text file for Topas script
        file = open(self.home_directory + "topas/" + filename, "w")
        # set number of threads depending on computing power available
        file.write("i:Ts/NumberOfThreads=" + self.no_of_threads + "\n")
        # define arbitrarily large world
        file.write("d:Ge/World/HLX = 5.0 m\n")
        file.write("d:Ge/World/HLY = 5.0 m\n")
        file.write("d:Ge/World/HLZ = 5.0 m\n")
        # set world as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')
        # begin setting up loop for construction of Gaussian shape
        # start at 1 to prevent errors and null slices
        i = 1
        # begin loop to create stack of cylinders following Gaussian shape
        while x[i] < 0:
            # Don't try to create 0 height widths
            # skip relevant rows
            if half_y[i] - half_y[i - 1] <= 0:
                i = i + 1
                continue

            else:
                if i == 1:
                    prev_HL = 0
                HL = (y[i] - y[i - 1]) - prev_HL
                if HL < 0.1:
                    i = i + 1
                    continue
                if HL <= 0:
                    break

                # define slice name - required for Topas
                sname = "slice" + str(i)
                file.write("d:Ge/" + sname + "/HL = " + str(HL) + " mm\n")
                prev_HL = HL
                # define slice as cylinder
                file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
                # in previously defined world
                file.write("s:Ge/" + sname + '/Parent="World"\n')
                # define material
                file.write("s:Ge/" + sname + '/Material="Aluminum"\n')
                # set radius of slice from horizontal slice steps
                file.write("d:Ge/" + sname + "/Rmax = " + str(abs(x[i])) + " mm\n")
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
                    + "/TransZ = "
                    + str(y[i] - (max_height + beam_to_S2))
                    + " mm\n"
                )
                # increment to begin next slice until shape completion
                i = i + 1
        # set up beam source at origin
        file.write('s:So/S1_source/Type = "PhaseSpace"\n')
        file.write('s:So/S1_source/Component = "World"\n')
        # import from previously run S1beam file to get correct phase space
        file.write("s:So/S1_source/PhaseSpaceFileName = " + input_filename + "\n")
        file.write('b:So/S1_source/PhaseSpacePreCheck = "False"\n')
        file.write("u:So/S1_source/PhaseSpaceScaleZPosBy = 0.\n")
        # uncomment for graphics options

        # file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
        # file.write("i:Gr/ViewA/WindowSizeX      = 1024\n")
        # file.write("i:Gr/ViewA/WindowSizeY      = 768\n")
        # file.write('b:Gr/ViewA/IncludeAxes      = "True"\n')
        # file.write("d:Gr/ViewA/Theta = 45. deg\n")
        # file.write("d:Gr/ViewA/Phi = 45. deg\n")
        # file.write("u:Gr/ViewA/Zoom = 10.\n")
        # file.write('b:Ts/PauseBeforeQuit = "True"\n')
        # file.write('b:Ts/UseQt = "True"\n')

        # set various checks to 0 to decrease RunTime
        file.write('b:Ge/CheckForOverlaps = "False" \n')
        file.write('b:Ge/QuitIfOverlapDetected = "False"\n')
        # define scorer surface
        file.write('s:Ge/ScorerSurface/Type="TsBox"\n')
        file.write('s:Ge/ScorerSurface/Parent = "World"\n')
        # set arbitrary material - vacuum for simplicity
        file.write('s:Ge/ScorerSurface/Material="Vacuum"\n')
        # set arbitrarily large surface area of scorer
        file.write("d:Ge/ScorerSurface/HLX = 1 m\n")
        file.write("d:Ge/ScorerSurface/HLY = 1 m\n")
        # set small thickness for precision
        file.write("d:Ge/ScorerSurface/HLZ = 0.01 mm\n")
        # set at appropriate distance for consistency between variables
        file.write(
            "d:Ge/ScorerSurface/TransZ = "
            + str(-(max_height + beam_to_S2 + S2_to_scorer))
            + " mm\n"
        )
        # set up phase space scorer
        file.write('s:Sc/S2_beam/Quantity = "PhaseSpace"\n')
        # place at previously defined patient location
        file.write('s:Sc/S2_beam/Surface = "ScorerSurface/ZPlusSurface"\n')
        # output as ascii file
        file.write('s:Sc/S2_beam/OutputType = "ASCII"\n')
        file.write('s:Sc/S2_beam/IfOutputFileAlreadyExists = "Overwrite"\n')
        # reduce terminal output to improve RunTime and reduce clutter
        file.write('b:Sc/S2_beam/OutputToConsole = "False"\n')
        file.write('b:Ph/ListProcesses = "False"\n')
        file.write('b:Ge/CheckForUnusedComponents = "False"\n')

        # Topas script complete, close file
        file.close()
        # set up environment for topas
        os.system(
            "export TOPAS_G4_DATA_DIR="
            + self.home_directory
            + "G4Data\n./bin/topas "
            + filename
        )
