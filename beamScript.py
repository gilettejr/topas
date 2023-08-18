#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:46:37 2023

@author: robertsoncl
"""
from additionScript import additionScript
import numpy as np


class beamScript(additionScript):
    def addGaussianPhspBeam(self, sigma_x, sigma_y, sigma_px, sigma_py, E, delta_E, N):
        file = self.openFile()
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
        file.close()

    def addFlatPhspBeam(self, radius_x, radius_y, radius_px, radius_py, E, delta_E, N):
        file = self.openFile()
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
        file.write('s:So/acc_source/BeamPositionDistribution= "Flat"\n')

        # cutoff at 5 sigma, retaining >99.9% of beam
        file.write(
            "d:So/acc_source/BeamPositionCutoffX = " +
            str(radius_x) + " mm\n"
        )
        file.write(
            "d:So/acc_source/BeamPositionCutoffY = " +
            str(radius_y) + " mm\n"
        )
        file.write(
            "d:So/acc_source/BeamAngularCutoffX= " +
            str(radius_px) + " mrad\n"
        )
        file.write(
            "d:So/acc_source/BeamAngularCutoffY = " +
            str(radius_py) + " mrad\n"
        )
        file.write('s:So/acc_source/BeamAngularDistribution="Flat"\n')
        # set delta E
        file.write("u:So/acc_source/BeamEnergySpread =" + str(delta_E) + " \n")
        # set beam as ellipse rather than rectangle
        file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')
        file.close()

    # generate Gaussian beam from twiss parameters

    def addTwissBeam(self, beta_x, beta_y, emitt_x, emitt_y, alpha_x, alpha_y, E, N):
        file = self.openFile()
        norm_emitt_x = emitt_x*(200/0.511)
        sigma_x = np.sqrt(emitt_x*beta_x)
        self.sigma_x = sigma_x
        self.norm_emitt_x = norm_emitt_x
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

        file.write("u:So/acc_source/ParticleFractionX = 0.3935 \n")
        file.write("u:So/acc_source/ParticleFractionY = 0.3935 \n")
        file.close()

    def importPhspBeam(self, infile, position=12):
        file = self.openFile()
        file.write('s:So/acc_source/Type = "PhaseSpace"\n')
        file.write('s:So/acc_source/Component = "World"\n')
        file.write('s:So/acc_source/PhaseSpaceFileName = "'+infile+'"\n')
        file.write('d:So/acc_source/TransZ = -'+str(position)+' mm\n')
