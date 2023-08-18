from partrec_gaussian_optimiser_utils import partrec_gaussian_optimiser_utils
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
from RFIntensityAnalyser import RFIntensityAnalyser
import cv2
import os
import matplotlib.pyplot as plt
import sys
import numpy as np
sys.path.append('/home/robertsoncl/dphil/rf-track-2.1.6/')


class s1Generator:
    def __init__(self, shape, radius, pradius, P, deltaP, N, thickness_mm, material, scorerPosition):
        beamParams = (radius, pradius, P, deltaP, N)
        geoParams = (thickness_mm, material, scorerPosition)
        self.shape = shape
        self.bp = beamParams
        self.gp = geoParams
        self.filestring = shape+str(round(radius, 1))+str(round(pradius, 1))+str(round(P, 0)) + \
            str(round(deltaP, 1))+str(N)+str(round(thickness_mm, 1)) + \
            material+str(scorerPosition)

    def saveTopasFullDists(self, folder='/home/robertsoncl/dphil/s1Data/Dists/TOPASFULL/'):
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
        origFileName1 = scorer.addPhspScorer(
            gp[2], primaries=True, secondaries=False)
        gui.runTopas()
        os.system('mv '+origFileName1+'.phsp ' +
                  folder+'Primaries/'+self.filestring)

        gui = guiScript()
        beam = beamScript()
        scat = scatScript()
        scorer = scorerScript()
        if self.shape == 'flat':
            beam.addFlatPhspBeam(bp[0], bp[0], bp[1],
                                 bp[1], bp[2], bp[3], bp[4])
        scat.addFlatScatterer(gp[0], gp[1])
        origFileName1 = scorer.addPhspScorer(
            gp[2], primaries=False, secondaries=True)
        gui.runTopas()
        os.system('mv '+origFileName1+'.phsp ' +
                  folder+'Secondaries/'+self.filestring)

    def saveTopasDist(self, folder='/home/robertsoncl/dphil/s1Data/Dists/TOPAS/'):
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
        origFileName = scorer.addPhspScorer(gp[2], secondaries=False)
        gui.runTopas()
        os.system('mv '+origFileName+'.phsp ' + folder+self.filestring)

    def saveMolDist(self, folder='/home/robertsoncl/dphil/s1Data/Dists/MOL/'):
        from rf_dual_scattering import RFScript
        bp = self.bp
        gp = self.gp
        rf = RFScript()
        if self.shape == 'flat':
            rf.addFlatPhspBeam(bp[0], bp[1], bp[2], bp[3], bp[4])
        rf.addMolScat(gp[0], gp[1])
        rf.addDrift(gp[2])
        rf.savePhsp(folder+self.filestring)

    def saveRFDist(self, folder='/home/robertsoncl/dphil/s1Data/Dists/RF/'):
        from rf_dual_scattering import RFScript
        bp = self.bp
        gp = self.gp
        rf = RFScript()
        if self.shape == 'flat':
            rf.addFlatPhspBeam(bp[0], bp[1], bp[2], bp[3], bp[4])
        rf.addRFScat(gp[0], gp[1])
        rf.addDrift(gp[2])
        rf.savePhsp(folder+self.filestring)

    def savePDGDist(self, folder='/home/robertsoncl/dphil/s1Data/Dists/PDG/'):
        from rf_dual_scattering import RFScript
        bp = self.bp
        gp = self.gp
        rf = RFScript()
        if self.shape == 'flat':
            rf.addFlatPhspBeam(bp[0], bp[1], bp[2], bp[3], bp[4])
        rf.addPDGScat(gp[0], gp[1])
        rf.addDrift(gp[2])

        rf.savePhsp(folder+self.filestring)


class s1StatGenerator(s1Generator):
    def saveDistStats(self, nlabel, infolder='/home/robertsoncl/dphil/s1Data/Dists/', outfolder='/home/robertsoncl/dphil/s1Data/Stats/'):
        analyser = allIntensityAnalyser(
            infolder+'TOPAS/'+self.filestring, infolder+'MOL/'+self.filestring, infolder+'PDG/'+self.filestring)
        analyser.saveStats(outfolder+self.filestring+str(nlabel))

    def saveRFStats(self, nlabel, infolder='/home/robertsoncl/dphil/s1Data/Dists/', outfolder='/home/robertsoncl/dphil/s1Data/Stats/RF/'):
        analyser = RFIntensityAnalyser(
            infolder+'RF/'+self.filestring, infolder+'PDG/'+self.filestring)
        analyser.saveStats(outfolder+self.filestring+str(nlabel))


class s1StatPlotter:
    def plotThicknessStats(folder='/home/robertsoncl/dphil/s1Data/Stats/'):
        thicknessRange = np.linspace(1, 20, 20)
        plotter = thickStatPlotter(folder)
        plotter.plotSigmas(thicknessRange)
        plotter.plotKurtoses(thicknessRange)
        plotter.plotRFSigmas(thicknessRange)

    def plotEnergyStats(folder='/home/robertsoncl/dphil/s1Data/Stats/'):
        energyRange = np.linspace(50, 250, 21)
        plotter = EStatPlotter(folder)
        plotter.plotSigmas(energyRange)
        plotter.plotKurtoses(energyRange)
        plotter.plotRFSigmas(energyRange)

    def plotRadiusStats(folder='/home/robertsoncl/dphil/s1Data/Stats/'):
        radiusRange = np.linspace(0.0001, 4.0001, 21)
        plotter = radiusStatPlotter(folder)
        plotter.plotSigmas(radiusRange)
        plotter.plotKurtoses(radiusRange)

    def plotPRadiusStats(folder='/home/robertsoncl/dphil/s1Data/Stats/'):
        radiusRange = np.linspace(0.0001, 12.0001, 21)
        plotter = pRadiusStatPlotter(folder)
        plotter.plotSigmas(radiusRange)
        plotter.plotKurtoses(radiusRange)

    def plotZStats(folder='/home/robertsoncl/dphil/s1Data/Stats/'):
        from moliere_dist import camscat
        matRange = ['Lithium', 'Carbon', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Calcium', 'Titanium', 'Chromium',
                    'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Silver', 'Tantalum', 'Tungsten', 'Platinum', 'Gold', 'Lead']
        ZRange = [3, 6, 11, 12, 13, 14, 20, 22, 24, 26,
                  27, 28, 29, 30, 47, 73, 74, 78, 78, 82]
        thicknessRange = []
        scat = camscat()
        for i in matRange:
            thicknessRange.append(
                scat.convertPDGMaterial(150, 'Aluminum', 10, i))
        plotter = ZStatPlotter(folder)
        plotter.plotSigmas(matRange, ZRange, thicknessRange)
        plotter.plotKurtoses(matRange, ZRange, thicknessRange)


class s1Plotter(s1Generator):
    def plotTopasDist(self, fov=15, col=15, folder='/home/robertsoncl/dphil/s1Data/Dists/TOPAS/'):
        plotter = partrecIntensityPlotter(folder+self.filestring)
        plotter.show_transverse_beam(fov, col)

    def plotTopasPHSP(self, fov=15, col=15, folder='/home/robertsoncl/dphil/s1Data/Dists/TOPAS/'):
        plotter = partrecIntensityPlotter(folder+self.filestring)
        plotter.showPHSP(fov, col)

    def plotMolDist(self, fov=15, col=15, folder='/home/robertsoncl/dphil/s1Data/Dists/MOL/'):
        plotter = RFIntensityPlotter(folder+self.filestring)
        plotter.show_transverse_beam(fov, col)

    def plotPDGDist(self, fov=15, col=15, folder='/home/robertsoncl/dphil/s1Data/Dists/PDG/'):
        plotter = RFIntensityPlotter(folder+self.filestring)
        plotter.show_transverse_beam(fov, col)

    def plotallDists(self, fov=15, col=15, folder='/home/robertsoncl/dphil/s1Data/Dists/'):
        plotter = allIntensityPlotter(
            folder+'TOPAS/'+self.filestring, folder+'MOL/'+self.filestring, folder+'PDG/'+self.filestring)
        plotter.plotComparisons(xfov=fov)

    def plotGaussianIncludedParticles(self, fov=15, col=15, folder='/home/robertsoncl/dphil/s1Data/Dists/PDG/'):
        plotter = RFIntensityPlotter(folder+self.filestring)
        plotter.showProportions(fov, col)

    def plotTOPASPDGIncludedParticles(self, fov=15, col=15, folder='/home/robertsoncl/dphil/s1Data/Dists/'):
        plotter = allIntensityPlotter(
            folder+'TOPAS/'+self.filestring, folder+'MOL/'+self.filestring, folder+'PDG/'+self.filestring)
        plotter.plotTOPASPDGProportions(fov, col)

    def plotCutoffComp(self, folder='/home/robertsoncl/dphil/s1Data/Stats/'):
        plotter = statPlotter()
        plotter.plotStatsQuality(folder+self.filestring)
        # fit Gaussian to gaussian dist, assess fit, take other two fits within 3 sigma
        # assess how this changes with 2 or 3 sigma


def saveAllstats(nRepeats=5):
    gen = s1StatGenerator('flat', 1, 0.0001, 200, 0,
                          1000000, 10, 'Aluminum', 1000)
    for i in range(nRepeats):
        gen.saveTopasDist()
        gen.saveMolDist()
        gen.savePDGDist()
        gen.saveDistStats(i)


def saveRFstats(nRepeats=5):
    gen = s1StatGenerator('flat', 1, 0.0001, 150.0, 0,
                          1000000, 10, 'Aluminum', 1000)
    for i in range(nRepeats):
        gen.saveRFDist()

        gen.saveRFStats(i)


def energyScan(nRepeats=5):
    eRange = np.linspace(50, 250, 21)
    for i in eRange:
        for j in range(nRepeats):
            gen = s1StatGenerator('flat', 1, 0.0001, i, 0,
                                  1000000, 10, 'Aluminum', 1000)
            # gen.saveTopasDist()
            # gen.saveMolDist()
            # gen.savePDGDist()
            gen.saveRFDist()
            # gen.saveDistStats(j)
            gen.saveRFStats(j)


def thickScan(nRepeats=5):
    tRange = np.linspace(1, 20, 20)
    for i in tRange:
        for j in range(nRepeats):
            gen = s1StatGenerator('flat', 1, 0.0001, 150, 0,
                                  1000000, i, 'Aluminum', 1000)
            # gen.saveTopasDist()
            # gen.saveMolDist()
            # gen.savePDGDist()
            gen.saveRFDist()
            # gen.saveDistStats(j)
            gen.saveRFStats(j)


def ZScan(nRepeats=5):
    from moliere_dist import camscat
    matRange = ['Lithium', 'Carbon', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Calcium', 'Titanium', 'Chromium',
                'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Silver', 'Tantalum', 'Tungsten', 'Platinum', 'Gold', 'Lead']
    for i in matRange:
        scat = camscat()
        new_thick = scat.convertPDGMaterial(150, 'Aluminum', 10, i)
        for j in range(nRepeats):
            gen = s1StatGenerator('flat', 1, 0.0001, 150, 0,
                                  1000000, new_thick, i, 1000)
            gen.saveTopasDist()
            gen.saveMolDist()
            gen.savePDGDist()
            gen.saveDistStats(j)


def pradScan():
    rRange = np.linspace(0.5, 10, 20)
    for i in rRange:
        gen = s1Generator('flat', 1, i, 150, 0,
                          1000000, 10, 'Aluminum', 1000)
        gen.saveTopasDist()
        gen.saveMolDist()
        gen.savePDGDist()


def spreadScan():
    esRange = np.linspace(0, 2.0, 21)
    for i in esRange:
        gen = s1Generator('flat', 1, 0.0001, 150, i,
                          1000000, 10, 'Aluminum', 1000)
        # gen.saveTopasDit()
        gen.saveMolDist()
        gen.savePDGDist()


def radiusScan(nRepeats=5):
    esRange = np.linspace(0.0001, 4.0001, 21)
    for i in esRange:
        for j in range(nRepeats):
            gen = s1StatGenerator('flat', i, 0.0001, 150, 0,
                                  1000000, 10, 'Aluminum', 1000)
            gen.saveTopasDist()
            gen.saveMolDist()
            gen.savePDGDist()
            gen.saveDistStats(j)


def pradiusScan(nRepeats=5):
    esRange = np.linspace(0.0001, 12.0001, 21)
    for i in esRange:
        for j in range(nRepeats):
            gen = s1StatGenerator('flat', 1, i, 150, 0,
                                  1000000, 10, 'Aluminum', 1000)
            gen.saveTopasDist()
            gen.saveMolDist()
            gen.savePDGDist()
            gen.saveDistStats(j)


def testStandard():
    gen = s1Generator('flat', 1, 0.0001, 250.0, 0,
                      100000, 10, 'Aluminum', 1000)

    #gen.plotallDists(100, 100)
    # gen.savePDGDist()
    # gen.saveMolDist()
    # gen.saveTopasDist()
    # gen.saveTopasFullDists()
    #gen.plotIncludedParticles(150, 120)
    #gen.plotTOPASPDGIncludedParticles(150, 120)
    # gen.plotCutoffComp()
    # gen.saveTopasDoseDist()


def generateThicknessPlots():
    s1StatPlotter.plotThicknessStats()


def purge():
    print('YOU WILL LOSE ALL GENERATED DISTRIBUTIONS')
    print('Proceed? y/n')
    choice = input()
    if choice == 'y':
        #os.system('cd /home/robertsoncl/dphil/s1Data/Dists')
        os.system('rm /home/robertsoncl/dphil/s1Data/Dists/TOPAS/*')
        os.system('rm /home/robertsoncl/dphil/s1Data/Dists/PDG/*')
        os.system('rm /home/robertsoncl/dphil/s1Data/Dists/MOL/*')


# thickScan()
# energyScan()
# purge()
# thickScan()
# saveAllstats()
# testStandard()
# spreadScan()
# spreadScan()
# pradiusScan()
# energyScan()
# radiusScan()
# radiusScan()
# s1StatPlotter.plotThicknessStats()
# s1StatPlotter.plotZStats()
# s1StatPlotter.plotEnergyStats()
# s1StatPlotter.plotRadiusStats()
# s1StatPlotter.plotPRadiusStats()
# generateZPlots()
# testStandard()
#s1DosePlotter.plotGenericDists(150, 150)
#genericDosePlotter.plotGenericDoseSlice(300, particles='total')
