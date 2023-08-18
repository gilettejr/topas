
import numpy as np
import os
from scipy.stats import norm
import matplotlib.pyplot as plt
from scipy import optimize

# class of methods used for optimising S2 shape and size with given S1


class dual_optimiser_utils():
    # generate beam
    # units in mm, mrad, MeV and use 0.05 for delta_E
    # units in mm, mrad, MeV
    # delta_E=0.01 is 1% energy spread
    def __init__(
        self,
        home_directory="/home/robertsoncl/",
        no_of_threads="6",
        filename="scattering_foil/dual_setup",
    ):
        file = open(home_directory + "topas/" + filename, "w")
        # set number of threads depending on computing power available
        file.write("i:Ts/NumberOfThreads=" + no_of_threads + "\n")
        # define arbitrarily large world
        file.write("d:Ge/World/HLX = 5.0 m\n")
        file.write("d:Ge/World/HLY = 5.0 m\n")
        file.write("d:Ge/World/HLZ = 5.0 m\n")
        # set world as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')
        self.home_directory = home_directory
        self.filename = filename
        self.file = file

    def generate_phsp_beam(self, sigma_x, sigma_y, sigma_px, sigma_py, E, delta_E, N):
        file = self.file
        self.sigma_x = sigma_x
        self.sigma_px = sigma_px
        self.E = E
        file.write('s:So/acc_source/Type = "Beam"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        # specify electron beam
        file.write('s:So/acc_source/BeamParticle="e-"\n')
        # set energy to 100 MeV
        file.write("d:So/acc_source/BeamEnergy= " + str(E) + " MeV \n")
        # define initial beam distribution as flat with 1mm radius
        file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')

        file.write("d:So/acc_source/BeamPositionSpreadX = " +
                   str(sigma_x) + " mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadY = " +
                   str(sigma_y) + " mm\n")
        file.write("d:So/acc_source/BeamAngularSpreadX= " +
                   str(sigma_px) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularSpreadY= " +
                   str(sigma_py) + " mrad\n")
        file.write(
            "d:So/acc_source/BeamPositionCutoffX = " +
            str(5 * sigma_x) + " mm\n"
        )
        file.write(
            "d:So/acc_source/BeamPositionCutoffY = " +
            str(5 * sigma_y) + " mm\n"
        )
        file.write(
            "d:So/acc_source/BeamAngularCutoffX= " +
            str(5 * sigma_px) + " mrad\n"
        )
        file.write(
            "d:So/acc_source/BeamAngularCutoffY = " +
            str(5 * sigma_py) + " mrad\n"
        )
        file.write('s:So/acc_source/BeamAngularDistribution="Gaussian"\n')
        # set delta E to 0
        file.write("u:So/acc_source/BeamEnergySpread =" + str(delta_E) + " \n")
        # set beam as ellipse rather than rectangle
        file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')
    # CLEAR: beta x, y= 40, emitt x, y=0.025um

    def generate_twiss_beam(self, beta_x, beta_y, emitt_x, emitt_y, alpha_x, alpha_y, E, N):
        file = self.file
        file.write('s:So/acc_source/Type = "emittance"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        #file.write("d:Ge/BeamPosition/RotY= 10 mrad\n")
        # specify electron beam
        file.write('s:So/acc_source/BeamParticle="e-"\n')
        # set energy to 100 MeV
        file.write("d:So/acc_source/BeamEnergy= " + str(E) + " MeV \n")
        # define initial beam distribution as flat with 1mm radius
        file.write('s:So/acc_source/Distribution= "twiss_gaussian"\n')

        file.write("u:So/acc_source/AlphaX = " + str(alpha_x) + "\n")
        file.write("u:So/acc_source/AlphaY = " + str(alpha_y) + "\n")
        file.write("d:So/acc_source/BetaX = " + str(beta_x) + " m \n")
        file.write("d:So/acc_source/BetaY = " + str(beta_y) + " m \n")
        file.write("d:So/acc_source/EmittanceX = " + str(emitt_x) + " um \n")
        file.write("d:So/acc_source/EmittanceY = " + str(emitt_y) + " um \n")

        file.write("u:So/acc_source/ParticleFractionX = 0.3935 \n")
        file.write("u:So/acc_source/ParticleFractionY = 0.3935 \n")

    # import beam profile from 'S1_beam'
    # create 3d gaussian shape from input arguments in topas
    # send beam through shape and into scorer, save phsp distribution
    # all positions defined by ENTRY

    def add_foils(
        self,
        s1_thickness,
        s2_max_height,
        s2_placement,
        patient_placement,
        s1_material,
        s2_material,
        s2_sigma="moliere",
        s2_radius=1,
        N_slices=30,
        sigma_convolution_factor=1,
        view_setup=False,
        filename="scattering_foil/dual_setup",
    ):
        self.s2_placement = s2_placement
        self.s2_max_height = s2_max_height

        # calculate required width of scatterer from Moliere approximation
        # E in MeV, X in mm, d in mm, theta in mrad
        def moliere_angle(E, X, d, init_theta=0):
            final_theta = (
                (14.1 / (E / 1000)) * np.sqrt(d / X) *
                (1 + (1 / 9) * np.log10(d / X))
            )
            return np.sqrt(init_theta ** 2 + final_theta ** 2)

        def get_s2_sigma(theta, s1_to_s2, init_sigma):
            final_sigma = s1_to_s2 / 1000 * \
                np.tan(theta / 1000) + init_sigma / 1000
            return final_sigma * 1000

        file = self.file
        X_dict = {"Aluminum": 88.97, "Nylon": 355.2, "Tantalum": 4.094}
        if s2_sigma == "moliere" or s2_sigma == "Moliere":

            X = X_dict[s1_material]
            s1_scattered_angle = moliere_angle(self.E, X, s1_thickness, 0)
            sigma_at_s2 = get_s2_sigma(s1_scattered_angle, s2_placement, 0)
            s2_sigma = sigma_at_s2
        else:
            s2_sigma = s2_sigma
        # define spread of gaussian shape
        # and precision (number of slices in shape) with step argument
        # x = np.arange(-half_width, half_width, step=1)
        x = np.arange(-s2_radius, 0, step=s2_radius / N_slices)
        if s1_material == "Nylon":
            s1_material = "G4_NYLON-6-6"
        if s2_material == "Nylon":
            s2_material = "G4_NYLON-6-6"
        # construct gaussian profile from method argument sigma
        y = norm.pdf(x, 0, s2_sigma * sigma_convolution_factor)
        # plt.plot(x, y)
        # scale for input amplitude
        y = y - min(y)
        y_scaling_factor = s2_max_height / max(y)
        y = y * y_scaling_factor
        # plt.plot(x, y)
        x = np.array(x)
        # scale height and normalise base to 0
        # according to method argument max_height
        # define distance in mm from beam source to gaussian foil
        # define half_y for ease, as Topas uses half lengths
        half_y = y / 2
        # create new text file for Topas script

        file.write('sv:Ma/Peek/Components = 3 "Carbon" "Hydrogen" "Oxygen"\n')
        file.write('uv:Ma/Peek/Fractions = 3 0.76 0.08 0.16\n')
        file.write('d:Ma/Peek/Density = 1.31 g/cm3\n')
        file.write('s:Ma/Peek/DefaultColor = "lightblue"\n')

        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/S1/Material=" + '"' + s1_material + '"' + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  10  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(s1_thickness / 2) + " mm\n")
        # set position of scatterer so that the edge is on the origin
        file.write("d:Ge/S1/TransZ = -" + str(s1_thickness / 2) + " mm\n")
        # begin setting up loop for construction of Gaussian shape
        # start at 1 to prevent errors and null slices
        i = 1
        # begin loop to create stack of cylinders following Gaussian shape
        for i in range(1, len(y)):
            # Don't try to create 0 height widths
            # skip relevant rows
            L = y[i] - y[i - 1]
            HL = L / 2

            # define slice name - required for Topas
            sname = "slice" + str(i)
            file.write("d:Ge/" + sname + "/HL = " + str(HL) + " mm\n")
            prev_HL = HL
            # define slice as cylinder
            file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
            # in previously defined world
            file.write("s:Ge/" + sname + '/Parent="World"\n')
            # define material
            if HL < 0.3:
                file.write("s:Ge/" + sname + "/Material=" +
                           '"' + 'Vacuum' + '"' + "\n")
                file.write("d:Ge/" + sname + "/Rmax = 0.001 mm\n")
            else:
                file.write("s:Ge/" + sname + "/Material=" +
                           '"' + s2_material + '"' + "\n")
            # set radius of slice from horizontal slice steps
                file.write("d:Ge/" + sname + "/Rmax = " +
                           str(abs(x[i])) + " mm\n")
            # set inner radius of slice to 0 - slice is solid, not a hoop
            file.write("d:Ge/" + sname + "/Rmin= 0 mm\n")
            #file.write("d:Ge/" + sname + "/TransX = -5 mm\n")
            # define height of slice from difference between y values
            # of points from defined Gaussian shape
            # set position to build Gaussian pointed toward beam
            # with distance beam_to_S2 from beam source to tip
            # and distance S2_to_scorer from shape base
            file.write(
                "d:Ge/"
                + sname
                + "/TransZ = -"
                + str(s2_placement - y[i - 1] - L / 2)
                + " mm\n"
            )
            # increment to begin next slice until shape completion
            i = i + 1
        # define beam beginning on origin, directed in -Z direction into S1

        # uncomment for graphics options
        if view_setup is True:
            file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
            file.write('b:Ts/UseQt = "True"\n')

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
        file.write("d:Ge/ScorerSurface/TransZ = -" +
                   str(patient_placement) + " mm\n")
        # set up phase space scorer
        file.write('s:Sc/S2_beam/Quantity = "PhaseSpace"\n')
        # place at previously defined patient location
        file.write('s:Sc/S2_beam/Surface = "ScorerSurface/ZPlusSurface"\n')
        #file.write('s:Sc/S2_beam/OnlyIncludeParticlesOfGeneration = "Primary"\n')
        # output as ascii file
        file.write('s:Sc/S2_beam/OutputType = "ASCII"\n')
        file.write('s:Sc/S2_beam/IfOutputFileAlreadyExists = "Overwrite"\n')
        # reduce terminal output to improve RunTime and reduce clutter
        file.write('b:Sc/S2_beam/OutputToConsole = "False"\n')
        file.write('b:Ph/ListProcesses = "False"\n')
        file.write('b:Ge/CheckForUnusedComponents = "False"\n')
        #file.write('sv:Ph/Default/Modules = 1 “g4em-standard_opt0”\n')
        #file.write('d:Ph/Default/CutForGamma = 0.00001 mm\n')
        #file.write('d:Ph/Default/EMRangeMin = 100. MeV\n')
        self.pp = patient_placement

    def add_tank(self, depth, view_setup=False):
        file = self.file
        file.write('s:Ge/Tank/Type="TsBox"\n')
        file.write('s:Ge/Tank/Parent = "World"\n')
        # set arbitrary material - vacuum for simplicity
        file.write('s:Ge/Tank/Material="G4_WATER"\n')
        # set arbitrarily large surface area of scorer
        file.write("d:Ge/Tank/HLX = 0.1 m\n")
        file.write("d:Ge/Tank/HLY = 0.1 m\n")
        file.write("d:Ge/Tank/HLZ = " + str(depth / 2) + " mm\n")
        file.write("d:Ge/Tank/TransZ=-" +
                   str(self.pp - depth / 2 - 0.021) + " mm\n")
        if view_setup is True:
            file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
            file.write('b:Ts/UseQt = "True"\n')

    def add_dipole(self, strength):
        file = self.file
        file.write('s:Ge/Dipole/Type="TsBox"\n')
        file.write('s:Ge/Dipole/Parent = "World"\n')
        # set arbitrary material - vacuum for simplicity
        file.write('s:Ge/Dipole/Material="Vacuum"\n')
        file.write('s:Ge/Dipole/Field="DipoleMagnet"\n')
        # set arbitrarily large surface area of scorer
        file.write("d:Ge/Dipole/HLX = 0.5 m\n")
        file.write("d:Ge/Dipole/HLY = 0.5 m\n")
        file.write("d:Ge/Dipole/HLZ = 0.5 m\n")
        file.write("d:Ge/Dipole/TransZ=-1100 mm\n")
        file.write("u:Ge/Dipole/MagneticFieldDirectionX=0.0\n")
        file.write("u:Ge/Dipole/MagneticFieldDirectionY=1.0\n")
        file.write("u:Ge/Dipole/MagneticFieldDirectionZ=0.0\n")
        file.write("d:Ge/Dipole/MagneticFieldStrength="+str(strength)+" T\n")

    def add_stem(self, position_up_from_base, stem_material='G4_NYLON-6-6'):
        file = self.file
        s2_placement = self.s2_placement
        s2_max_height = self.s2_max_height
        file.write('s:Ge/stem/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/stem/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/stem/Material=" + '"' + stem_material + '"' + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/stem/Rmax =  0.25  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/stem/Rmin= 0 mm\n")
        file.write("d:Ge/stem/RotX= 90 deg\n")
        # define thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/stem/HL = 5 cm\n")
        # set position of scatterer so that the edge is on the origin
        # file.write("d:Ge/stem/TransZ = -" +
        #           str(s2_placement-position_up_from_base) + " mm\n")
        file.write("d:Ge/stem/TransZ = -497.92 mm\n")

        file.write("d:Ge/stem/TransY = "+str(5+2.4E-1)+"  cm\n")

    def add_col(self, col_material='Tantalum'):
        file = self.file
        s2_placement = self.s2_placement
        s2_max_height = self.s2_max_height
        file.write('s:Ge/stem/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/stem/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/stem/Material=" + '"' + col_material + '"' + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/stem/Rmax =  5  cm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/stem/Rmin= 3.600 mm\n")
        # define thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/stem/HL = 0.1 cm\n")
        # set position of scatterer so that the edge is on the origin
        file.write("d:Ge/stem/TransZ = -" + str(499.38435+1) + " mm\n")

    def topas_run(self):
        file = self.file
        # Topas script complete, close file
        file.close()
        # set up environment for topas
        os.system(
            "export TOPAS_G4_DATA_DIR="
            + self.home_directory
            + "G4Data\n./bin/topas "
            + self.filename
        )
