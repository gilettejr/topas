#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 11:29:03 2023

@author: robertsoncl
"""

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis


class RFIntensityAnalyser:
    def __init__(self, RFPhspFilePath, PDGPhspFilePath):
        def getSlices(phsp, slice_width=1):
            phsp_xslice = phsp[(phsp["Y"] < slice_width)]
            phsp_xslice = phsp_xslice[(phsp_xslice["Y"] > -slice_width)]
            phsp_yslice = phsp[(phsp["X"] < slice_width)]
            phsp_yslice = phsp_yslice[(phsp_yslice["X"] > -slice_width)]
            return phsp_xslice, phsp_yslice
        self.RFPhsp = pd.read_parquet(RFPhspFilePath)
        self.PDGPhsp = pd.read_parquet(PDGPhspFilePath)
        self.getSlices = getSlices

    def saveStats(self, outfilepath):
        t = self.RFPhsp
        p = self.PDGPhsp
        tx, ty = self.getSlices(t)
        px, py = self.getSlices(p)

        t1 = t[(t["R"] < 1*np.std(p['X']))]['X']

        t2 = t[(t["R"] < 2*np.std(p['X']))]['X']

        t3 = t[(t["R"] < 3*np.std(p['X']))]['X']

        t4 = t[(t["R"] < 4*np.std(p['X']))]['X']

        t5 = t[(t["R"] < 5*np.std(p['X']))]['X']

        stdT = np.array(
            [np.std(t1), np.std(t2), np.std(t3), np.std(t4), np.std(t5)])

        kurtT = np.array([kurtosis(t1), kurtosis(
            t2), kurtosis(t3), kurtosis(t4), kurtosis(t5)])

        statsT = np.concatenate((stdT, kurtT))

        statFrame = pd.DataFrame({'r': statsT})
        statFrame.to_parquet(outfilepath)
