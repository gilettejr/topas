from thickness_optimiser_utils import thickness_optimiser_utils
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# x,y for 150=1.83657125mm x 0.99433641
# px,py for 150=7.80910106 5.78318716


class clear_experiment_utils(thickness_optimiser_utils):
    def run_through_s1_clear(
        self,
        s1_thickness,
        distance_to_patient,
        sigma_x=0.86,
        sigma_y=1.14,
        sigma_px=4.17,
        sigma_py=3.26,
        material='"G4_NYLON-6-6"',
        N=10,
        energy=200,
        score_at_S1=False,
    ):
        # set inputs as class attributes, required for further analysis
        self.s1_thickness = s1_thickness
        self.distance_to_patient = distance_to_patient
        self.material = material
        self.energy = energy
        # define half_length - useful for Topas script writing
        half_length = s1_thickness / 2
        # begin constructing topas text file
        # create new file with write permission
        file = open("material_classifications/S1_run.txt", "w")
        # set number of threads for multithreading
        file.write("i:Ts/NumberOfThreads=" + self.no_of_threads + "\n")
        # define large, square world
        file.write("d:Ge/World/HLX = 30.0 m\n")
        file.write("d:Ge/World/HLY = 30.0 m\n")
        file.write("d:Ge/World/HLZ = 30.0 m\n")
        # set world material as vacuum for simplicity
        file.write('s:Ge/World/Material = "G4_AIR"\n')
        # begin defining S1 scatterer
        # cylinder used, for rotational symmetry
        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/S1/Material=" + material + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  10  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define s1_thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(half_length) + " mm\n")
        if distance_to_patient == 500:
            # set position of scatterer so that the edge is on the origin
            file.write("d:Ge/S1/TransZ = -" + str(half_length) + " mm\n")
        else:
            print("reduced length")
            file.write("d:Ge/S1/TransZ = -" + str(half_length + 250) + " mm\n")
        # define beam beginning on origin, directed in -Z direction into S1
        file.write('s:So/acc_source/Type = "Beam"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        # specify electron beam
        file.write('s:So/acc_source/BeamParticle="e-"\n')
        # set energy to 100 MeV
        file.write("d:So/acc_source/BeamEnergy= " + str(energy) + " MeV \n")
        # define initial beam distribution as flat with 1mm radius
        file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')
        file.write("d:So/acc_source/BeamPositionCutoffX = 100 mm\n")
        file.write("d:So/acc_source/BeamPositionCutoffY = 100 mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadX = " +
                   str(sigma_x) + " mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadY = " +
                   str(sigma_y) + " mm\n")
        file.write("d:So/acc_source/BeamAngularSpreadX= " +
                   str(sigma_px) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularSpreadY= " +
                   str(sigma_py) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffX= 100 mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffY = 100 mrad\n")
        file.write('s:So/acc_source/BeamAngularDistribution="Gaussian"\n')
        # set delta E to 0
        file.write("u:So/acc_source/BeamEnergySpread = 0.05\n")
        # set beam as ellipse rather than rectangle
        file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')
        # uncomment below to view Topas graphics and alter perspective etc
        file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
        # file.write("i:Gr/ViewA/WindowSizeX      = 1024\n")
        # file.write("i:Gr/ViewA/WindowSizeY      = 768\n")
        # file.write('b:Gr/ViewA/IncludeAxes      = "True"\n')
        # file.write("d:Gr/ViewA/Theta = 45. deg\n")
        # file.write("d:Gr/ViewA/Phi = 45. deg\n")
        # file.write("u:Gr/ViewA/Zoom = 1000.\n")
        # file.write('b:Ts/PauseBeforeQuit = "True"\n')
        file.write('b:Ts/UseQt = "True"\n')

        # initialise scorer
        file.write('s:Ge/PatientScorerSurface/Type="TsBox"\n')
        file.write('s:Ge/PatientScorerSurface/Parent = "World"\n')
        # set arbitrary material as vacuum for simplicity
        file.write('s:Ge/PatientScorerSurface/Material="G4_AIR"\n')
        # set to arbitrarily large transverse size to ensure full beam coverage
        file.write("d:Ge/PatientScorerSurface/HLX = 0.1 m\n")
        file.write("d:Ge/PatientScorerSurface/HLY = 0.1 m\n")
        file.write("d:Ge/PatientScorerSurface/HLZ = 0.01 mm\n")
        # place scorer based on distance_to_patient input from end of S1 scatterer
        file.write(
            "d:Ge/PatientScorerSurface/TransZ = -"
            + str(half_length * 2 + 500 + 0.01)
            + " mm\n"
        )

        # set surface facing beam as scoring surface
        file.write(
            's:Sc/clear_beam_after_s1/Surface = "PatientScorerSurface/ZPlusSurface"\n'
        )
        # initialise phase space scorer on defined surface
        file.write('s:Sc/clear_beam_after_s1/Quantity = "PhaseSpace"\n')
        # output phase space beam data to ASCII file
        file.write('s:Sc/clear_beam_after_s1/OutputType = "ASCII"\n')
        # overwrite file from previous runs
        file.write(
            's:Sc/clear_beam_after_s1/IfOutputFileAlreadyExists = "Overwrite"\n')
        # reduce console output for repeated optimisation runs
        file.write('b:Sc/clear_beam_after_s1/OutputToConsole = "False"\n')
        if score_at_S1 is True:
            # initialise scorer
            file.write('s:Ge/S1ScorerSurface/Type="TsBox"\n')
            file.write('s:Ge/S1ScorerSurface/Parent = "World"\n')
            # set arbitrary material as vacuum for simplicity
            file.write('s:Ge/S1ScorerSurface/Material="Vacuum"\n')
            # set to arbitrarily large transverse size to ensure full beam coverage
            file.write("d:Ge/S1ScorerSurface/HLX = 0.3 m\n")
            file.write("d:Ge/S1ScorerSurface/HLY = 0.3 m\n")
            file.write("d:Ge/S1ScorerSurface/HLZ = 0.0001 mm\n")
            # place scorer based on distance_to_patient input from end of S1 scatterer
            file.write(
                "d:Ge/S1ScorerSurface/TransZ = -" +
                str(half_length * 2 + 1) + " mm\n"
            )

            # set surface facing beam as scoring surface
            file.write(
                's:Sc/clear_S1beam/Surface = "S1ScorerSurface/ZPlusSurface"\n')
            # initialise phase space scorer on defined surface
            file.write('s:Sc/clear_S1beam/Quantity = "PhaseSpace"\n')
            # output phase space beam data to ASCII file
            file.write('s:Sc/clear_S1beam/OutputType = "ASCII"\n')
            # overwrite file from previous runs
            file.write(
                's:Sc/clear_S1beam/IfOutputFileAlreadyExists = "Overwrite"\n')
            # reduce console output for repeated optimisation runs
            file.write('b:Sc/clear_S1beam/OutputToConsole = "False"\n')

        file.write('b:Ph/ListProcesses = "False"\n')
        # turn off uneccesary overlap and component checks to decrease runtime
        file.write('b:Ge/CheckForOverlaps = "False" \n')
        file.write('b:Ge/QuitIfOverlapDetected = "False"\n')
        file.write('b:Ge/CheckForUnusedComponents = "False"')
        # close written file
        file.close()
        # point topas to Geant4 data firectory
        os.system(
            "export TOPAS_G4_DATA_DIR="
            + self.home_directory
            + "G4Data\n./bin/topas material_classifications/S1_run.txt"
        )

    def run_through_s1_and_s2_clear(
        self,
        s1_thickness,
        s1_to_patient,
        sigma,
        max_height,
        shape_radius,
        s1_to_s2=250,
        show_shape=False,
        N_slices=40,
        sigma_x=0.86,
        sigma_y=1.14,
        sigma_px=4.17,
        sigma_py=3.26,
        material='"G4_NYLON-6-6"',
        N=10000,
        ut_filename_ext="",
        energy=200,
        slice_half_thickness_limit=2,
        perspex_pos=False,
        jitter_matrix=[[[0, 0], [0, 0, 0]], [
            [0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]]],
        show_setup=False,
        output_filename_ext="",
    ):
        jm = jitter_matrix
        beam_pos_jitter = jm[0][0]
        beam_angle_jitter = jm[0][1]
        s1_pos_jitter = jm[1][0]
        s1_angle_jitter = jm[1][1]
        s2_pos_jitter = jm[2][0]
        s2_angle_jitter = jm[2][1]
        # define half_length - useful for Topas script writing
        half_length = s1_thickness / 2

        s2_half_length = max_height / 2
        # begin constructing topas text file
        # create new file with write permission
        file = open("material_classifications/s1_s2_clear_run.txt", "w")
        # set number of threads for multithreading
        file.write("i:Ts/NumberOfThreads=" + self.no_of_threads + "\n")
        # define large, square world
        file.write("d:Ge/World/HLX = 30.0 m\n")
        file.write("d:Ge/World/HLY = 30.0 m\n")
        file.write("d:Ge/World/HLZ = 30.0 m\n")
        # set world material as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')
        # begin defining S1 scatterer
        # cylinder used, for rotational symmetry
        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write('s:Ge/S1/Material="G4_NYLON-6-6"\n')

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  10  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define s1_thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(half_length) + " mm\n")
        file.write("d:Ge/S1/TransZ = -" + str(half_length) + " mm\n")
        file.write("d:Ge/S1/TransX = " + str(s1_pos_jitter[0]) + " mm\n")
        file.write("d:Ge/S1/TransY = " + str(s1_pos_jitter[1]) + " mm\n")
        file.write("d:Ge/S1/RotZ = " + str(s1_angle_jitter[2]) + " mrad\n")
        file.write("d:Ge/S1/RotX = " + str(s1_angle_jitter[0]) + " mrad\n")
        file.write("d:Ge/S1/RotY = " + str(s1_angle_jitter[1]) + " mrad\n")
        # define beam beginning on origin, directed in -Z direction into S1
        file.write('s:So/acc_source/Type = "Beam"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        file.write("d:Ge/BeamPosition/TransX= " +
                   str(beam_pos_jitter[0]) + " mm\n")
        file.write("d:Ge/BeamPosition/TransY= " +
                   str(beam_pos_jitter[1]) + " mm\n")
        # file.write("d:Ge/BeamPosition/RotZ= " + str(beam_angle_jitter[2]) + " mrad\n")
        # file.write("d:Ge/BeamPosition/RotX= " + str(beam_angle_jitter[0]) + " mrad\n")
        # file.write("d:Ge/BeamPosition/RotY= " + str(beam_angle_jitter[1]) + " mrad\n")
        # specify electron beam
        file.write('s:So/acc_source/BeamParticle="e-"\n')
        # set energy to 100 MeV
        file.write("d:So/acc_source/BeamEnergy= " + str(energy) + " MeV \n")
        # define initial beam distribution as flat with 1mm radius
        file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')
        file.write("d:So/acc_source/BeamPositionCutoffX = 100 mm\n")
        file.write("d:So/acc_source/BeamPositionCutoffY = 100 mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadX = " +
                   str(sigma_x) + " mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadY = " +
                   str(sigma_y) + " mm\n")
        file.write("d:So/acc_source/BeamAngularSpreadX= " +
                   str(sigma_px) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularSpreadY= " +
                   str(sigma_py) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffX= 100 mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffY = 100 mrad\n")
        file.write('s:So/acc_source/BeamAngularDistribution="Gaussian"\n')
        # set delta E to 0
        file.write("u:So/acc_source/BeamEnergySpread = 0.05\n")
        # set beam as ellipse rather than rectangle
        file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')

        # initialise scorer
        file.write('s:Ge/PatientScorerSurface/Type="TsBox"\n')
        file.write('s:Ge/PatientScorerSurface/Parent = "World"\n')
        # set arbitrary material as vacuum for simplicity
        file.write('s:Ge/PatientScorerSurface/Material="G4_AIR"\n')
        # set to arbitrarily large transverse size to ensure full beam coverage
        file.write("d:Ge/PatientScorerSurface/HLX = 0.1 m\n")
        file.write("d:Ge/PatientScorerSurface/HLY = 0.1 m\n")
        file.write("d:Ge/PatientScorerSurface/HLZ = 0.01 mm\n")
        # place scorer based on distance_to_patient input from end of S1 scatterer
        file.write(
            "d:Ge/PatientScorerSurface/TransZ = -" +
            str(s1_to_patient) + " mm\n"
        )
        # set radius of desired beam profile
        # should be the same as S1_source radius

        # define spread of gaussian shape
        # and precision (number of slices in shape) with step argument
        # x = np.arange(-half_width, half_width, step=1)
        x_di = 200
        step = x_di / N_slices
        slice_no = x_di / step
        x_old = np.arange(-100, 100, step=step)
        # define expectation value of Gaussian = 0 for symmetry
        mu = 0
        # construct gaussian profile from method argument sigma
        y = norm.pdf(x_old, mu, sigma)
        x = []
        for i in range(len(y)):
            if y[i] < 1e-12:
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

        old_radius = max(x)
        x = x * shape_radius / old_radius

        # define half_y for ease, as Topas uses half lengths
        half_y = y / 2
        if show_shape is True:
            plt.plot(x, y)
            plt.xlabel("R [mm]")
            plt.ylabel("Z [mm]")

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
                if HL <= 0:
                    break
                elif HL < slice_half_thickness_limit or abs(x[i]) < 2.5:
                    i = i + 1
                    continue

                # define slice name - required for Topas
                sname = "slice" + str(i)
                #file.write("d:Ge/" + sname + "/TransX = 1 mm\n")
                file.write("d:Ge/" + sname + "/HL = " + str(HL) + " mm\n")
                prev_HL = HL
                # define slice as cylinder
                file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
                # in previously defined world
                file.write("s:Ge/" + sname + '/Parent="World"\n')
                # define material
                file.write("s:Ge/" + sname + "/Material=" + material + "\n")
                # set radius of slice from horizontal slice steps
                file.write("d:Ge/" + sname + "/Rmax = " +
                           str(abs(x[i])) + " mm\n")
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
                    + str(y[i] - (max_height / 2 + s1_to_s2))
                    + " mm\n"
                )
                # file.write(
                #    "d:Ge/" + sname + "/TransY= " +
                #    str(s2_pos_jitter[1]) + " mm\n"
                # )
                if perspex_pos == i:
                    file.write("d:Ge/perspex/HL = 2.85 mm\n")
                    file.write('s:Ge/perspex/Type = "TsCylinder"\n')
                    file.write('s:Ge/perspex/Parent = "World"\n')
                    file.write('s:Ge/perspex/Material="Vacuum"\n')
                    file.write("d:Ge/perspex/Rmax = 30 mm\n")
                    file.write("d:Ge/perspex/Rmin=" + str(abs(x[i])) + " mm\n")
                    file.write(
                        "d:Ge/perspex/TransZ = "
                        + str((y[i] - (max_height / 2 + s1_to_s2)) + (2.85 - HL))
                        + " mm\n"
                    )
                # increment to begin next slice until shape completion
                i = i + 1

        # uncomment for graphics options
        if show_setup is True:
            file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
            file.write('b:Ts/UseQt = "True"\n')

        # set various checks to 0 to decrease RunTime
        file.write('b:Ge/CheckForOverlaps = "False" \n')
        file.write('b:Ge/QuitIfOverlapDetected = "False"\n')

        # set up phase space scorer
        file.write("s:Sc/S2_beam" + output_filename_ext +
                   '/Quantity = "PhaseSpace"\n')
        # place at previously defined patient location
        file.write(
            "s:Sc/S2_beam"
            + output_filename_ext
            + '/Surface = "PatientScorerSurface/ZPlusSurface"\n'
        )
        # output as ascii file
        file.write("s:Sc/S2_beam" + output_filename_ext +
                   '/OutputType = "ASCII"\n')
        file.write(
            "s:Sc/S2_beam"
            + output_filename_ext
            + '/IfOutputFileAlreadyExists = "Overwrite"\n'
        )
        # reduce terminal output to improve RunTime and reduce clutter
        file.write(
            "b:Sc/S2_beam" + output_filename_ext + '/OutputToConsole = "False"\n'
        )
        file.write('b:Ph/ListProcesses = "False"\n')
        file.write('b:Ge/CheckForUnusedComponents = "False"\n')
        # Topas script complete, close file
        file.close()
        # set up environment for topas
        os.system(
            "export TOPAS_G4_DATA_DIR="
            + self.home_directory
            + "G4Data\n./bin/topas material_classifications/s1_s2_clear_run.txt"
        )

    def run_through_yag_and_s2_tank_clear(
        self,
        s1_thickness,
        s1_to_patient,
        sigma,
        max_height,
        shape_radius,
        s1_to_s2=410,
        show_shape=False,
        N_slices=40,
        sigma_x=0.86,
        sigma_y=1.14,
        sigma_px=4.17,
        sigma_py=3.26,
        material='"Aluminum"',
        N=10000,
        ut_filename_ext="",
        energy=200,
        slice_half_thickness_limit=2,
        perspex_pos=False,
        jitter_matrix=[[[0, 0], [0, 0, 0]], [
            [0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]]],
        output_filename_ext="",
    ):
        jm = jitter_matrix
        beam_pos_jitter = jm[0][0]
        beam_angle_jitter = jm[0][1]
        s1_pos_jitter = jm[1][0]
        s1_angle_jitter = jm[1][1]
        s2_pos_jitter = jm[2][0]
        s2_angle_jitter = jm[2][1]
        # define half_length - useful for Topas script writing
        half_length = s1_thickness / 2

        s2_half_length = max_height / 2
        # begin constructing topas text file
        # create new file with write permission
        file = open("material_classifications/s1_s2_clear_run.txt", "w")
        # set number of threads for multithreading
        file.write("i:Ts/NumberOfThreads=" + self.no_of_threads + "\n")
        # define large, square world
        file.write("d:Ge/World/HLX = 30.0 m\n")
        file.write("d:Ge/World/HLY = 30.0 m\n")
        file.write("d:Ge/World/HLZ = 30.0 m\n")
        # set world material as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')
        # begin defining S1 scatterer
        # cylinder used, for rotational symmetry
        file.write('s:Ge/tank/Type = "TsBox"\n')
        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # file.write('s:Ge/tank/Parent = "World"\n')
        # file.write('s:Ge/tank/Material="G4_WATER"\n')
        # file.write("d:Ge/tank/TransZ = -610 mm\n")
        file.write("d:Ge/tank/HLZ = 200 mm\n")
        file.write("d:Ge/tank/HLX = 100 mm\n")
        file.write("d:Ge/tank/HLY = 100 mm\n")
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write('s:Ge/S1/Material="G4_NYLON-6-6"\n')

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  10  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define s1_thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(half_length) + " mm\n")
        file.write("d:Ge/S1/TransZ = -" + str(half_length) + " mm\n")
        file.write("d:Ge/S1/TransX = " + str(s1_pos_jitter[0]) + " mm\n")
        file.write("d:Ge/S1/TransY = " + str(s1_pos_jitter[1]) + " mm\n")
        file.write("d:Ge/S1/RotZ = " + str(s1_angle_jitter[2]) + " mrad\n")
        file.write("d:Ge/S1/RotX = " + str(s1_angle_jitter[0]) + " mrad\n")
        file.write("d:Ge/S1/RotY = " + str(s1_angle_jitter[1]) + " mrad\n")
        # define beam beginning on origin, directed in -Z direction into S1
        file.write('s:So/acc_source/Type = "Beam"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        file.write("d:Ge/BeamPosition/TransX= " +
                   str(beam_pos_jitter[0]) + " mm\n")
        file.write("d:Ge/BeamPosition/TransY= " +
                   str(beam_pos_jitter[1]) + " mm\n")
        # file.write("d:Ge/BeamPosition/RotZ= " + str(beam_angle_jitter[2]) + " mrad\n")
        # file.write("d:Ge/BeamPosition/RotX= " + str(beam_angle_jitter[0]) + " mrad\n")
        # file.write("d:Ge/BeamPosition/RotY= " + str(beam_angle_jitter[1]) + " mrad\n")
        # specify electron beam
        file.write('s:So/acc_source/BeamParticle="e-"\n')
        # set energy to 100 MeV
        file.write("d:So/acc_source/BeamEnergy= " + str(energy) + " MeV \n")
        # define initial beam distribution as flat with 1mm radius
        file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')
        file.write("d:So/acc_source/BeamPositionCutoffX = 100 mm\n")
        file.write("d:So/acc_source/BeamPositionCutoffY = 100 mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadX = " +
                   str(sigma_x) + " mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadY = " +
                   str(sigma_y) + " mm\n")
        file.write("d:So/acc_source/BeamAngularSpreadX= " +
                   str(sigma_px) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularSpreadY= " +
                   str(sigma_py) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffX= 100 mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffY = 100 mrad\n")
        file.write('s:So/acc_source/BeamAngularDistribution="Gaussian"\n')
        # set delta E to 0
        file.write("u:So/acc_source/BeamEnergySpread = 0.05\n")
        # set beam as ellipse rather than rectangle
        file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')

        # initialise scorer
        file.write('s:Ge/PatientScorerSurface/Type="TsBox"\n')
        file.write('s:Ge/PatientScorerSurface/Parent = "World"\n')
        # set arbitrary material as vacuum for simplicity
        file.write('s:Ge/PatientScorerSurface/Material="G4_AIR"\n')
        # set to arbitrarily large transverse size to ensure full beam coverage
        file.write("d:Ge/PatientScorerSurface/HLX = 0.1 m\n")
        file.write("d:Ge/PatientScorerSurface/HLY = 0.1 m\n")
        file.write("d:Ge/PatientScorerSurface/HLZ = 0.01 mm\n")
        # place scorer based on distance_to_patient input from end of S1 scatterer
        file.write(
            "d:Ge/PatientScorerSurface/TransZ = -" +
            str(s1_to_patient) + " mm\n"
        )
        # set radius of desired beam profile
        # should be the same as S1_source radius

        # define spread of gaussian shape
        # and precision (number of slices in shape) with step argument
        # x = np.arange(-half_width, half_width, step=1)
        x_di = 200
        step = x_di / N_slices
        slice_no = x_di / step
        x_old = np.arange(-100, 100, step=step)
        # define expectation value of Gaussian = 0 for symmetry
        mu = 0
        # construct gaussian profile from method argument sigma
        y = norm.pdf(x_old, mu, sigma)
        x = []
        for i in range(len(y)):
            if y[i] < 1e-12:
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

        old_radius = max(x)
        x = x * shape_radius / old_radius

        # define half_y for ease, as Topas uses half lengths
        half_y = y / 2
        if show_shape is True:
            plt.plot(x, y)
            plt.xlabel("R [mm]")
            plt.ylabel("Z [mm]")

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
                if HL <= 0:
                    break
                elif HL < slice_half_thickness_limit or abs(x[i]) < 2.5:
                    i = i + 1
                    continue

                # define slice name - required for Topas
                sname = "slice" + str(i)
                file.write("d:Ge/" + sname + "/HL = " + str(HL) + " mm\n")
                prev_HL = HL
                # define slice as cylinder
                file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
                # in previously defined world
                file.write("s:Ge/" + sname + '/Parent="World"\n')
                # define material
                file.write("s:Ge/" + sname + "/Material=" + material + "\n")
                # set radius of slice from horizontal slice steps
                file.write("d:Ge/" + sname + "/Rmax = " +
                           str(abs(x[i])) + " mm\n")
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
                    + str(y[i] - (max_height / 2 + s1_to_s2))
                    + " mm\n"
                )
                file.write(
                    "d:Ge/" + sname + "/TransX= " +
                    str(s2_pos_jitter[0]) + " mm\n"
                )
                file.write(
                    "d:Ge/" + sname + "/TransY= " +
                    str(s2_pos_jitter[1]) + " mm\n"
                )
                if perspex_pos == i:
                    file.write("d:Ge/perspex/HL = 2.85 mm\n")
                    file.write('s:Ge/perspex/Type = "TsCylinder"\n')
                    file.write('s:Ge/perspex/Parent = "World"\n')
                    file.write('s:Ge/perspex/Material="Vacuum"\n')
                    file.write("d:Ge/perspex/Rmax = 30 mm\n")
                    file.write("d:Ge/perspex/Rmin=" + str(abs(x[i])) + " mm\n")
                    file.write(
                        "d:Ge/perspex/TransZ = "
                        + str((y[i] - (max_height / 2 + s1_to_s2)) + (2.85 - HL))
                        + " mm\n"
                    )
                # increment to begin next slice until shape completion
                i = i + 1

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

        # set up phase space scorer
        file.write("s:Sc/S2_beam" + output_filename_ext +
                   '/Quantity = "PhaseSpace"\n')
        # place at previously defined patient location
        file.write(
            "s:Sc/S2_beam"
            + output_filename_ext
            + '/Surface = "PatientScorerSurface/ZPlusSurface"\n'
        )
        # output as ascii file
        file.write("s:Sc/S2_beam" + output_filename_ext +
                   '/OutputType = "ASCII"\n')
        file.write(
            "s:Sc/S2_beam"
            + output_filename_ext
            + '/IfOutputFileAlreadyExists = "Overwrite"\n'
        )
        # reduce terminal output to improve RunTime and reduce clutter
        file.write(
            "b:Sc/S2_beam" + output_filename_ext + '/OutputToConsole = "False"\n'
        )
        file.write('b:Ph/ListProcesses = "False"\n')
        file.write('b:Ge/CheckForUnusedComponents = "False"\n')
        # Topas script complete, close file
        file.close()
        # set up environment for topas
        os.system(
            "export TOPAS_G4_DATA_DIR="
            + self.home_directory
            + "G4Data\n./bin/topas material_classifications/s1_s2_clear_run.txt"
        )

    def run_through_no_scatterer(
        self,
        distance_to_patient,
        initial_sigma_x,
        initial_sigma_y,
        initial_sigma_px,
        initial_sigma_py,
        energy=200,
        N=10000,
    ):
        self.distance_to_patient = distance_to_patient
        self.energy = energy
        # begin constructing topas text file
        # create new file with write permission
        file = open("clear_phsp/run.txt", "w")
        # set number of threads for multithreading
        file.write("i:Ts/NumberOfThreads=" + self.no_of_threads + "\n")
        # define large, square world
        file.write("d:Ge/World/HLX = 30.0 m\n")
        file.write("d:Ge/World/HLY = 30.0 m\n")
        file.write("d:Ge/World/HLZ = 30.0 m\n")
        # set world material as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')

        # define beam beginning on origin, directed in -Z direction into S1
        file.write('s:So/acc_source/Type = "Beam"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        # specify electron beam
        file.write('s:So/acc_source/BeamParticle="e-"\n')
        # set energy to 100 MeV
        file.write("d:So/acc_source/BeamEnergy= " + str(energy) + " MeV \n")
        # define initial beam distribution as flat with 1mm radius
        file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')
        file.write("d:So/acc_source/BeamPositionCutoffX = 100 mm\n")
        file.write("d:So/acc_source/BeamPositionCutoffY = 100 mm\n")
        file.write(
            "d:So/acc_source/BeamPositionSpreadX = " +
            str(initial_sigma_x) + " mm\n"
        )
        file.write(
            "d:So/acc_source/BeamPositionSpreadY = " +
            str(initial_sigma_y) + " mm\n"
        )
        # define beam as parallel
        file.write(
            "d:So/acc_source/BeamAngularSpreadX= " +
            str(initial_sigma_px) + " mrad\n"
        )
        file.write(
            "d:So/acc_source/BeamAngularSpreadY= " +
            str(initial_sigma_py) + " mrad\n"
        )
        file.write("d:So/acc_source/BeamAngularCutoffX= 100 mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffY = 100 mrad\n")
        file.write('s:So/acc_source/BeamAngularDistribution="Gaussian"\n')
        # set delta E to same as clear
        file.write("u:So/acc_source/BeamEnergySpread = 0.05\n")
        # set beam as ellipse rather than rectangle
        file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')
        # uncomment below to view Topas graphics and alter perspective etc
        # file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
        # file.write("i:Gr/ViewA/WindowSizeX      = 1024\n")
        # file.write("i:Gr/ViewA/WindowSizeY      = 768\n")
        # file.write('b:Gr/ViewA/IncludeAxes      = "True"\n')
        # file.write("d:Gr/ViewA/Theta = 45. deg\n")
        # file.write("d:Gr/ViewA/Phi = 45. deg\n")
        # file.write("u:Gr/ViewA/Zoom = 1000.\n")
        # file.write('b:Ts/PauseBeforeQuit = "True"\n')
        # file.write('b:Ts/UseQt = "True"\n')

        # initialise scorer
        file.write('s:Ge/PatientScorerSurface/Type="TsBox"\n')
        file.write('s:Ge/PatientScorerSurface/Parent = "World"\n')
        # set arbitrary material as vacuum for simplicity
        file.write('s:Ge/PatientScorerSurface/Material="Vacuum"\n')
        # set to arbitrarily large transverse size to ensure full beam coverage
        file.write("d:Ge/PatientScorerSurface/HLX = 30 m\n")
        file.write("d:Ge/PatientScorerSurface/HLY = 30 m\n")
        file.write("d:Ge/PatientScorerSurface/HLZ = 0.01 mm\n")
        # place scorer based on distance_to_patient input from end of S1 scatterer
        file.write(
            "d:Ge/PatientScorerSurface/TransZ = -" +
            str(distance_to_patient) + " mm\n"
        )

        # set surface facing beam as scoring surface
        file.write(
            's:Sc/clear_beam_no_scatterer/Surface = "PatientScorerSurface/ZPlusSurface"\n'
        )
        # initialise phase space scorer on defined surface
        file.write('s:Sc/clear_beam_no_scatterer/Quantity = "PhaseSpace"\n')
        # output phase space beam data to ASCII file
        file.write('s:Sc/clear_beam_no_scatterer/OutputType = "ASCII"\n')
        # overwrite file from previous runs
        file.write(
            's:Sc/clear_beam_no_scatterer/IfOutputFileAlreadyExists = "Overwrite"\n'
        )
        # reduce console output for repeated optimisation runs
        file.write('b:Sc/clear_beam_no_scatterer/OutputToConsole = "False"\n')

        file.write('b:Ph/ListProcesses = "False"\n')
        # turn off uneccesary overlap and component checks to decrease runtime
        file.write('b:Ge/CheckForOverlaps = "False" \n')
        file.write('b:Ge/QuitIfOverlapDetected = "False"\n')
        file.write('b:Ge/CheckForUnusedComponents = "False"')
        # close written file
        file.close()
        # point topas to Geant4 data firectory
        os.system(
            "export TOPAS_G4_DATA_DIR="
            + self.home_directory
            + "G4Data\n./bin/topas clear_phsp/run.txt"
        )
