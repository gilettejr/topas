import matplotlib.pyplot as plt
import numpy as np


def part1():

    chargesBefore = np.array(
        [0.99, 2.02, 2.91, 4.01, 5.01, 6.16, 7.08, 8.04, 10.03, 12.05])
    chargesAfter = np.array(
        [0.36, 0.75, 1.07, 1.49, 1.83, 2.23, 2.61, 2.96, 3.7, 4.45])
    doses = np.array([1.22, 1.69, 2.17, 3.14, 3.44, 4.19, 4.83, 5.35, 6.87, 7.63
                      ])
    stds = np.array([0.12, 0.11, 0.13, 0.18, 0.15,
                    0.18, 0.24, 0.25, 0.31, 0.37])

    dosesWholex = np.array([1.1728245805319115, 1.6828367030837108, 2.161283043066141, 3.207777939026496,
                           3.40517255050564, 4.181869511361658, 4.826122121504748, 5.366395948120173, 6.724260315262152, 7.627829685805303])
    dosesWholey = np.array([1.1351933772782805, 1.6198088909892359, 2.077719137113431, 3.0933343945416105,
                           3.2308975382176417, 4.006885509280582, 4.612399794145871, 5.0692644097469595, 6.4067037108681735, 7.3640720172356895])
    stdsWholex = np.array([0.13422837420769546, 0.19286178303143472, 0.267378867476694, 0.3046719845196898,
                          0.3863907642762517, 0.5281117455305575, 0.5235646081196993, 0.6211502636677697,
                          0.9555555713071523, 0.9680283005692867])
    stdsWholey = np.array([0.1813165633975305, 0.23064849808025034, 0.2809815247617575, 0.4375291143146404,
                          0.5557699686616459, 0.6688516370907995, 0.7186063002113792, 0.7315437064325092, 1.1666340430487976, 1.1061442274375417])

    print(np.mean(stds/doses))
    print(np.mean(chargesAfter/chargesBefore))
    print(np.std(chargesAfter/chargesBefore))
    print(np.mean(doses/chargesAfter))
    print(np.std(doses/chargesAfter))

    fig, ax = plt.subplots(2, 1, figsize=[8, 7])
    ax[0].set_xlabel('Accumulated Charge Before Collimation [nC]')
    ax[0].set_ylabel('Dose [Gy]')
    ax[0].errorbar(chargesBefore, doses, yerr=stds, capsize=2, color='k')
    ax[0].grid(True)
    ax[1].set_xlabel('Accumulated Charge Before Collimation [nC]')
    ax[1].set_ylabel('Accumalted Charge After Collimation [nC]')
    ax[1].plot(chargesBefore, chargesAfter, color='k')

    fig, ax = plt.subplots(2, 1, figsize=[8, 7])
    ax[0].set_xlabel('Accumulated Charge Before Collimation [nC]')
    ax[0].set_ylabel('Mean Dose Across X Profile [Gy]')
    ax[0].errorbar(chargesBefore, dosesWholex,
                   yerr=stdsWholex, capsize=2, color='k')
    ax[1].set_xlabel('Accumulated Charge Before Collimation [nC]')
    ax[1].set_ylabel('Mean Dose Across Y Profile [Gy]')
    ax[1].errorbar(chargesBefore, dosesWholey,
                   yerr=stdsWholey, capsize=2, color='k')
    ax[0].grid(True)
    ax[1].grid(True)

    fig, ax = plt.subplots(1, 1, figsize=[8, 8])
    ax.set_xlabel('Accumulated Charge After Collimation [nC]')
    ax.set_ylabel('Dose [Gy]')
    ax.errorbar(chargesAfter, doses,
                yerr=stds, capsize=2, color='k')
    ax.grid(True)


part1()
