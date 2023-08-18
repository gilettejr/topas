#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:47:26 2023

@author: robertsoncl
"""


class pdgConverters:
    @staticmethod
    def equivalentThickness(newMaterial, shape='flat', radius=1, pradius=0.0001, energy=150, energySpread=0,
                            nParticles=1000000, oldThickness=10, oldMaterial='Aluminum', distance=1000):
