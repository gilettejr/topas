#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:51:43 2023

@author: robertsoncl
"""
import numpy as np
import os
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
# class of methods used for generating topas scripts for scattering foils


class partrec_gaussian_optimiser_utils():
    # set filepaths and number of threads available
    # input file is the topas script being generated and run here
    # output file is 'patient_beam'
    def __init__(
        self,
        home_directory="/home/robertsoncl/",
        no_of_threads="6",
        input_filename="partrec_test"

    ):
        # write new topas script
        file = open(home_directory + "topas/" + input_filename, "w")
        # set number of threads depending on computing power available
        file.write("i:Ts/NumberOfThreads=" + no_of_threads + "\n")
        # define arbitrarily large world
        file.write("d:Ge/World/HLX = 5.0 m\n")
        file.write("d:Ge/World/HLY = 5.0 m\n")
        file.write("d:Ge/World/HLZ = 5.0 m\n")
        # set world as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')
        file.write('sv:Ma/Peek/Components = 3 "Carbon" "Hydrogen" "Oxygen"\n')
        file.write('uv:Ma/Peek/Fractions = 3 0.76 0.08 0.16\n')
        file.write('d:Ma/Peek/Density = 1.31 g/cm3\n')
        file.write('s:Ma/Peek/DefaultColor = "lightblue"\n')
        self.home_directory = home_directory
        # set filename and file object as class attributes to retrieve later
        self.input_filename = input_filename
        self.file = file
    # define Gaussian beam in terms of phase space parameters
    # sigma, sigmap, E in mm, mrad, MeV respectively

    def generate_phsp_beam(self, sigma_x, sigma_y, sigma_px, sigma_py, E, delta_E, N):
        file = self.file
        # initialise beam
        file.write('s:So/acc_source/Type = "Beam"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        # specify proton beam
        file.write('s:So/acc_source/BeamParticle="e-"\n')
        file.write("d:So/acc_source/BeamEnergy= " + str(E) + " MeV \n")
        # define initial beam distribution from method arguments
        file.write('s:So/acc_source/BeamPositionDistribution= "Gaussian"\n')

        file.write("d:So/acc_source/BeamPositionSpreadX = " +
                   str(sigma_x) + " mm\n")
        file.write("d:So/acc_source/BeamPositionSpreadY = " +
                   str(sigma_y) + " mm\n")
        file.write("d:So/acc_source/BeamAngularSpreadX= " +
                   str(sigma_px) + " mrad\n")
        file.write("d:So/acc_source/BeamAngularSpreadY= " +
                   str(sigma_py) + " mrad\n")
        # cutoff at 5 sigma, retaining >99.9% of beam
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
        # set delta E
        file.write("u:So/acc_source/BeamEnergySpread =" + str(delta_E) + " \n")
        # set beam as ellipse rather than rectangle
        file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')

    # generate Gaussian beam from twiss parameters

    def generate_twiss_beam(self, beta_x, beta_y, emitt_x, emitt_y, alpha_x, alpha_y, E, N):
        file = self.file
        norm_emitt_x = emitt_x*(200/0.511)
        sigma_x = np.sqrt(emitt_x*beta_x)
        print(sigma_x)
        print(norm_emitt_x)
        file.write('s:So/acc_source/Type = "emittance"\n')
        # set number of particles in beam
        file.write("i:So/acc_source/NumberOfHistoriesInRun =" + str(N) + "\n")
        # required to set beam direction
        file.write('s:So/acc_source/Component = "BeamPosition"\n')
        file.write("d:Ge/BeamPosition/TransZ= 0 mm\n")
        # specify proton beam
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

        file.write("u:So/acc_source/ParticleFractionX = 0.90 \n")
        file.write("u:So/acc_source/ParticleFractionY = 0.90 \n")

    # script lines for pre scatterer
    # position refers to longitudinal placement of upstream scatterer face in mm
    # by default, positioned at origin
    def add_flat_scatterer(self, thickness, material, position=0):
        file = self.file
        file.write('s:Ge/S1/Type = "TsCylinder"\n')
        # defined from world centre
        file.write('s:Ge/S1/Parent="World"\n')
        # set material based on input argument
        file.write("s:Ge/S1/Material=" + '"' + material + '"' + "\n")

        # set radius of scatterer (make sure it is larger than beam radius)
        file.write("d:Ge/S1/Rmax =  100  mm\n")
        # solid scatterer - inner radius must be set to 0
        file.write("d:Ge/S1/Rmin= 0 mm\n")
        # define thickness of scatterer using previously define half length
        # topas works with half lengths rather than full lengths
        file.write("d:Ge/S1/HL = " + str(thickness / 2) + " mm\n")
        # set position of scatterer so that the edge is on the origin
        file.write("d:Ge/S1/TransZ = -" +
                   str(position+thickness / 2) + " mm\n")
        self.s1_geometry = thickness

    # position here refers to downstream face of scatterer (don't ask me why)
    # convolution factor = 1 for standard Gaussian scatterer
    def add_gaussian_scatterer(self, max_thickness, radius, convolution_factor, N_slices, material, position, show_shape=False, thickness_limit=False):
        file = self.file

        s2_sigma = radius/2
        # define spread of gaussian shape
        # and precision (number of slices in shape) with step argument
        # x = np.arange(-half_width, half_width, step=1)
        step = radius / (N_slices)
        x = np.arange(-(radius+step), 0, step=step)
        # construct gaussian profile from method argument sigma
        # convolution factor "warps" shape
        y = norm.pdf(x, 0, s2_sigma * convolution_factor)
        # plt.plot(x, y)
        # scale for input amplitude
        y = y - min(y)
        y_scaling_factor = max_thickness / max(y)
        y = y * y_scaling_factor
        if show_shape is True:
            plt.plot(np.append(x, -np.flip(x, 0)), np.append(y, np.flip(y)))
            plt.xlabel('r[mm]')
            plt.ylabel('h[mm]')
        # scale height and normalise base to 0
        # according to method argument max_height
        slice_radius = []
        slice_thickness = []
        slice_position = []

        # begin loop to create stack of cylinders following Gaussian shape
        for i in range(1, len(y)):
            # Don't try to create 0 height widths
            # skip relevant rows
            L = y[i] - y[i - 1]
            if thickness_limit is False or L > thickness_limit:
                HL = L / 2

                slice_radius.append(abs(x[i]))
                slice_thickness.append(L)

                # define slice name - required for Topas
                sname = "slice" + str(i)
                file.write("d:Ge/" + sname + "/HL = " + str(HL) + " mm\n")
                prev_HL = HL
                # define slice as cylinder
                file.write("s:Ge/" + sname + '/Type = "TsCylinder"\n')
                # in previously defined world
                file.write("s:Ge/" + sname + '/Parent="World"\n')
                # define material

                file.write("s:Ge/" + sname + "/Material=" +
                           '"' + material + '"' + "\n")
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
                    + "/TransZ = -"
                    + str(position - y[i - 1] - L / 2)
                    + " mm\n"
                )
                slice_position.append(position - y[i - 1] - L / 2)

            # increment to begin next slice until shape completion
            i = i + 1
        s2_geometry = pd.DataFrame(
            {'slice_radius': slice_radius, 'slice_thickness': slice_thickness, 'slice_position': slice_position})
        self.s2_geometry = s2_geometry

    def display_scatterers(self):
        s2_geometry = self.s2_geometry
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))
        ax[0].set_xlim([-25, 25])
        ax[0].set_ylim([-2, self.s1_geometry*5])
        ax[0].set_ylabel('z [mm]')
        ax[0].set_xlabel('r [mm]')
        s1_xy = [-10, 0]
        s1 = Rectangle(s1_xy, 20,
                       self.s1_geometry, fc='None', ec='k')
        ax[0].add_patch(s1)
        ax[0].annotate('S1, L='+str(self.s1_geometry) +
                       'mm', [-20, 0])

        for i in self.s2_geometry.index:
            s2_xy = np.array([-s2_geometry['slice_radius'].at[i],
                              s2_geometry['slice_position'].at[i]-s2_geometry['slice_thickness'].at[i]/2])
            s2_slice = Rectangle(s2_xy,
                                 2*s2_geometry['slice_radius'].at[i], s2_geometry['slice_thickness'].at[i], fc='None', ec='k')
            ax[1].add_patch(s2_slice)
            an_string = 'Slice '+str(i+1)+', r='+str(round(s2_geometry['slice_radius'].at[i], 3))+'mm, L='+str(
                round(s2_geometry['slice_thickness'].at[i], 3))+'mm'
            ax[1].annotate(
                an_string, s2_xy-np.array([max(s2_geometry['slice_radius'])*1.5, 0]), fontsize=9, color='k')
        ax[1].set_xlim(-max(s2_geometry['slice_radius'])*2-1,
                       max(s2_geometry['slice_radius'])*2)
        ax[1].set_ylim(min(s2_geometry['slice_position'])-1,
                       max(s2_geometry['slice_position'])+1)
        ax[1].set_ylabel('z [mm]')
        ax[1].set_xlabel('r [mm]')

    def add_patient(self, position):
        file = self.file
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
                   str(position) + " mm\n")
        # set up phase space scorer
        file.write('s:Sc/patient_beam/Quantity = "PhaseSpace"\n')
        # place at previously defined patient location
        file.write('s:Sc/patient_beam/Surface = "ScorerSurface/ZPlusSurface"\n')
        # file.write(
        #    's:Sc/patient_beam/OnlyIncludeParticlesOfGeneration = "Primary"\n')
        # output as ascii file
        file.write('s:Sc/patient_beam/OutputType = "ASCII"\n')
        file.write('s:Sc/patient_beam/IfOutputFileAlreadyExists = "Overwrite"\n')
        # reduce terminal output to improve RunTime and reduce clutter
        file.write('b:Sc/patient_beam/OutputToConsole = "False"\n')
        # set various checks to 0 to decrease RunTime
        file.write('b:Ge/CheckForOverlaps = "False" \n')
        file.write('b:Ge/QuitIfOverlapDetected = "False"\n')

        file.write('b:Ph/ListProcesses = "False"\n')
        file.write('b:Ge/CheckForUnusedComponents = "False"\n')
        self.pp = position

    # position refers to upstream face of tank
    def add_tank(self, position, depth):
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
                   str(position+depth/2) + " mm\n")
    # X bending dipole

    def add_dipole(self, strength, position, lx, ly, lz):
        file = self.file
        file.write('s:Ge/Dipole/Type="TsBox"\n')
        file.write('s:Ge/Dipole/Parent = "World"\n')
        # set arbitrary material - vacuum for simplicity
        file.write('s:Ge/Dipole/Material="Vacuum"\n')
        file.write('s:Ge/Dipole/Field="DipoleMagnet"\n')
        # set arbitrarily large surface area of scorer
        file.write("d:Ge/Dipole/HLX ="+str(lx/2)+" mm\n")
        file.write("d:Ge/Dipole/HLY ="+str(ly/2)+" mm\n")
        file.write("d:Ge/Dipole/HLZ ="+str(lz/2)+" mm\n")
        file.write("d:Ge/Dipole/TransZ=-"+position+" mm\n")
        file.write("u:Ge/Dipole/MagneticFieldDirectionX=0.0\n")
        file.write("u:Ge/Dipole/MagneticFieldDirectionY=1.0\n")
        file.write("u:Ge/Dipole/MagneticFieldDirectionZ=0.0\n")
        file.write("d:Ge/Dipole/MagneticFieldStrength="+str(strength)+" T\n")

    def run_topas(self, view_setup=False):
        file = self.file
        if view_setup is True:
            file.write('s:Gr/ViewA/Type             = "OpenGL"\n')
            file.write('b:Ts/UseQt = "True"\n')

        # Topas script complete, close file
        file.close()
        # set up environment for topas
        os.system(
            "export TOPAS_G4_DATA_DIR="
            + self.home_directory
            + "G4Data\n./bin/topas "
            + self.input_filename
        )
