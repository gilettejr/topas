#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:23:00 2023

@author: robertsoncl
"""
from statPlotter import statPlotter
import numpy as np
import matplotlib.pyplot as plt


class allStatPlotter:
    def __init__(self, folder='/home/robertsoncl/s1Data/Dists/'):
        def unpackStats(statPath):
            sp = statPlotter()
            return sp.plotStatsQuality(statPath, plot=False)

        def unpackRFStats(statPath):
            sp = statPlotter()
            return sp.plotStatsQualityRF(statPath)
        self.unpackStats = unpackStats
        self.unpackRFStats = unpackRFStats
        self.folder = folder
