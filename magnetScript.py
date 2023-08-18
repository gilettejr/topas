#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:13:02 2023

@author: robertsoncl
"""
from additionScript import additionScript


class magnetScript(additionScript):
    def addDipole(self, strength, position, lx, ly, lz):
        file = self.openFile()
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
        file.close()
