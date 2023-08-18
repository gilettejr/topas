#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 12:19:17 2023

@author: robertsoncl
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class statPlotter:
    def plotStatsQualityRF(self, RFstatsFilePath):
        s0 = pd.read_parquet(RFstatsFilePath+str(0))
        s1 = pd.read_parquet(RFstatsFilePath+str(1))
        s2 = pd.read_parquet(RFstatsFilePath+str(2))
        s3 = pd.read_parquet(RFstatsFilePath+str(3))
        s4 = pd.read_parquet(RFstatsFilePath+str(4))

        t_sigs = np.zeros(5)

        t_uncs = np.zeros(5)

        t_kurts = np.zeros(5)

        t_kurt_uncs = np.zeros(5)

        for i in range(len(t_uncs)):
            t_sigs[i] = np.mean([s0['r'].at[i], s1['r'].at[i],
                                s2['r'].at[i], s3['r'].at[i], s4['r'].at[i]])

            t_uncs[i] = np.std([s0['r'].at[i], s1['r'].at[i],
                               s2['r'].at[i], s3['r'].at[i], s4['r'].at[i]])

        for i in range(len(t_uncs), 2*len(t_uncs)):
            t_kurts[i-5] = np.mean([s0['r'].at[i], s1['r'].at[i],
                                    s2['r'].at[i], s3['r'].at[i], s4['r'].at[i]])

            t_kurt_uncs[i-5] = np.std([s0['r'].at[i], s1['r'].at[i],
                                       s2['r'].at[i], s3['r'].at[i], s4['r'].at[i]])

        return np.array([t_sigs, t_uncs, t_kurts, t_kurt_uncs])

    def plotStatsQuality(self, statsFilePath, plot=True):
        s0 = pd.read_parquet(statsFilePath+str(0))
        s1 = pd.read_parquet(statsFilePath+str(1))
        s2 = pd.read_parquet(statsFilePath+str(2))
        s3 = pd.read_parquet(statsFilePath+str(3))
        s4 = pd.read_parquet(statsFilePath+str(4))

        t_sigs = np.zeros(5)
        m_sigs = np.zeros(5)
        p_sigs = np.zeros(5)

        t_uncs = np.zeros(5)
        m_uncs = np.zeros(5)
        p_uncs = np.zeros(5)

        t_kurts = np.zeros(5)
        m_kurts = np.zeros(5)
        p_kurts = np.zeros(5)

        t_kurt_uncs = np.zeros(5)
        m_kurt_uncs = np.zeros(5)
        p_kurt_uncs = np.zeros(5)

        for i in range(len(t_uncs)):
            t_sigs[i] = np.mean([s0['t'].at[i], s1['t'].at[i],
                                s2['t'].at[i], s3['t'].at[i], s4['t'].at[i]])
            m_sigs[i] = np.mean([s0['m'].at[i], s1['m'].at[i],
                                s2['m'].at[i], s3['m'].at[i], s4['m'].at[i]])
            p_sigs[i] = np.mean([s0['p'].at[i], s1['p'].at[i],
                                s2['p'].at[i], s3['p'].at[i], s4['p'].at[i]])

            t_uncs[i] = np.std([s0['t'].at[i], s1['t'].at[i],
                               s2['t'].at[i], s3['t'].at[i], s4['t'].at[i]])
            m_uncs[i] = np.std([s0['m'].at[i], s1['m'].at[i],
                               s2['m'].at[i], s3['m'].at[i], s4['m'].at[i]])
            p_uncs[i] = np.std([s0['p'].at[i], s1['p'].at[i],
                               s2['p'].at[i], s3['p'].at[i], s4['p'].at[i]])

        for i in range(len(t_uncs), 2*len(t_uncs)):
            t_kurts[i-5] = np.mean([s0['t'].at[i], s1['t'].at[i],
                                    s2['t'].at[i], s3['t'].at[i], s4['t'].at[i]])
            m_kurts[i-5] = np.mean([s0['m'].at[i], s1['m'].at[i],
                                    s2['m'].at[i], s3['m'].at[i], s4['m'].at[i]])
            p_kurts[i-5] = np.mean([s0['p'].at[i], s1['p'].at[i],
                                    s2['p'].at[i], s3['p'].at[i], s4['p'].at[i]])

            t_kurt_uncs[i-5] = np.std([s0['t'].at[i], s1['t'].at[i],
                                       s2['t'].at[i], s3['t'].at[i], s4['t'].at[i]])
            m_kurt_uncs[i-5] = np.std([s0['m'].at[i], s1['m'].at[i],
                                       s2['m'].at[i], s3['m'].at[i], s4['m'].at[i]])
            p_kurt_uncs[i-5] = np.std([s0['p'].at[i], s1['p'].at[i],
                                       s2['p'].at[i], s3['p'].at[i], s4['p'].at[i]])

        if plot is True:
            sig_lims = [1, 2, 3, 4, 5]
            fig, ax = plt.subplots(1, 2, figsize=(12, 6))
            ax[0].errorbar(sig_lims, t_sigs, yerr=t_uncs,
                           label='TOPAS', capsize=2, color='black')
            ax[0].errorbar(sig_lims, m_sigs, yerr=m_uncs,
                           label='Moliere', capsize=2, color='blue')
            ax[0].errorbar(sig_lims, p_sigs, yerr=p_uncs,
                           label='Gaussian', capsize=2, color='red')
            ax[0].set_ylabel('Measured Beamsize [mm]')
            ax[0].set_xlabel('Cutoff [$\sigma$ from Gaussian]')
            ax[0].legend()
            ax[1].errorbar(sig_lims, t_kurts, yerr=t_kurt_uncs,
                           label='TOPAS', capsize=2, color='black')
            ax[1].errorbar(sig_lims, m_kurts, yerr=m_kurt_uncs,
                           label='Moliere', capsize=2, color='blue')
            ax[1].errorbar(sig_lims, p_kurts, yerr=p_kurt_uncs,
                           label='Gaussian', capsize=2, color='red')
            ax[1].set_xlabel('Cutoff [$\sigma$ from Gaussian]')
            ax[1].set_ylabel('Measured Kurtosis')
            ax[1].legend()
            ax[0].grid()
            ax[1].grid()
        return np.array([[t_sigs, m_sigs, p_sigs], [t_uncs, m_uncs, p_uncs], [t_kurts, m_kurts, p_kurts], [t_kurt_uncs, m_kurt_uncs, p_kurt_uncs]])
