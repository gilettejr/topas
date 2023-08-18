import numpy as np
from scipy.optimize import minimize
from thickness_optimiser_utils import thickness_optimiser_utils
from gaussian_optimiser_utils import gaussian_optimiser_utils
from scipy.stats import kurtosis

# optimise thickness of S1 based on distribution at patient
# material of S1, distance to patient defined by input arguments
# number of optimisation attempts and range of randomised input guesses also
def optimise_S1_thickness(N, distance, material, min_guess, max_guess, energy="100"):
    # core merit function to be optimised
    # thickness is only optimised argument, other two are constant
    def merit(thickness, distance, material):
        # retrieve float as np.random produces array
        length = thickness[0]
        # initalise object for running Topas simulations
        beam = thickness_optimiser_utils()
        # run simulation with S1 and patient positionfrom input arguments
        beam.run_through_uniform_foil(length, distance, material, energy=energy)
        # retrieve scorer phase space information
        beam.get_X_Y("scattered_beam.phsp")
        # retrieve 2 sigma value at patient
        two_sigma = beam.get_two_sigma()
        # define desired beam radius at patient in mm
        rad = 100
        # function with minimal result when 2 sigma of beam = desired radius
        M = (two_sigma / rad - 1) ** 2
        # return function result
        return M

    # set initial lowest function result at arbitarily large value
    M_min = np.inf
    # loop for N optimisation
    for i in range(N):
        # define initial guess within function input limits
        initial_guess = np.random.uniform(low=min_guess, high=max_guess)
        # carry out simplex minimisation of merit function
        # to produce desired beam profile at patient
        result = minimize(
            merit, x0=initial_guess, args=(distance, material), method="Nelder-Mead"
        )
        # set function result and corresponding thickness input as variables
        M = result.fun
        x = result.x
        # print run number and minimised merit value
        print("Run " + str(i) + " complete")
        print("Value of Merit Function:" + str(M))
        # if multiple runs used, only save minimal value from loop
        if M < M_min:
            M_min = M
            x_min = x[0]
    # print minimal result from multiple optimisations
    # and corresponding thickness
    print("Best solution:")
    print("Merit Value = " + str(M_min))
    print("Thickness:" + str(x_min))
    # return function result and input for parameter sweeping code
    return M_min, x_min


# function runs optimisation of S2 Gaussian foil aiming for flatness at patient
# runs N times with randomised initial guesses for simplex minimisation
def optimise_gaussian_foil(N):
    # merit function takes array of gaussian foil sigma, height, and
    # distance from S1 as input
    # returns merit value to be minimised in optimisation
    def merit(gaussian_params):
        # retrieve variables from input array
        sigma = gaussian_params[0]
        height = gaussian_params[1]
        S1_to_S2 = gaussian_params[2]
        # create instance of class for generating and running topas script,
        # and retrieving phase space
        beam = gaussian_optimiser_utils()
        # generate and run topas script from input attributes
        beam.run_through_gaussian_foil(sigma, height, S1_to_S2)
        # retrieve phase space distributions from scorer
        beam.get_X_Y("S2_beam.phsp")
        # retrieve collimated beam coordinates
        col_X = beam.col_X
        col_Y = beam.col_Y
        # retrieve anti-collimated beam coordinates
        anticol_X = beam.anticol_X
        # X_width = np.sum(np.abs(beam.anticol_X))
        # Y_width = np.sum(np.abs(beam.anticol_Y))

        # exception block as kurtosis can return errors, killing optimisation
        try:
            # merit equation minimises with low kurtosis and high number of
            # electrons retained after collimation
            M = (
                +(((kurtosis(col_X) + 3) / 2 - 1) ** 2)
                + ((kurtosis(col_Y) + 3) / 2 - 1) ** 2
                + ((kurtosis(col_X + col_Y) + 3) / 2 - 1) ** 2
                + ((kurtosis(col_X - col_Y) + 3) / 2 - 1) ** 2
                + len(anticol_X) / 10000000
                + np.ptp(col_X) / 1000
                + np.ptp(col_Y) / 1000
            )
        # value error sets function to maximum
        except ValueError:
            M = np.inf
        return M

    # set initial merit function value to maximum
    M_min = np.inf

    for i in range(N):
        initial_guesses = [
            0,
            np.random.uniform(low=5, high=15),
            np.random.uniform(low=50, high=1000),
        ]
        initial_guesses[0] = np.random.uniform(low=5, high=30)
        result = minimize(merit, x0=initial_guesses, method="Nelder-Mead")
        M = result.fun
        x = result.x
        print("Run " + str(i) + " complete")
        print("Value of Merit Function:" + str(M))
        if M < M_min:
            M_min = M
            x_min = x

    beam = gaussian_optimiser_utils()
    beam.run_through_gaussian_foil(x_min[0], x_min[1], x_min[2], save_shape=True)

    print("Best solution:")
    print("Merit Value = " + str(M_min))
    print("sigma:" + str(x_min[0]))
    print("height:" + str(x_min[1]))
    print("S1_to_S2:" + str(x_min[2]))
