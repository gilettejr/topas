from scipy.optimize import minimize
from thickness_optimiser_utils import thickness_optimiser_utils
from gaussian_optimiser_utils import gaussian_optimiser_utils
from scipy.stats import kurtosis
from topas_ttb_runners import topas_ttb_runners
import numpy as np


def optimise_downstream_lattice(N_runs, N_particles):
    def merit(foil_params, ttb_runners):
        # retrieve variables from input array
        spot_two_sigma = foil_params[0]
        sigma = foil_params[1]
        height = foil_params[2]
        S1_to_S2 = foil_params[3]
        # create instance of class for generating and running topas script,
        # and retrieving phase space
        ttb_runners.run_through_s1(spot_two_sigma)
        ttb_runners.run_through_s2(sigma, height, S1_to_S2)
        ttb_runners.get_X_Y("S2_beam.phsp")
        # retrieve collimated beam coordinates
        target_X = ttb_runners.target_X
        target_Y = ttb_runners.target_Y
        # retrieve anti-collimated beam coordinates
        anticol_X = ttb_runners.anticol_X

        # X_width = np.sum(np.abs(beam.anticol_X))
        # Y_width = np.sum(np.abs(beam.anticol_Y))

        # exception block as kurtosis can return errors, killing optimisation
        try:
            # merit equation minimises with low kurtosis and high number of
            # electrons retained after collimation
            M = (
                +(((kurtosis(target_X) + 3) / 2 - 1) ** 2)
                + ((kurtosis(target_Y) + 3) / 2 - 1) ** 2
                + ((kurtosis(target_X + target_Y) + 3) / 2 - 1) ** 2
                + ((kurtosis(target_X - target_Y) + 3) / 2 - 1) ** 2
                + len(anticol_X) / (N_particles * 20)
            )
        # value error sets function to maximum
        except ValueError:
            M = np.inf
        return M

    # set initial merit function value to maximum
    M_min = np.inf
    bounds = [[0, 150], [0, 100], [0, 100], [0, 2500]]

    for i in range(N_runs):
        try:
            initial_guesses = [
                80,
                np.random.uniform(low=5, high=30),
                np.random.uniform(low=1, high=10),
                np.random.uniform(low=50, high=1000),
            ]
            ttb_runners = topas_ttb_runners()
            result = minimize(
                merit,
                x0=initial_guesses,
                args=(ttb_runners),
                bounds=bounds,
                method="Nelder-Mead",
            )
            M = result.fun
            x = result.x
        except ValueError:
            M = np.inf
            x = []
        print("Run " + str(i) + " complete")
        print("Value of Final Merit Function:" + str(M))
        if M < M_min:
            M_min = M
            x_min = x
    print("Best Topas solution: ")
    print(x_min)
    print("Function Result: ")
    print(M_min)

    return x_min


def optimise_downstream_lattice_vary_width(
    N_runs,
    N_particles,
    initial_params,
    set_S1_to_S2=False,
):
    def merit(foil_params, ttb_runners, spot_two_sigma, set_S1_to_S2):
        # retrieve variables from input array
        # spot_two_sigma = foil_params[0]
        sigma = foil_params[0]
        height = foil_params[1]

        # create instance of class for generating and running topas script,
        # and retrieving phase space
        ttb_runners.run_through_s1(spot_two_sigma)
        if set_S1_to_S2 is False:
            S1_to_S2 = foil_params[2]
            width = foil_params[3]
        else:
            S1_to_S2 = set_S1_to_S2
            width = foil_params[2]
            ttb_runners.run_through_s2_vary_width(
                sigma, height, S1_to_S2, width, show_shape=False
            )
        ttb_runners.get_X_Y("S2_beam.phsp")
        # retrieve collimated beam coordinates
        target_X = ttb_runners.target_X
        target_Y = ttb_runners.target_Y
        col_X = ttb_runners.col_X
        # retrieve anti-collimated beam coordinates

        # X_width = np.sum(np.abs(beam.anticol_X))
        # Y_width = np.sum(np.abs(beam.anticol_Y))

        # exception block as kurtosis can return errors, killing optimisation
        try:
            # merit equation minimises with low kurtosis and high number of
            # electrons retained after collimation
            low_flux_penalty = 0
            if len(col_X) < N_particles / 2:
                low_flux_penalty = (N_particles) / len(col_X)
            M = (
                +(((kurtosis(target_X) + 3) / 2 - 1) ** 2)
                + ((kurtosis(target_Y) + 3) / 2 - 1) ** 2
                + low_flux_penalty
            )
        # value error sets function to maximum
        except ValueError:
            M = np.inf
        return M

    # set initial merit function value to maximum
    M_min = np.inf

    bounds = [[30, np.inf], [0, np.inf], [0, np.inf]]
    if set_S1_to_S2 is False:
        bounds.append([0, np.inf])
    for i in range(N_runs):

        foil_params = initial_params[1:]
        ttb_runners = topas_ttb_runners()
        result = minimize(
            merit,
            x0=foil_params,
            args=(ttb_runners, initial_params[0], set_S1_to_S2),
            method="Nelder-Mead",
        )
        M = result.fun
        x = result.x
        if M < M_min:
            M_min = M
            x_min = x
    print("Best Topas solution: ")
    print(x_min)
    print("Function Result: ")
    print(M_min)

    return x_min
