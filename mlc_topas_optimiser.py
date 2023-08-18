from scipy.optimize import minimize, differential_evolution
from thickness_optimiser_utils import thickness_optimiser_utils
from gaussian_optimiser_utils import gaussian_optimiser_utils
from scipy.stats import kurtosis
from topas_ttb_runners import topas_ttb_runners
import numpy as np


def optimise_downstream_lattice_mlc_vary_width(
    N_runs,
    N_particles,
    N_slices,
    set_S1_to_S2=False,
    method="simplex",
):
    def merit(foil_params, ttb_runners, N_slices, set_S1_to_S2):
        # retrieve variables from input array
        # spot_two_sigma = foil_params[0]
        slice_radii = []
        for i in range(N_slices):
            slice_radii.append(foil_params[i])
        max_height = foil_params[N_slices]

        # create instance of class for generating and running topas script,
        # and retrieving phase space
        if set_S1_to_S2 is False:
            S1_to_S2 = foil_params[N_slices + 1]
            max_radius = foil_params[N_slices + 2]
        else:
            S1_to_S2 = set_S1_to_S2
            max_radius = foil_params[N_slices + 1]
        slice_radii = np.array(slice_radii)
        ttb_runners.run_through_s2_mlc(
            slice_radii, max_height, S1_to_S2, N_slices, max_radius, show_shape=False
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

    bounds = []
    # slice radius bounds - not necessary as scaled
    for i in range(N_slices):
        bounds.append([0, 1])
    # max height bounds
    bounds.append([10, 50])
    # s1 to s2 bounds if not set
    if set_S1_to_S2 is False:
        bounds.append([500, 2000])
    # max radius bounds
    bounds.append([20, 80])
    for i in range(N_runs):
        slice_radii_guesses = []
        for i in range(N_slices):
            slice_radii_guesses.append(np.random.uniform())
        initial_guesses = np.sort(np.array(slice_radii_guesses))
        initial_guesses = np.append(initial_guesses, np.random.uniform(10, 50))
        # s1 to s2 bounds if not set
        if set_S1_to_S2 is False:
            initial_guesses = np.append(initial_guesses, np.random.uniform(500, 2000))
        # max radius bounds
        initial_guesses = np.append(initial_guesses, np.random.uniform(20, 80))
        ttb_runners = topas_ttb_runners()
        print(bounds)
        if method == "simplex":
            result = minimize(
                merit,
                bounds=bounds,
                x0=initial_guesses,
                args=(ttb_runners, N_slices, set_S1_to_S2),
                method="Nelder-Mead",
            )
        elif method == "DE":
            result = differential_evolution(
                merit,
                bounds=bounds,
                x0=initial_guesses,
                args=(ttb_runners, N_slices, set_S1_to_S2),
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
