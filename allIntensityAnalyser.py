#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 14:51:08 2023

@author: robertsoncl
"""
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from allIntensityReader import allIntensityReader


class allIntensityAnalyser(allIntensityReader):
    def saveStats(self, outfilepath):
        t = self.topasPhsp
        m = self.molPhsp
        p = self.pdgPhsp
        tx, ty = self.getSlices(t)
        mx, my = self.getSlices(m)
        px, py = self.getSlices(p)

        t1 = t[(t["R"] < 1*np.std(p['X']))]['X']
        m1 = m[(m["R"] < 1*np.std(p['X']))]['X']
        p1 = p[(p["R"] < 1*np.std(p['X']))]['X']

        t2 = t[(t["R"] < 2*np.std(p['X']))]['X']
        m2 = m[(m["R"] < 2*np.std(p['X']))]['X']
        p2 = p[(p["R"] < 2*np.std(p['X']))]['X']

        t3 = t[(t["R"] < 3*np.std(p['X']))]['X']
        m3 = m[(m["R"] < 3*np.std(p['X']))]['X']
        p3 = p[(p["R"] < 3*np.std(p['X']))]['X']

        t4 = t[(t["R"] < 4*np.std(p['X']))]['X']
        m4 = m[(m["R"] < 4*np.std(p['X']))]['X']
        p4 = p[(p["R"] < 4*np.std(p['X']))]['X']

        t5 = t[(t["R"] < 5*np.std(p['X']))]['X']
        m5 = m[(m["R"] < 5*np.std(p['X']))]['X']
        p5 = p[(p["R"] < 5*np.std(p['X']))]['X']

        stdT = np.array(
            [np.std(t1), np.std(t2), np.std(t3), np.std(t4), np.std(t5)])
        stdM = np.array(
            [np.std(m1), np.std(m2), np.std(m3), np.std(m4), np.std(m5)])
        stdP = np.array(
            [np.std(p1), np.std(p2), np.std(p3), np.std(p4), np.std(p5)])

        kurtT = np.array([kurtosis(t1), kurtosis(
            t2), kurtosis(t3), kurtosis(t4), kurtosis(t5)])
        kurtM = np.array([kurtosis(m1), kurtosis(
            m2), kurtosis(m3), kurtosis(m4), kurtosis(m5)])
        kurtP = np.array([kurtosis(p1), kurtosis(
            p2), kurtosis(p3), kurtosis(p4), kurtosis(p5)])

        statsT = np.concatenate((stdT, kurtT))
        statsM = np.concatenate((stdM, kurtM))
        statsP = np.concatenate((stdP, kurtP))

        statFrame = pd.DataFrame({'t': statsT, 'm': statsM, 'p': statsP})
        statFrame.to_parquet(outfilepath)
