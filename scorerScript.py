#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:19:18 2023

@author: robertsoncl
"""
from additionScript import additionScript
from mediaScript import mediaScript


class scorerScript(mediaScript):
    def __init__(self):
        super(mediaScript, self).__init__(home_directory="/home/robertsoncl/",
                                          input_filename="partrec_test")
        self.phspScorerCounter = 1
        self.phspScorerSurfaceCounter = 1
        self.doseScorerCounter = 1
        self.doseFilmScorerCounter = 0

    # add invisible vacuum counter to retrieve phase space at chosen position
    def addPhspScorer(self, position, primaries=True, secondaries=False):
        file = self.openFile()
        scorerName = 'phspScorer'+str(self.phspScorerCounter)
        scorerSurfaceName = 'phspScorerSurface' + \
            str(self.phspScorerSurfaceCounter)
        # define scorer surface
        file.write('s:Ge/'+scorerSurfaceName+'/Type="TsBox"\n')
        file.write('s:Ge/'+scorerSurfaceName+'/Parent = "World"\n')
        # set arbitrary material - vacuum for simplicity
        file.write('s:Ge/'+scorerSurfaceName+'/Material="Vacuum"\n')

        # set arbitrarily large surface area of scorer
        file.write("d:Ge/"+scorerSurfaceName+"/HLX = 1 m\n")
        file.write("d:Ge/"+scorerSurfaceName+"/HLY = 1 m\n")
        # set small thickness for precision
        file.write("d:Ge/"+scorerSurfaceName+"/HLZ = 0.01 mm\n")
        # set at appropriate distance for consistency between variables
        file.write("d:Ge/"+scorerSurfaceName+"/TransZ = -" +
                   str(position) + " mm\n")
        # set up phase space scorer
        file.write('s:Sc/'+scorerName+'/Quantity = "PhaseSpace"\n')
        # place at previously defined patient location
        file.write('s:Sc/'+scorerName +
                   '/Surface = "'+scorerSurfaceName+'/ZPlusSurface"\n')
        # file.write(
        #    's:Sc/patient_beam/OnlyIncludeParticlesOfGeneration = "Primary"\n')
        # output as ascii file
        file.write('s:Sc/'+scorerName+'/OutputType = "ASCII"\n')
        file.write('s:Sc/'+scorerName +
                   '/IfOutputFileAlreadyExists = "Overwrite"\n')
        # reduce terminal output to improve RunTime and reduce clutter
        file.write('b:Sc/'+scorerName+'/OutputToConsole = "False"\n')
        if secondaries is not True:
            file.write('s:Sc/'+scorerName +
                       '/OnlyIncludeParticlesOfGeneration = "Primary"\n')
        if primaries is not True:
            file.write('s:Sc/'+scorerName +
                       '/OnlyIncludeParticlesOfGeneration = "Secondary"\n')

        file.close()
        self.pp = position
        self.phspScorerCounter = self.phspScorerCounter+1
        self.phspScorerSurfaceCounter = self.phspScorerSurfaceCounter+1
        self.scorerName = scorerName
        return scorerName

    def addPhspSplitter(self, position):
        file = self.openFile()
        scorerSurfaceName = 'surface'
        pname = 'psurface'
        position = position+2
        # define scorer surface
        file.write('s:Ge/'+scorerSurfaceName+'/Type="TsBox"\n')
        file.write('s:Ge/'+scorerSurfaceName+'/Parent = "World"\n')
        # set arbitrary material - vacuum for simplicity
        file.write('s:Ge/'+scorerSurfaceName+'/Material="Vacuum"\n')

        # set arbitrarily large surface area of scorer
        file.write("d:Ge/"+scorerSurfaceName+"/HLX = 1 m\n")
        file.write("d:Ge/"+scorerSurfaceName+"/HLY = 1 m\n")
        # set small thickness for precision
        file.write("d:Ge/"+scorerSurfaceName+"/HLZ = 0.01 mm\n")
        # set at appropriate distance for consistency between variables
        file.write("d:Ge/"+scorerSurfaceName+"/TransZ = -" +
                   str(position) + " mm\n")
        # set up phase space scorer
        file.write('s:Sc/Total/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/Primary/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/Secondary/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/Photon/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/e2/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/p2/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/compt/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/bremm/Quantity = "PhaseSpace"\n')
        file.write('s:Sc/pp/Quantity = "PhaseSpace"\n')
        file.write('s:Ge/psurface/Parent     = "surface"\n')
        file.write('s:Ge/psurface/Type       = "TsBox"\n')
        file.write('b:Ge/psurface/IsParallel = "TRUE"\n')
        file.write('d:Ge/psurface/HLX      = 1 m\n')
        file.write('d:Ge/psurface/HLY      = 1 m\n')
        file.write('d:Ge/psurface/HLZ      = 0.01 mm\n')

        file.write('s:Sc/Total/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/Total/OutputType = "ASCII"\n')
        file.write('s:Sc/Total/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/Total/OutputToConsole = "False"\n')

        file.write('s:Sc/Primary/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/Primary/OutputType = "ASCII"\n')
        file.write('s:Sc/Primary/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/Primary/OutputToConsole = "False"\n')
        file.write(
            'sv:Sc/Primary/OnlyIncludeIfParticleOrAncestorNotFromVolume = 1 "S1"\n')

        file.write('s:Sc/Secondary/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/Secondary/OutputType = "ASCII"\n')
        file.write('s:Sc/Secondary/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/Secondary/OutputToConsole = "False"\n')
        file.write(
            'sv:Sc/Secondary/OnlyIncludeIfParticleOrAncestorFromVolume = 1 "S1"\n')

        file.write('s:Sc/Photon/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/Photon/OutputType = "ASCII"\n')
        file.write('s:Sc/Photon/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/Photon/OutputToConsole = "True"\n')
        file.write(
            'sv:Sc/Photon/OnlyIncludeIfIncidentParticlesNamed  = 1 "gamma"\n')

        file.write('s:Sc/e2/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/e2/OutputType = "ASCII"\n')
        file.write('s:Sc/e2/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/e2/OutputToConsole = "False"\n')
        file.write(
            'sv:Sc/e2/OnlyIncludeIfParticleOrAncestorFromVolume = 1 "S1"\n')
        file.write('sv:Sc/e2/OnlyIncludeIfIncidentParticlesNamed  = 1 "e-"\n')

        file.write('s:Sc/p2/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/p2/OutputType = "ASCII"\n')
        file.write('s:Sc/p2/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/p2/OutputToConsole = "False"\n')
        file.write('sv:Sc/p2/OnlyIncludeIfIncidentParticlesNamed  = 1 "e+"\n')

        file.write('s:Sc/bremm/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/bremm/OutputType = "ASCII"\n')
        file.write('s:Sc/bremm/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/bremm/OutputToConsole = "False"\n')
        file.write(
            'sv:Sc/bremm/OnlyIncludeIfIncidentParticlesNamed  = 1 "gamma"\n')
        file.write(
            'sv:Sc/bremm/OnlyIncludeIfIncidentParticlesFromProcess = 1 "eBrem"\n')

        file.write('s:Sc/compt/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/compt/OutputType = "ASCII"\n')
        file.write('s:Sc/compt/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/compt/OutputToConsole = "False"\n')
        #file.write('sv:Sc/compt/OnlyIncludeIfIncidentParticlesNamed  = 1 "e-"\n')
        file.write(
            'sv:Sc/compt/OnlyIncludeIfIncidentParticlesFromProcess = 1 "compt"\n')

        file.write('s:Sc/pp/Surface = "surface/ZPlusSurface"\n')
        file.write('s:Sc/pp/OutputType = "ASCII"\n')
        file.write('s:Sc/pp/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('b:Sc/pp/OutputToConsole = "False"\n')
        file.write(
            'sv:Sc/pp/OnlyIncludeParticlesFromProcess = 1 "compt"\n')

    def addFilmDoseScorer(self, positionmm, widthmm=35, heightmm=40.5, depthmm=0.278, xBins=10, yBins=11, zBins=1, film='ebt3'):
        material = 'EBT3'
        file = self.openFile()
        self.doseFilmScorerCounter = self.doseFilmScorerCounter+1
        name = 'Film'+str(self.doseFilmScorerCounter)
        file.write('s:Ge/'+name+'/Type     = "TsBox"\n')
        file.write('s:Ge/'+name+'/Parent   = "World"\n')
        file.write('s:Ge/'+name+'/Material = "'+material+'"\n')
        file.write('d:Ge/'+name+'/HLX      = '+str(widthmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/HLY      = '+str(heightmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/HLZ      = '+str(depthmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/TransZ   = -' +
                   str(positionmm+depthmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/RotX     = 0. deg\n')
        file.write('d:Ge/'+name+'/RotY     = 0. deg\n')
        file.write('d:Ge/'+name+'/RotZ     = 0. deg\n')
        file.write('s:Ge/'+name+'/Color    = "green"\n')
        file.write('i:Ge/'+name+'/XBins    = '+str(xBins)+'\n')
        file.write('i:Ge/'+name+'/YBins    = '+str(yBins)+'\n')
        file.write('i:Ge/'+name+'/ZBins    = '+str(zBins)+'\n')

        file.write(
            's:Sc/DoseAt'+name+'/Quantity                  = "DoseToWater"\n')
        file.write('s:Sc/DoseAt'+name +
                   '/Component                 = "'+name+'"\n')
        file.write('s:Sc/DoseAt'+name +
                   '/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('s:Sc/DoseAt'+name+'/OutputType                = "CSV"\n')
        file.close()

    def addWaterPhantomScorer(self, positionmm, widthmm, heightmm, depthmm, xBins=50, yBins=50, zBins=50):
        file = self.openFile()

        name = 'Phantom'
        pname = 'ParallelPhantom'
        material = 'G4_WATER'
        file.write('s:Ge/'+name+'/Type     = "TsBox"\n')
        file.write('s:Ge/'+name+'/Parent   = "World"\n')
        file.write('s:Ge/'+name+'/Material = "'+material+'"\n')
        file.write('d:Ge/'+name+'/HLX      = '+str(widthmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/HLY      = '+str(heightmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/HLZ      = '+str(depthmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/TransZ   = -' +
                   str(positionmm+depthmm/2)+' mm\n')
        file.write('d:Ge/'+name+'/RotX     = 0. deg\n')
        file.write('d:Ge/'+name+'/RotY     = 0. deg\n')
        file.write('d:Ge/'+name+'/RotZ     = 0. deg\n')
        file.write('s:Ge/'+name+'/Color    = "green"\n')

        # file.write('d:Ge/'+pname+'/TransZ   = -' +
        #           str(positionmm+depthmm/2)+' mm\n')

        file.write('i:Ge/'+name+'/XBins    = '+str(xBins)+'\n')
        file.write('i:Ge/'+name+'/YBins    = '+str(yBins)+'\n')
        file.write('i:Ge/'+name+'/ZBins    = '+str(zBins)+'\n')

        file.write(
            's:Sc/DoseAt'+name+'/Quantity                  = "DoseToWater"\n')
        file.write('s:Sc/DoseAt'+name +
                   '/Component                 = "'+name+'"\n')
        file.write('s:Sc/DoseAt'+name +
                   '/IfOutputFileAlreadyExists = "Overwrite"\n')
        file.write('s:Sc/DoseAt'+name +
                   '/OutputType                = "CSV"\n')

        file.close()

    def setScorerFilter(self, generation='all', particle='all'):
        file = self.openFile()
        name = 'Film'+str(self.doseFilmScorerCounter)
        if generation != 'all':
            file.write(
                's:Sc/DoseAt'+name+'/OnlyIncludeParticlesOfGeneration = "'+generation+'"\n')
        if particle != 'all':

            file.write(
                'sv:Sc/DoseAt'+name+'/OnlyIncludeParticlesNamed = 1 "'+particle+'"\n')
        file.close()
