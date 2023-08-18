#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 12:05:28 2023

@author: robertsoncl
"""

from statPlotter import statPlotter
from thickStatPlotter import thickStatPlotter
from EStatPlotter import EStatPlotter
from ZStatPlotter import ZStatPlotter
from radiusStatPlotter import radiusStatPlotter
from pRadiusStatPlotter import pRadiusStatPlotter
from partrecIntensityPlotter import partrecIntensityPlotter
from allIntensityPlotter import allIntensityPlotter
from allIntensityAnalyser import allIntensityAnalyser
from RFIntensityPlotter import RFIntensityPlotter
from partrecDosePlotter import partrecDosePlotter
from guiScript import guiScript
from beamScript import beamScript
from scatScript import scatScript
from magnetScript import magnetScript
from additionScript import additionScript
from scorerScript import scorerScript
from mediaScript import mediaScript
from s1DosePlotter import s1DosePlotter
from s1DoseZPlotter import s1DoseZPlotter
from s1PaperPlots import s1Generator
import cv2
import os
import matplotlib.pyplot as plt
import sys
import numpy as np
sys.path.append('/home/robertsoncl/dphil/rf-track-2.1.6/')


class genericDosePlotter:
    def plotGenericDists(fov=150, col=150, folder='/home/robertsoncl/dphil/s1Data/Dists/TOPASFULL/'):
        filestring = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(1000000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        plotterPrimary = partrecIntensityPlotter(
            folder+'Primaries/'+filestring)
        plotterPrimary.show_transverse_beam(fov, col)

        plotterSecondaryE = partrecIntensityPlotter(
            folder+'Secondaries/'+filestring)
        plotterSecondaryE.show_transverse_beam(fov, col)

        plotterSecondaryY = partrecIntensityPlotter(
            folder+'Secondaries/'+filestring, particles='y')
        plotterSecondaryY.show_transverse_beam(fov, col)

        plotterSecondaryp = partrecIntensityPlotter(
            folder+'Secondaries/'+filestring, particles='p')
        plotterSecondaryp.show_transverse_beam(fov, col)

    def plotGenericDoseSlice(depthmm, particles='total', fov=150, col=150, folder='/home/robertsoncl/dphil/s1Data/Doses/'):
        filestring = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(100000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        plotterTotal = partrecDosePlotter(
            folder+filestring+particles+'.csv', 100000, 0.167)
        plotterTotal.setCharge(10)
        plotterTotal.plotDoseSlice(depthmm)

    def plotGenericDD(folder='/home/robertsoncl/dphil/s1Data/Doses/'):
        filestring = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(1000000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        plotter = s1DosePlotter()
        # plotter.plotGenericComposition(folder+filestring)
        # plotter.plotTransverseEvolution(folder+filestring)
        plotter.plotGenericComposition(folder+filestring, ddBins=1)

    def plotEnergyDD(folder='/home/robertsoncl/dphil/s1Data/Doses/'):
        filestring = 'flat'+str(round(1, 1))+str(round(0.0001, 1))+str(round(150.0, 0)) + \
            str(round(0, 1))+str(10000)+str(round(10, 1)) + \
            'Aluminum'+str(1000)
        plotter = s1DosePlotter()
        plotter.plotEnergyScan()

    def plotThicknessDD():
        plotter = s1DosePlotter()
        plotter.plotThicknessScan()

    def plotZDD():
        plotter = s1DoseZPlotter()
        plotter.plotZScan()

    def plotEnergyTransverse():
        plotter = s1DosePlotter()
        plotter.plotTransverseEnergyEvolution()

    def plotThicknessTransverse():
        plotter = s1DosePlotter()
        plotter.plotTransverseThicknessEvolution()


class s1DoseGenerator(s1Generator):
    def splitScatteredBeam(self, folder='/home/robertsoncl/dphil/s1Data/Doses/'):
        bp = self.bp
        gp = self.gp
        gui = guiScript()
        beam = beamScript()
        scat = scatScript()
        scorer = scorerScript()
        if self.shape == 'flat':
            beam.addFlatPhspBeam(bp[0], bp[0], bp[1],
                                 bp[1], bp[2], bp[3], bp[4])
        scat.addFlatScatterer(gp[0], gp[1])
        scorer.addPhspSplitter(gp[0]+0.5)
        # origFileName = scorer.addWaterPhantomScorer(
        #    1000, 400, 400, 300, 50, 50, 50)
        gui.runTopas(list_processes=True)

    def generateSplitDoses(self, folder='/home/robertsoncl/dphil/s1Data/Doses/'):
        bp = self.bp
        gp = self.gp
        gui = guiScript()
        beam = beamScript()
        scorer = scorerScript()
        beam.importPhspBeam('Total')
        scorer.addWaterPhantomScorer(1000, 300, 300, 300, 50, 50, 50)
        gui.runTopas()
        os.system('mv DoseAtPhantom.csv ' +
                  folder+self.filestring+'total.csv')
        gui = guiScript()
        beam = beamScript()
        scorer = scorerScript()
        beam.importPhspBeam('Primary')
        scorer.addWaterPhantomScorer(1000, 300, 300, 300, 50, 50, 50)
        gui.runTopas()
        os.system('mv DoseAtPhantom.csv ' +
                  folder+self.filestring+'primary.csv')
        gui = guiScript()
        beam = beamScript()
        scorer = scorerScript()

        beam.importPhspBeam('Photon')
        scorer.addWaterPhantomScorer(1000, 300, 300, 300, 50, 50, 50)
        gui.runTopas()
        os.system('mv DoseAtPhantom.csv ' +
                  folder+self.filestring+'photon.csv')
        gui = guiScript()
        beam = beamScript()
        scorer = scorerScript()

        beam.importPhspBeam('Secondary')
        scorer.addWaterPhantomScorer(1000, 300, 300, 300, 50, 50, 50)
        gui.runTopas()
        os.system('mv DoseAtPhantom.csv ' +
                  folder+self.filestring+'secondary.csv')
        gui = guiScript()
        beam = beamScript()
        scorer = scorerScript()
        os.system('mv DoseAtPhantom.csv ' +
                  folder+self.filestring+'pp.csv')
        beam.importPhspBeam('e2')
        scorer.addWaterPhantomScorer(1000, 300, 300, 300, 50, 50, 50)
        gui.runTopas()
        os.system('mv DoseAtPhantom.csv ' +
                  folder+self.filestring+'e2.csv')
        gui = guiScript()
        beam = beamScript()
        scorer = scorerScript()

        beam.importPhspBeam('p2')
        scorer.addWaterPhantomScorer(1000, 300, 300, 300, 50, 50, 50)
        gui.runTopas()
        os.system('mv DoseAtPhantom.csv ' +
                  folder+self.filestring+'p2.csv')


def generateZscan():
    from moliere_dist import camscat
    matRange = ['Lithium', 'Carbon', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Calcium', 'Titanium', 'Chromium',
                'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Silver', 'Tantalum', 'Tungsten', 'Platinum', 'Gold', 'Lead']
    for i in matRange:
        scat = camscat()
        new_thick = scat.convertPDGMaterial(150.0, 'Aluminum', 10, i)
        gen = s1DoseGenerator('flat', 1, 0.0001, 150.0, 0,
                              100000, new_thick, i, 1000)
        gen.splitScatteredBeam()
        gen.generateSplitDoses()


def testStandard():
    gen = s1DoseGenerator('flat', 1, 0.0001, 150.0, 0,
                          1000000, 10, 'Aluminum', 1000)
    gen.splitScatteredBeam()
    gen.generateSplitDoses()

    # gen = s1DoseGenerator('flat', 1, 0.0001, 150.0, 0,
    #                      100000, 20, 'Aluminum', 1000)
    # gen.splitScatteredBeam()
    # gen.generateSplitDoses()

    # gen = s1DoseGenerator('flat', 1, 0.0001, 150.0, 0,
    #                      10000, 20, 'Aluminum', 1000)

    # gen = s1DoseGenerator('flat', 1, 0.0001, 150.0, 0,
    #                      100000, 1, 'Aluminum', 1000)
    # gen.splitScatteredBeam()
    # gen.generateSplitDoses()

    # gen = s1DoseGenerator('flat', 1, 0.0001, 150.0, 0,
    #                      100000, 25, 'Aluminum', 1000)
    # gen.splitScatteredBeam()
    # gen.generateSplitDoses()

   # gen = s1DoseGenerator('flat', 1, 0.0001, 200.0, 0,
    #                     100000, 10, 'Aluminum', 1000)
    # gen.saveTopasDoseDist()

    # gen = s1DoseGenerator('flat', 1, 0.0001, 100.0, 0,
    #                     100000, 10, 'Aluminum', 1000)
    # gen.saveTopasDoseDist()

    #gen.plotallDists(100, 100)
    # gen.savePDGDist()
    # gen.saveMolDist()
    # gen.saveTopasDist()
    # gen.saveTopasFullDists()
    #gen.plotIncludedParticles(150, 120)
    gen.plotTOPASPDGIncludedParticles(150, 120)

    # gen.plotCutoffComp()
    # gen.saveTopasDoseDist()
##
# genericDosePlotter.plotEnergyDD()
# genericDosePlotter.plotZDD()
# genericDosePlotter.plotGenericDD()
# testStandard()
generateZscan()
