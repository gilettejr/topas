import pandas as pd
import numpy as np
import os
import warnings
import matplotlib.pyplot as plt
from automation_utils import automation_utils
from astropy.modeling import models, fitting


# class of methods for optimising and analysing S1 characteristics on beam
class thickness_optimiser_utils(automation_utils):

    # create topas script with uniform beam
    # beam immediately enters S1 scatterer
    # Thickness of S1, distance from S1 to patient and Material taken as input
    def run_through_uniform_foil_from_generated_beam(
        self, thickness, distance, material, N=10000, energy=100, score_at_S1=False
    ):
        # set inputs as class attributes, required for further analysis
        self.thickness = thickness
        self.distance = distance
        self.material = material
        self.energy = energy
        # define half_length - useful for Topas script writing
        half_length = thickness / 2
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
        file.write('s:Ge/World/Material = "Vacuum"\n')
        # begin defining S1 scatterer
        # cylinder used, for rotational symmetry
        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/S1/Material=" + material + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  4  mm\n")
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
        file.write('s:So/acc_source/BeamPositionDistribution= "Flat"\n')
        file.write("d:So/acc_source/BeamPositionCutoffX = 1 mm\n")
        file.write("d:So/acc_source/BeamPositionCutoffY = 1 mm\n")
        # define beam as parallel
        file.write("d:So/acc_source/BeamAngularCutoffX= 1 mrad\n")
        file.write("d:So/acc_source/BeamAngularCutoffY = 1 mrad\n")
        file.write('s:So/acc_source/BeamAngularDistribution="Flat"\n')
        # set delta E to 0
        file.write("u:So/acc_source/BeamEnergySpread = 0.25\n")
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
        # reduce console output for repeated optimisation runs
        file.write('b:Sc/scattered_beam/OutputToConsole = "False"\n')
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
            # place scorer based on distance input from end of S1 scatterer
            file.write(
                "d:Ge/S1ScorerSurface/TransZ = -" + str(half_length * 2 + 1) + " mm\n"
            )

            # set surface facing beam as scoring surface
            file.write('s:Sc/S1beam/Surface = "S1ScorerSurface/ZPlusSurface"\n')
            # initialise phase space scorer on defined surface
            file.write('s:Sc/S1beam/Quantity = "PhaseSpace"\n')
            # output phase space beam data to ASCII file
            file.write('s:Sc/S1beam/OutputType = "ASCII"\n')
            # overwrite file from previous runs
            file.write('s:Sc/S1beam/IfOutputFileAlreadyExists = "Overwrite"\n')
            # reduce console output for repeated optimisation runs
            file.write('b:Sc/S1beam/OutputToConsole = "False"\n')

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

    def run_through_uniform_foil_from_generated_beam_kapton(
        self, thickness, distance, material, N=10000, energy=200
    ):
        # set inputs as class attributes, required for further analysis
        self.thickness = thickness
        self.distance = distance
        self.material = material
        self.energy = energy
        # define half_length - useful for Topas script writing
        half_length = thickness / 2
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
        file.write('s:Ge/World/Material = "Vacuum"\n')
        # begin defining S1 scatterer
        # cylinder used, for rotational symmetry
        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/S1/Material=" + material + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  2  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(half_length) + " mm\n")
        # set position of scatterer so that the edge is on the origin
        file.write("d:Ge/S1/TransZ = -" + str(half_length) + " mm\n")
        # define beam beginning on origin, directed in -Z direction into S1
        file.write('s:So/acc_source/Type = "Emittance"\n')
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
        file.write('s:So/acc_source/Distribution= "twiss_gaussian"\n')
        file.write("u:So/acc_source/AlphaX = 0\n")
        file.write("d:So/acc_source/BetaX = 4 m\n")
        file.write("d:So/acc_source/EmittanceX = 10 mm\n")
        # define beam as parallel
        file.write("u:So/acc_source/AlphaY = 0\n")
        file.write("d:So/acc_source/BetaY = 4 m\n")
        file.write("d:So/acc_source/EmittanceY = 10 mm\n")
        file.write("u:So/acc_source/ParticleFractionX = 0.9 \n")
        file.write("u:So/acc_source/ParticleFractionY = 0.9 \n")

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
        # reduce console output for repeated optimisation runs
        file.write('b:Sc/scattered_beam/OutputToConsole = "False"\n')

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

    def run_through_uniform_foil_from_imported_beam_kapton(
        self,
        thickness,
        distance,
        material,
        input_filename,
        score_at_S1=True,
    ):
        # set inputs as class attributes, required for further analysis
        self.thickness = thickness
        self.distance = distance
        self.material = material
        # define half_length - useful for Topas script writing
        half_length = thickness / 2
        # begin constructing topas text file
        # create new file with write permission
        file = open(self.home_directory + "topas/ttb_run_data/S1_topas_script.txt", "w")
        # set number of threads for multithreading
        file.write("i:Ts/NumberOfThreads=" + self.no_of_threads + "\n")
        # define large, square world
        file.write("d:Ge/World/HLX = 30.0 m\n")
        file.write("d:Ge/World/HLY = 30.0 m\n")
        file.write("d:Ge/World/HLZ = 30.0 m\n")
        # set world material as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')
        # import beam from phase space file
        file.write('s:So/S1_source/Type = "PhaseSpace"\n')
        file.write('s:So/S1_source/Component = "World"\n')
        # import from previously run S1beam file to get correct phase space
        file.write("s:So/S1_source/PhaseSpaceFileName = " + input_filename + "\n")
        file.write('b:So/S1_source/PhaseSpacePreCheck = "False"\n')
        file.write("u:So/S1_source/PhaseSpaceScaleZPosBy = 0.\n")
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
        file.write("d:Ge/S1/TransZ = -" + str(half_length + 1) + " mm\n")
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

        if score_at_S1 is True:
            # initialise scorer
            file.write('s:Ge/S1ScorerSurface/Type="TsBox"\n')
            file.write('s:Ge/S1ScorerSurface/Parent = "World"\n')
            # set arbitrary material as vacuum for simplicity
            file.write('s:Ge/S1ScorerSurface/Material="Vacuum"\n')
            # set to arbitrarily large transverse size to ensure full beam coverage
            file.write("d:Ge/S1ScorerSurface/HLX = 0.3 m\n")
            file.write("d:Ge/S1ScorerSurface/HLY = 0.3 m\n")
            file.write("d:Ge/S1ScorerSurface/HLZ = 0.00001 mm\n")
            # place scorer based on distance input from end of S1 scatterer
            file.write(
                "d:Ge/S1ScorerSurface/TransZ = -"
                + str(half_length * 2 + 1 + 0.0001)
                + " mm\n"
            )

            # set surface facing beam as scoring surface
            file.write(
                's:Sc/beam_downstream_of_s1/Surface = "S1ScorerSurface/ZPlusSurface"\n'
            )

            # initialise phase space scorer on defined surface
            file.write('s:Sc/beam_downstream_of_s1/Quantity = "PhaseSpace"\n')
            # output phase space beam data to ASCII file
            file.write('s:Sc/beam_downstream_of_s1/OutputType = "ASCII"\n')
            # overwrite file from previous runs
            file.write(
                's:Sc/beam_downstream_of_s1/IfOutputFileAlreadyExists = "Overwrite"\n'
            )
            # reduce console output for repeated optimisation runs
            file.write('b:Sc/beam_downstream_of_s1/OutputToConsole = "False"\n')

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
            + str(half_length * 2 + distance)
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
        # reduce console output for repeated optimisation runs
        file.write('b:Sc/scattered_beam/OutputToConsole = "False"\n')
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
            + "G4Data\n./bin/topas ttb_run_data/S1_topas_script.txt"
        )

    # retrieve two sigma value of gaussian phase space data
    def get_two_sigma(self, max_radius=200, bins=500):
        # retrieve X data (rotationally symmetric, Y not required)
        X = self.X
        # initiate Astropy Gaussian model with arbitrary initial values
        # construct density histogram from X data
        for i in X.index:
            if np.abs(X.at[i]) > max_radius:
                X.at[i] = np.nan
        X = X.dropna()
        hist, bin_edges = np.histogram(X, bins=bins)
        # define X coordinates as bin centres rather than edges
        bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
        # initialise LSQ fitter (fast, more complex fitter not necessary)
        fit_g = fitting.LevMarLSQFitter()
        g_init = models.Gaussian1D()
        # carry out gaussian fit over data
        g = fit_g(g_init, bin_centres, hist)
        plt.figure()
        plt.plot(bin_centres, g(bin_centres))
        plt.plot(bin_centres, hist)
        # return value of 2 * sigma
        self.two_sigma = g.stddev.value

        return 2 * g.stddev.value

    # create topas script with uniform beam
    # beam immediately enters S1 scatterer
    # Thickness of S1, distance from S1 to patient and Material taken as input
    def run_through_uniform_foil_for_paper(
        self,
        thickness,
        material,
        title_material,
        N,
        energy,
        energy_spread,
        radius,
        angular_radius,
        gauss,
    ):
        # set inputs as class attributes, required for further analysis
        self.thickness = thickness
        self.material = material
        self.energy = energy
        title = (
            title_material
            + "_"
            + str(energy)
            + "MeV_"
            + str(thickness)
            + "mm_"
            + str(energy_spread)
            + "%_"
            + str(radius)
            + "mm_"
            + str(angular_radius)
            + "mrad_"
            + str(gauss)
        )
        # define half_length - useful for Topas script writing
        half_length = thickness / 2
        # begin constructing topas text file
        # create new file with write permission
        file = open("s1_paper_data/run_script.txt", "w")
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
        file.write("s:Ge/S1/Material=" + material + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  50  mm\n")
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
        if gauss is True:

            # define initial beam distribution as flat with radius
            file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')
            file.write('s:So/acc_source/BeamAngularDistribution="Gaussian"\n')
            file.write("d:So/acc_source/BeamPositionSpreadX = " + str(radius) + " mm\n")
            file.write("d:So/acc_source/BeamPositionSpreadY = " + str(radius) + " mm\n")
            # define beam as parallel
            file.write(
                "d:So/acc_source/BeamAngularSpreadX= " + str(angular_radius) + " mrad\n"
            )
            file.write(
                "d:So/acc_source/BeamAngularSpreadY = "
                + str(angular_radius)
                + " mrad\n"
            )
            file.write("d:So/acc_source/BeamPositionCutoffX = 20 mm\n")
            file.write("d:So/acc_source/BeamPositionCutoffY = 20 mm\n")
            # define beam as parallel
            file.write("d:So/acc_source/BeamAngularCutoffX= 20 mrad\n")
            file.write("d:So/acc_source/BeamAngularCutoffY = 20 mrad\n")

        else:
            file.write('s:So/acc_source/BeamPositionDistribution= "Flat"\n')
            file.write('s:So/acc_source/BeamAngularDistribution="Flat"\n')
            file.write("d:So/acc_source/BeamPositionCutoffX = " + str(radius) + " mm\n")
            file.write("d:So/acc_source/BeamPositionCutoffY = " + str(radius) + " mm\n")
            # define beam as parallel
            file.write(
                "d:So/acc_source/BeamAngularCutoffX= " + str(angular_radius) + " mrad\n"
            )
            file.write(
                "d:So/acc_source/BeamAngularCutoffY = "
                + str(angular_radius)
                + " mrad\n"
            )
        # set delta E to 0
        file.write("u:So/acc_source/BeamEnergySpread = " + str(energy_spread) + "\n")
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
        file.write("d:Ge/PatientScorerSurface/TransZ = -" + str(2500) + " mm\n")

        # set surface facing beam as scoring surface
        file.write("s:Sc/" + title + '/Surface = "PatientScorerSurface/ZPlusSurface"\n')
        # initialise phase space scorer on defined surface
        file.write("s:Sc/" + title + '/Quantity = "PhaseSpace"\n')
        # output phase space beam data to ASCII file
        file.write("s:Sc/" + title + '/OutputType = "ASCII"\n')
        # overwrite file from previous runs
        file.write("s:Sc/" + title + '/IfOutputFileAlreadyExists = "Overwrite"\n')
        # reduce console output for repeated optimisation runs
        file.write("b:Sc/" + title + '/OutputToConsole = "False"\n')

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
            + "G4Data\n./bin/topas s1_paper_data/run_script.txt"
        )

    # display database of Topas run data in parquet format from filename input
    def show_database(
        self,
        filename="material_classifications/electron_results",
        material=False,
        distance=False,
        energy=False,
    ):
        # retrieve data into Pandas DataFrame format
        database = pd.read_parquet(filename)
        if material != "all" and distance != "all" and energy != "all":
            for i in database.index:
                if (
                    database["Material"].at[i] == material
                    and database["Distance"].at[i] == distance
                    and database["Initial_Beam_E"].at[i] == energy
                ):
                    print(database.loc[i])
        pd.set_option("display.max_columns", database.shape[1] + 1)
        print(database)

    # permanently delete rows from data file from filename and row input
    # takes array of integers corresponding to rows to be deleted as input
    def delete_database_rows(
        self, lines, filename="material_classifications/electron_results"
    ):
        # retrieve data into Pandas DataFrame format
        database = pd.read_parquet(filename)
        # loop through and delete rows i from lines list input
        for i in lines:
            database.loc[i] = np.nan
        # purge deleted lines
        database = database.dropna()
        # reset index
        database = database.reset_index(drop=True)
        # save purged DataFrame to original filename
        database.to_parquet(filename)

    # save data from topas run to parquet file
    def save_to_database(self, filename):
        # removes energy values for widely scattered particles
        # prevents tails of beam from skewing mean energy results
        def collimate(X, Y, E):
            # loop through data
            for i in X.index:
                # cut energy values with X or Y coords beyond 0.1m
                if np.abs(X[i]) > 100 or np.abs(Y[i]) > 100:
                    E[i] = np.nan
            # purge nan values for consistency
            E = E.dropna()
            return E

        # try importing existing database to update with new values
        try:
            database = pd.read_parquet(filename)
        # create new dataframe if file does not already exist
        except FileNotFoundError:
            # define databame with empty columns
            database = pd.DataFrame(
                {
                    "Material": [],
                    "Thickness": [],
                    "Distance": [],
                    "Initial_Beam_E": [],
                    "Mean_E_Collimated": [],
                    "e_number": [],
                    "Mean_gamma_E_collimated": [],
                    "gamma_number": [],
                }
            )
        # collimate electron and gamma energy values
        E = collimate(self.X, self.Y, self.E)
        gamma_E = collimate(self.gamma_X, self.gamma_Y, self.gamma_E)
        # compute mean energy of collimated particles
        try:
            mean_E_col = np.average(E)
        except ZeroDivisionError:
            mean_E_col = 0
        try:
            mean_gamma_E_col = np.average(gamma_E)
        except ZeroDivisionError:
            mean_gamma_E_col = 0
        # count number of electrons and photons for dataframe
        e_number = len(self.X.dropna())
        gamma_number = len(self.gamma_X.dropna())
        # only add run data to database if run has been succesful
        # average electon E of below 70 implies poor scattering solution
        if mean_E_col / self.energy > 0.7:
            # construct dataframe of new data
            new_entries = pd.DataFrame(
                {
                    "Material": [self.material],
                    "Thickness": [self.thickness],
                    "Distance": [self.distance],
                    "Initial_Beam_E": [self.energy],
                    "Mean_E_Collimated": [mean_E_col],
                    "e_number": [e_number],
                    "Mean_gamma_E_collimated": [mean_gamma_E_col],
                    "gamma_number": [gamma_number],
                }
            )
        else:
            new_entries = pd.DataFrame(
                {
                    "Material": [self.material],
                    "Thickness": [self.thickness],
                    "Distance": [self.distance],
                    "Initial_Beam_E": [self.energy],
                    "Mean_E_Collimated": [mean_E_col],
                    "e_number": [e_number],
                    "Mean_gamma_E_collimated": [mean_gamma_E_col],
                    "gamma_number": [gamma_number],
                }
            )
            warnings.warn("Bad solutions for Optimisation")

            # update original database/fill new database with column data
            updated_database = pd.concat([database, new_entries])
            # rest indices of dataframe for consistency
            updated_database = updated_database.reset_index(drop=True)
            # resave as binary parquet
            updated_database.to_parquet(filename)
