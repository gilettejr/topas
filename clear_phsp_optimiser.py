from astropy.modeling import models, fitting
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import kurtosis
from clear_experiment_utils import clear_experiment_utils


def optimise_s2_for_clear(
    runs, s1_thickness, sigma_x, sigma_y, sigma_px, sigma_py, N_particles=10000
):
    def merit(
        gaussian_params,
        utils_object,
        s1_thickness,
        sigma_x,
        sigma_y,
        sigma_px,
        sigma_py,
        N_particles,
    ):
        sigma = gaussian_params[0]
        max_height = gaussian_params[1]
        shape_radius = gaussian_params[2]
        ceu = utils_object
        ceu.run_through_s1_and_s2_clear(
            s1_thickness,
            500,
            sigma,
            max_height,
            shape_radius,
            sigma_x=sigma_x,
            sigma_y=sigma_y,
            sigma_px=sigma_px,
            sigma_py=sigma_py,
            N=N_particles,
            s1_to_s2=250,
        )
        ceu.get_X_Y("S2_beam.phsp", true_col_rad=5.0, target_col_rad=5.0)
        X = ceu.X
        Y = ceu.Y

        anticol_X = ceu.anticol_X

        M = (
            (((kurtosis(X) + 3) / 2 - 1) ** 2)
            + (((kurtosis(Y) + 3) / 2 - 1) ** 2)
            + (((kurtosis(X + Y) + 3) / 2 - 1) ** 2)
            + (((kurtosis(X - Y) + 3) / 2 - 1) ** 2)
            + len(anticol_X) / 100000
        )
        return M

    bounds = [[0, 50], [0, 300], [1, 50]]
    initial_guesses = [
        np.random.uniform(low=0, high=100),
        np.random.uniform(low=0, high=100),
        np.random.uniform(low=1, high=30),
    ]
    ceu = clear_experiment_utils()
    M_min = np.inf
    for i in range(runs):

        result = minimize(
            merit,
            x0=initial_guesses,
            args=(ceu, s1_thickness, sigma_x, sigma_y,
                  sigma_px, sigma_py, N_particles),
            method="Nelder-Mead",
        )
        M = result.fun
        x = result.x
        if M < M_min:
            x_min = x
            M_min = M
    print("Best Topas solution: ")
    print(x_min)
    print("Function Result: ")
    print(M_min)


def generate_elliptical_beam(true_sigmas, N, clear_sigma_x, clear_sigma_y):
    a = true_sigmas[0]
    b = true_sigmas[1]
    # define random number generator for beam construction
    rng = np.random.default_rng()
    rang = rng.normal
    ran = rng.uniform
    # empty lists to hold beam parameters
    # x,y in mm, px,py in mrad
    x = []
    y = []

    # fill lists with beam parameters for uniform circular beam
    # and p radius PR
    for i in range(int(N)):
        R = np.sqrt(np.abs(rang()))

        phi = 2 * np.pi * np.abs(ran())

        x_i = R * np.cos(phi)

        y_i = R * np.sin(phi)
        x_i = x_i * a
        y_i = y_i * b

        x.append(x_i)
        y.append(y_i)

    # plt.scatter(x, y, s=1)
    # plt.figure()
    hist_x, bin_edges_x = np.histogram(x, bins=100)

    # define X coordinates as bin centres rather than edges
    bin_centres_x = (bin_edges_x[:-1] + bin_edges_x[1:]) / 2
    hist_y, bin_edges_y = np.histogram(y, bins=100)
    # define y coordinates as bin centres rather than edges
    bin_centres_y = (bin_edges_y[:-1] + bin_edges_y[1:]) / 2
    model_x = models.Gaussian1D(stddev=a)
    model_y = models.Gaussian1D(stddev=b)
    fit = fitting.LevMarLSQFitter()
    fitted_x = fit(model_x, bin_centres_x, hist_x)
    fitted_y = fit(model_y, bin_centres_y, hist_y)
    x_sigma = fitted_x.stddev.value
    y_sigma = fitted_y.stddev.value
    # print(x_sigma)
    # print(y_sigma)
    # plt.plot(bin_centres_x, hist_x, label="Data")
    # plt.plot(bin_centres_x, fitted_x(bin_centres_x), label="Fit")
    # plt.figure()
    # plt.plot(bin_centres_y, hist_y, label="Data")
    # plt.plot(bin_centres_y, fitted_y(bin_centres_y), label="Fit")
    M = ((clear_sigma_x / x_sigma) - 1) ** 2 + \
        ((clear_sigma_y / y_sigma) - 1) ** 2

    return M


def get_true_x_sigma_y_sigma(clear_sigma_x, clear_sigma_y):
    result = minimize(
        generate_elliptical_beam,
        x0=(clear_sigma_x, clear_sigma_y),
        args=(10000, clear_sigma_x, clear_sigma_y),
        method="Nelder-Mead",
    )
    M = result.fun
    x = result.x
    M_min = M
    x_min = x
    print(M_min)
    print(x_min)
    # generate_elliptical_beam(x_min, 100000, 0.8, 1.2)


# get_true_x_sigma_y_sigma(1.4, 1.3)

# true final beam:(2.0,2.16):2.84x3.0
# true beam at scatterer(1.4,1.3):1.98x1.84
# get_true_x_sigma_y_sigma(2.33, 2.0)
# generate_elliptical_beam([1.14508565, 1.70761944], 10000, 1, 2)
# 200
# true initial beam:(0.65 x 0.80): 0.86 x 1.14mm

# true final beam:(2.33 mm x 2.0):3.29mmx2.85mm

# 150
# true intial_beam(1.3 x 0.7 mm):1.83657125mmx 0.99433641mm
# true final beam with s1  (5.6 x 4.8):7.96970784x 6.65242155
# get_true_x_sigma_y_sigma(5.6, 4.8)


def find_initial_phsp(
    initial_sigma_x=0.86,
    initial_sigma_y=1.14,
    final_sigma_x=3.29,
    final_sigma_y=2.85,
    distance_between_screens=575,
    N=10000,
):
    def merit(px_py, initial_sigma_x, initial_sigma_y, final_x, final_y, N):
        initial_sigma_px = px_py[0]
        initial_sigma_py = px_py[1]

        ceu = clear_experiment_utils()
        ceu.run_through_no_scatterer(
            distance_between_screens,
            initial_sigma_x,
            initial_sigma_y,
            initial_sigma_px,
            initial_sigma_py,
        )
        # ceu.get_X_Y("clear_beam_no_scatterer.phsp")
        # ceu.run_through_s1_clear(
        #    10,
        #    250,
        #    initial_sigma_x,
        #    initial_sigma_y,
        #    initial_sigma_px,
        #    initial_sigma_py,
        #    energy=150,
        #    N=10000,
        # )
        ceu.get_X_Y("clear_beam_after_s1")

        true_dist, xedges, yedges = np.histogram2d(
            final_x,
            final_y,
            range=[
                [3 * -final_sigma_x, 3 * final_sigma_x],
                [3 * -final_sigma_y, 3 * final_sigma_y],
            ],
            normed=True,
            bins=10,
        )
        optimising_dist, xedges, yedges = np.histogram2d(
            ceu.X,
            ceu.Y,
            range=[
                [3 * -final_sigma_x, 3 * final_sigma_x],
                [3 * -final_sigma_y, 3 * final_sigma_y],
            ],
            normed=True,
            bins=10,
        )
        err = np.sum((true_dist - optimising_dist) ** 2) / float(
            true_dist.shape[0] * true_dist.shape[1]
        )
        return err

    a = final_sigma_x
    b = final_sigma_y
    # define random number generator for beam construction
    rng = np.random.default_rng()
    rang = rng.normal
    ran = rng.uniform
    # empty lists to hold beam parameters
    # x,y in mm, px,py in mrad
    x = []
    y = []

    # fill lists with beam parameters for uniform circular beam
    # and p radius PR
    for i in range(int(N)):
        R = np.sqrt(np.abs(rang()))

        phi = 2 * np.pi * np.abs(ran())

        x_i = R * np.cos(phi)

        y_i = R * np.sin(phi)
        x_i = x_i * a
        y_i = y_i * b

        x.append(x_i)
        y.append(y_i)
    initial_guess = (4, 8)
    bounds = ((0.1, 1000), (0.1, 1000))
    result = minimize(
        merit,
        x0=initial_guess,
        args=(initial_sigma_x, initial_sigma_y, x, y, N),
        method="Nelder-Mead",
    )
    M = result.fun
    x = result.x
    M_min = M
    x_min = x
    print(M_min)
    print(x_min)


#find_initial_phsp(1.98, 1.84, 2.84, 3.0, 575 - 385)
