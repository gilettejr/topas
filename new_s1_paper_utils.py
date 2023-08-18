import os
import numpy as np
import pandas as pd


class new_s1_paper_utils:  # Thickness of S1, distance from S1 to patient and Material taken as input
    def run_through_uniform_foil_from_generated_beam(
        self,
        thickness,
        material,
        distance=2500,
        energy=200,
        delta_E=0,
        beam_dist="Gaussian",
        beam_pdist="Gaussian",
        xy_rad=1,
        pxy_rad=1,
        N=10000000,
    ):
        if material == '"Nylon"':
            material = '"G4_NYLON-6-6"'
        home_directory = "/home/robertsoncl/"
        # define half_length - useful for Topas script writing
        half_length = thickness / 2
        # begin constructing topas text file
        # create new file with write permission
        file = open("material_classifications/S1_run.txt", "w")
        # set number of threads for multithreading
        file.write("i:Ts/NumberOfThreads = 6\n")
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
        file.write("s:Ge/S1/Material=" + material + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  10  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(half_length) + " mm\n")
        # set position of scatterer so that the edge is on the origin
        file.write("d:Ge/S1/TransZ = -" + str(half_length) + " mm\n")
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
        if beam_dist == "Flat":
            file.write('s:So/acc_source/BeamPositionDistribution= "Flat"\n')
            file.write("d:So/acc_source/BeamPositionCutoffX = " + str(xy_rad) + " mm\n")
            file.write("d:So/acc_source/BeamPositionCutoffY = " + str(xy_rad) + " mm\n")
        else:
            file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')
            file.write("d:So/acc_source/BeamPositionSpreadX = " + str(xy_rad) + " mm\n")
            file.write("d:So/acc_source/BeamPositionSpreadY = " + str(xy_rad) + " mm\n")
            file.write(
                "d:So/acc_source/BeamPositionCutoffX = " + str(5 * xy_rad) + " mm\n"
            )
            file.write(
                "d:So/acc_source/BeamPositionCutoffY = " + str(5 * xy_rad) + " mm\n"
            )

        if beam_pdist == "Flat":
            file.write('s:So/acc_source/BeamAngularDistribution="Flat"\n')
            # define beam as parallel
            file.write(
                "d:So/acc_source/BeamAngularCutoffX= " + str(pxy_rad) + " mrad\n"
            )
            file.write(
                "d:So/acc_source/BeamAngularCutoffY = " + str(pxy_rad) + " mrad\n"
            )

        else:
            file.write('s:So/acc_source/BeamAngularDistribution="Gaussian"\n')
            file.write(
                "d:So/acc_source/BeamAngularCutoffX= " + str(5 * pxy_rad) + " mrad\n"
            )
            file.write(
                "d:So/acc_source/BeamAngularCutoffY = " + str(5 * pxy_rad) + " mrad\n"
            )
            file.write(
                "d:So/acc_source/BeamAngularSpreadX = " + str(pxy_rad) + " mrad\n"
            )
            file.write(
                "d:So/acc_source/BeamAngularSpreadY = " + str(pxy_rad) + " mrad\n"
            )
        # set delta E
        file.write("u:So/acc_source/BeamEnergySpread = " + str(delta_E) + "\n")
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
        # place scorer based on distance input from end of S1 scatterer
        file.write(
            "d:Ge/PatientScorerSurface/TransZ = -"
            + str(half_length * 2 + distance + 0.01)
            + " mm\n"
        )

        # set surface facing beam as scoring surface
        file.write(
            's:Sc/scattered_beam/Surface = "PatientScorerSurface/ZPlusSurface"\n'
        )
        # initialise phase space scorer on defined surface
        file.write('s:Sc/scattered_beam/Quantity = "PhaseSpace"\n')
        # output phase space beam data to ASCII file
        file.write('s:Sc/scattered_beam/OutputType = "ASCII"\n')
        # overwrite file from previous runs
        file.write('s:Sc/scattered_beam/IfOutputFileAlreadyExists = "Overwrite"\n')
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
            + home_directory
            + "G4Data\n./bin/topas material_classifications/S1_run.txt"
        )

    def get_X_Y(self, path_to_file="/home/robertsoncl/topas/scattered_beam.phsp"):

        # read Topas ASCII output file
        phase_space = pd.read_csv(
            path_to_file,
            names=["X", "Y", "Z", "PX", "PY", "E", "Weight", "PDG", "9", "10"],
            delim_whitespace=True,
        )
        phase_space["X"] = phase_space["X"] * 10
        phase_space["Y"] = phase_space["Y"] * 10
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
        positron_phase_space = phase_space.drop(
            phase_space[phase_space["PDG"] != -11].index
        )
        phsp_dict = {
            "all": phase_space,
            "e": electron_phase_space,
            "y": gamma_phase_space,
            "p": positron_phase_space,
        }

        return phsp_dict
