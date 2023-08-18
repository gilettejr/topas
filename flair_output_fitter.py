import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from thickness_optimiser_utils import thickness_optimiser_utils
from astropy.modeling import models, fitting
from astropy.table import Table
from astropy.io import ascii


def import_flair_data(filename="/home/robertsoncl/fluka_benchmark_51_plot.dat"):
    flair_data = ascii.read(filename, names=["X", "Y", "Density", "Error"])
    plotting_data = pd.DataFrame(
        {"X": flair_data["X"].value, "Density": flair_data["Density"].value}
    )
    return plotting_data


def fit_and_plot_data(plotting_data):
    x = plotting_data["X"]
    y = plotting_data["Density"]
    fitter = fitting.LevMarLSQFitter()
    gaussian_init = models.Gaussian1D()
    gaussian_fit = fitter(gaussian_init, x, y)
    x_smoothed = np.arange(-40, 40, step=0.01)
    plt.plot(x_smoothed, gaussian_fit(x_smoothed), color="black")
    plt.plot(x, y, color="red")
    print(gaussian_fit)


def get_two_sigma_topas(length, distance, material, energy):
    beam = thickness_optimiser_utils()
    beam.run_through_uniform_foil_from_generated_beam(
        length, distance, material, N=1000000, energy=energy
    )
    beam.get_X_Y("scattered_beam.phsp")
    # beam.plot_transverse_beam()
    two_sigma = beam.get_two_sigma()
    print(two_sigma)


# get_two_sigma_topas(0.116549, 2500, '"Tantalum"', "100")
plotting_data = import_flair_data()
fit_and_plot_data(plotting_data)
