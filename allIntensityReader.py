#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 14:48:53 2023

@author: robertsoncl
"""
import pandas as pd
import matplotlib.pyplot as plt
from partrecIntensityPlotter import partrecIntensityPlotter


class allIntensityReader(partrecIntensityPlotter):
    def __init__(self, topasPhspFilePath, molPhspFilePath, pdgPhspFilePath):
        super(allIntensityReader, self).__init__(topasPhspFilePath)
        self.topasPhsp = self.phsp
        self.molPhsp = pd.read_parquet(molPhspFilePath)
        self.pdgPhsp = pd.read_parquet(pdgPhspFilePath)
