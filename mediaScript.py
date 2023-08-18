#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:24:37 2023

@author: robertsoncl
"""
from additionScript import additionScript


class mediaScript(additionScript):
    def __init__(self):
        super(additionScript, self).__init__(home_directory="/home/robertsoncl/",
                                             input_filename="partrec_test")
        self.tankCounter = 1
        self.colCounter = 1
    # position refers to upstream face of tank

    def addTank(self, position, widthmm, heightmm, depthmm):
        file = self.openFile()
        name = 'tank'+str(self.tankCounter)
        file.write('s:Ge/'+name+'/Type="TsBox"\n')
        file.write('s:Ge/'+name+'/Parent = "World"\n')
        # set arbitrary material - vacuum for simplicity
        file.write('s:Ge/'+name+'/Material="G4_WATER"\n')
        # set arbitrarily large surface area of scorer
        file.write("d:Ge/"+name+"/HLX = " + str(widthmm / 2) + " mm\n")
        file.write("d:Ge/"+name+"/HLY = " + str(heightmm / 2) + " mm\n")
        file.write("d:Ge/"+name+"/HLZ = " + str(depthmm / 2) + " mm\n")
        file.write("d:Ge/"+name+"/TransZ=-" +
                   str(position+depthmm/2) + " mm\n")
        file.close()
        self.tankCounter = self.tankCounter+1

    def addCollimator(self, position, fullAperture, depthmm, material):
        file = self.openFile()
        name = 'col'+str(self.colCounter)
        file.write("d:Ge/"+name+"/HLZ = " + str(depthmm / 2) + " mm\n")
        file.write("d:Ge/"+name+"/TransZ=-" +
                   str(position+depthmm/2) + " mm\n")
        file.close()
        self.colCounter = self.colCounter+1
