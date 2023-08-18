import matplotlib.pyplot as plt
import numpy as np

sim_250_values_x = np.array(
    [
        3.28,
        4.43,
        5.36,
    ]
)
sim_250_values_y = np.array(
    [
        3.47,
        4.29,
        5.23,
    ]
)
exp_250_values_x = np.array(
    [
        3.48213288380644,
        4.40334183247826,
        5.35770771968328,
    ]
)
exp_250_values_y = np.array(
    [
        3.32655344455969,
        4.46904612880883,
        5.44722153012169,
    ]
)
sim_500_values_x = np.array(
    [
        5.37476367050808,
        7.53954051522831,
        9.23185924712699,
    ]
)
sim_500_values_y = np.array(
    [
        5.28169672162713,
        7.43892045846974,
        9.28488251581304,
    ]
)
exp_500_values_x = np.array(
    [
        5.09939400658651,
        7.60038057712941,
        9.30593197769402,
    ]
)
exp_500_values_y = np.array(
    [
        5.18748267508474,
        7.39174491528637,
        9.65873514831427,
    ]
)
sim_250_values_x_short = np.array(
    [
        5.60272539970164,
        5.96499215759977,
        7.22649108358632,
    ]
)
sim_250_values_y_short = np.array(
    [
        4.65123602060837,
        6.70571582406411,
        7.8254119973857,
    ]
)
exp_250_values_x_short = np.array(
    [
        7.17518564593171,
        8.14473118785054,
        9.43389067999097,
    ]
)
exp_250_values_y_short = np.array(
    [
        4.63620221256231,
        5.92801271016638,
        7.06859343824758,
    ]
)
sim_500_values_x_short = np.array(
    [
        7.16971531664968,
        10.4604531768866,
        12.691228815454,
    ]
)
sim_500_values_y_short = np.array(
    [
        7.80997249333568,
        10.0200910439396,
        12.4266908811006,
    ]
)
exp_500_values_x_short = np.array(
    [
        9.85356861929232,
        11.4424846516935,
        13.7320379372757,
    ]
)
exp_500_values_y_short = np.array(
    [
        7.34403538768327,
        9.75747145941266,
        11.9893670548849,
    ]
)
ss = [10, 20, 30]
fig, ax = plt.subplots(2, 1)
ax[0].plot(ss, exp_250_values_x, label="CLEAR", color="black")
ax[0].plot(ss, sim_250_values_x, label="TOPAS", color="red")
ax[0].set_xlabel("Scatterer Length [mm]")
ax[0].set_ylabel("$\sigma_x$")
ax[0].set_title("200 MeV, 250mm upstream")
ax[1].plot(ss, exp_250_values_y, label="CLEAR", color="black")
ax[1].plot(ss, sim_250_values_y, label="TOPAS", color="red")
ax[1].set_xlabel("Scatterer Length [mm]")
ax[1].set_ylabel("$\sigma_y$")
ax[0].legend()
ax[1].legend()


fig, ax = plt.subplots(2, 1)
ax[0].plot(ss, exp_500_values_x, label="CLEAR", color="black")
ax[0].plot(ss, sim_500_values_x, label="TOPAS", color="red")
ax[0].set_xlabel("Scatterer Length [mm]")
ax[0].set_ylabel("$\sigma_x$")
ax[0].set_title("200 MeV, 500mm upstream")
ax[1].plot(ss, exp_500_values_y, label="CLEAR", color="black")
ax[1].plot(ss, sim_500_values_y, label="TOPAS", color="red")
ax[1].set_xlabel("Scatterer Length [mm]")
ax[1].set_ylabel("$\sigma_y$")
ax[0].legend()
ax[1].legend()
fig, ax = plt.subplots(2, 1)
ax[0].plot(ss, exp_250_values_x_short, label="CLEAR", color="black")
ax[0].plot(ss, sim_250_values_x_short, label="TOPAS", color="red")
ax[0].set_xlabel("Scatterer Length [mm]")
ax[0].set_ylabel("$\sigma_x$")
ax[0].set_title("150 MeV, 250mm upstream")
ax[1].plot(ss, exp_250_values_y_short, label="CLEAR", color="black")
ax[1].plot(ss, sim_250_values_y_short, label="TOPAS", color="red")
ax[1].set_xlabel("Scatterer Length [mm]")
ax[1].set_ylabel("$\sigma_y$")
ax[0].legend()
ax[1].legend()
fig, ax = plt.subplots(2, 1)
ax[0].plot(ss, exp_500_values_x_short, label="CLEAR", color="black")
ax[0].plot(ss, sim_500_values_x_short, label="TOPAS", color="red")
ax[0].set_xlabel("Scatterer Length [mm]")
ax[0].set_ylabel("$\sigma_x$")
ax[0].set_title("150 MeV, 500mm upstream")
ax[1].plot(ss, exp_500_values_y_short, label="CLEAR", color="black")
ax[1].plot(ss, sim_500_values_y_short, label="TOPAS", color="red")
ax[1].set_xlabel("Scatterer Length [mm]")
ax[1].set_ylabel("$\sigma_y$")
ax[0].legend()
ax[1].legend()
