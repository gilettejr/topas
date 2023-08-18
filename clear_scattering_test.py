import numpy as np
import matplotlib.pyplot as plt

"""
Created on Mon Apr 11 15:37:16 2022

@author: robertsoncl
"""
HL = np.array(
    [
        10,
        20,
        30,
        40,
        50,
    ]
)
L = HL * 2
s_positron_nos = np.array([991, 904, 513, 343, 184]) / 10000 * 100
s_electron_nos = np.array([5545, 1672, 799, 508, 297]) / 10000 * 100
s_gamma_nos = np.array([55527, 46674, 32106, 21336, 14179]) / 10000 * 100

t_positron_nos = np.array([329, 28, 2, 0.0, 0]) / 10000 * 100
t_electron_nos = (
    np.array(
        [
            364,
            47,
            10,
            1,
            0,
        ]
    )
    / 10000
    * 100
)
t_electron_nos = 100 - t_electron_nos
s_electron_nos = 100 - s_electron_nos
t_gamma_nos = (
    np.array(
        [
            28391,
            6282,
            1392,
            355,
            72,
        ]
    )
    / 10000
    * 100
)

no = 10000

plt.plot(L, s_electron_nos, label="Steel")
plt.plot(L, t_electron_nos, label="Tungsten")
plt.xlabel("Metal Thickness [mm]")
plt.ylabel("Percentage of beam electrons removed")

plt.legend()
