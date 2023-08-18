import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root
import scipy.special as sc


# generate random distribution with Moliere PDF based on scatterer parameters
# theta should be array of angles, in rad
# initial energy in MeV, thickness in cm
def generate_moliere_distribution(
    theta, initial_energy, thickness, material, N_particles
):
    def moliere_pdf(theta, initial_energy, thickness, material):
        # formulae for relevant parameters required for Moliere's calculations
        def calc_expb(t_rho, Z, A):
            expb = (
                6680
                * t_rho
                * np.divide((Z + 1) * Z ** (1 / 3), A * (1 + 3.34 * alpha ** 2))
            )
            return expb

        def calc_X0(db, Z):
            return db / (0.885 * bohr_rad * Z ** (-1 / 3))

        def calc_Xa(X0):
            return np.sqrt(X0 ** 2 * (1.13 + 3.76 * alpha ** 2))

        def calc_Xc(Xa, expb):
            return np.sqrt(expb * 1.167 * Xa ** 2)

        # calculation of B has to be done numerically - not analytically solvable
        def calc_B(b):
            def fun(B, b):
                return B - np.log(B) - b

            B_guess = 2
            B_true = root(fun, x0=B_guess, args=(b))
            return B_true.x

        def calc_x(theta, Xc, B):
            return (theta ** 2) / (Xc ** 2 * B)

        def calc_f0(x):
            return 2 * np.exp(-x)

        def calc_f1(x):
            return 2 * np.exp(-x) * (x - 1) * (sc.expi(x) - np.log(x)) - 2 * (
                1 - 2 * (np.exp(-x))
            )

        # set constants
        C = 0.577215
        alpha = 1 / 137
        bohr_rad = 5.29e-11
        h = 6.626e-34
        c = 2.997e8
        e = 1.6e-19
        # dictionaries holding Z, A and densities of materials
        # densities in g/cm^3
        # feel free to add more
        Z_dict = {"Aluminum": 13, "Steel": 26, "Tantalum": 73}
        A_dict = {"Aluminum": 26.981539, "Steel": 54.9380, "Tantalum": 180.984}
        density_dict = {"Aluminum": 2.710, "Steel": 7.85, "Tantalum": 16.6}
        # retrieve parameters for specific material
        Z, A, density = Z_dict[material], A_dict[material], density_dict[material]
        # get material thickness in units of g cm^-2
        thickness_rho = thickness / 10 * density
        # calculate electron de broglie wavelength
        db = (h * c) / (e * initial_energy * 1e6 * (2 * np.pi))

        # calculate exp b parameter, dependent on material thickness and density
        expb = calc_expb(thickness_rho, Z, A)
        # calculate various characteristic angles
        X0 = calc_X0(db, Z)
        Xa = calc_Xa(X0)
        Xc = calc_Xc(Xa, expb)
        # numerically compute B pamaeter for trascendental function of b
        B = calc_B(np.log(expb))
        # translate input angle into function variable using B and Xc
        x = calc_x(theta, Xc, B)
        # calculate f0 and f1 functions
        # result is sum of f functions divided by B^-n
        f0 = calc_f0(x)
        f1 = calc_f1(x)
        return f0 + f1 / B

    pdf = moliere_pdf(theta, initial_energy, thickness, material)
    norm = [float(i) / sum(pdf) for i in pdf]
    dist = np.random.choice(theta, p=norm, size=N_particles)
    return dist


def main():
    theta_range_mrad = np.arange(-200.0001, 200.0001, step=1)
    theta_range = theta_range_mrad / 1000
    data = generate_moliere_distribution(theta_range, 100, 1, "Aluminum", 1000000)
    plt.hist(data, range=[-0.1, 0.1], bins=100)


main()
