import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.modeling import models, fitting
from new_s1_paper_utils import new_s1_paper_utils


def read_stats(
    thickness=18.34567,
    material='"Aluminum"',
    distance=2500,
    energy=200,
    delta_E=0,
    beam_dist="Gaussian",
    beam_pdist="Gaussian",
    xy_rad=1,
    pxy_rad=1,
):
    line = pd.read_parquet(
        "/home/robertsoncl/s1_paper_stats/"
        + str(thickness)
        + material
        + str(energy)
        + str(delta_E)
        + beam_dist
        + beam_pdist
        + str(xy_rad)
        + str(pxy_rad)
    )
    return line


def fit_2D_gaussian(x, y, fit_radius=75, bins=50):
    data_sim, x_edges, y_edges = np.histogram2d(
        x, y, bins=bins, range=[[-fit_radius, fit_radius], [-fit_radius, fit_radius]]
    )
    x_centres = (x_edges[:-1] + x_edges[1:]) / 2
    y_centres = (y_edges[:-1] + y_edges[1:]) / 2
    x, y = np.meshgrid(x_centres, y_centres)
    model = models.Gaussian2D()
    fitter = fitting.LevMarLSQFitter()
    fit_data = fitter(model, x, y, data_sim)
    err_params = np.sqrt(np.diag(fitter.fit_info["param_cov"]))
    return fit_data, x, y, err_params[3], err_params[4]


def fit_2D_lorentzian(x, y, fit_radius=150, bins=100):
    data_sim, x_edges, y_edges = np.histogram2d(
        x, y, bins=bins, range=[[-fit_radius, fit_radius], [-fit_radius, fit_radius]]
    )
    x_centres = (x_edges[:-1] + x_edges[1:]) / 2
    y_centres = (y_edges[:-1] + y_edges[1:]) / 2
    x, y = np.meshgrid(x_centres, y_centres)
    model = models.Lorentzian2D()
    fitter = fitting.LevMarLSQFitter()
    fit_data = fitter(model, x, y, data_sim)
    err_params = np.sqrt(np.diag(fitter.fit_info["param_cov"]))
    return fit_data, x, y, err_params[3], err_params[4]


def fit_1D_gaussian(x, max_radius=150, bins=100):
    # retrieve X data (rotationally symmetric, Y not required)

    # initiate Astropy Gaussian model with arbitrary initial values

    hist, bin_edges = np.histogram(x, bins=bins, range=[-max_radius, max_radius])
    # define X coordinates as bin centres rather than edges
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    # initialise LSQ fitter (fast, more complex fitter not necessary)
    fit_g = fitting.LevMarLSQFitter()
    g_init = models.Gaussian1D()
    # carry out gaussian fit over data
    g = fit_g(g_init, bin_centres, hist)

    return g


def get_slices(phsp, slice_width=1):
    phsp_xslice = phsp[(phsp["Y"] < slice_width)]
    phsp_xslice = phsp_xslice[(phsp_xslice["Y"] > -slice_width)]
    phsp_yslice = phsp[(phsp["X"] < slice_width)]
    phsp_yslice = phsp_yslice[(phsp_yslice["X"] > -slice_width)]
    return phsp_xslice, phsp_yslice


def plot_generic_1d_and_fits_e(rerun=True):
    utils = new_s1_paper_utils()
    if rerun is True:
        utils.run_through_uniform_foil_from_generated_beam(
            15.88112, '"Aluminum"', N=10000000
        )
    phsp_dict = utils.get_X_Y()
    print("done")
    e = phsp_dict["p"]
    e_slice_x, e_slice_y = get_slices(e)
    fig, ax = plt.subplots(
        1, 2, sharey=True, figsize=(10, 4), gridspec_kw={"width_ratios": [1, 1]}
    )
    fit = fit_1D_gaussian(e_slice_x["X"])
    # print(fit.stddev)
    x = np.linspace(-150, 150, 1000)
    ax[0].hist(e_slice_x["X"], bins=100, range=[-150, 150], color="k")
    ax[0].plot(x, fit(x), color="r")
    ax[0].set_xlabel("X (mm)")
    ax[0].set_ylabel("Density")
    ax[0].set_xlim([-150, 150])
    # ax[0].set_title("Simulated Data")
    g = models.Gaussian1D(stddev=75, amplitude=fit.amplitude.value)

    ax[1].plot(x, g(x), color="b")
    ax[1].set_xlabel("X (mm)")
    ax[1].set_xlim([-150, 150])
    plt.savefig("/home/robertsoncl/s1_paper_plots/1d_generic_e.png")
    plt.savefig("/home/robertsoncl/s1_paper_plots/1d_generic_e.pdf")


def plot_generic_2d_and_fits_e(rerun=True):
    utils = new_s1_paper_utils()
    if rerun is True:
        utils.run_through_uniform_foil_from_generated_beam(
            18.34567, '"Aluminum"', N=10000000
        )
    phsp_dict = utils.get_X_Y()
    print("done")
    e = phsp_dict["p"]
    fig, ax = plt.subplots(
        1, 3, sharey=True, figsize=(14, 4), gridspec_kw={"width_ratios": [1, 1, 1]}
    )
    ax[0].hist2d(e["X"], e["Y"], bins=100, range=[[-1000, 1000], [-1000, 1000]])
    ax[0].set_xlabel("X (mm)")
    # ax[0].set_ylabel("Y (mm)")
    # ax[0].set_title("Simulated Data")
    p, x, y, unc_x, unc_y = fit_2D_gaussian(e["X"], e["Y"])
    print("sigma=" + str(np.mean([p.x_stddev.value, p.y_stddev.value])) + "mm")
    print("sigma_err= " + str(max(unc_x, unc_y)) + "mm")
    ax[1].imshow(p(x, y), extent=[-150, 150, -150, 150])
    ax[1].set_xlabel("X (mm)")
    ax[1].set_yticks([-100, 0, 100])

    # ax[1].set_ylabel("Y (mm)")
    # ax[1].set_xlim([-100, 100])
    # ax[1].set_ylim([-100, 100])
    # ax[1].set_title(
    #    "Gaussian Fit to Simulated Data, $\sigma$=" + str(p.x_stddev) + "mm"
    # )
    g = models.Gaussian2D(x_stddev=75, y_stddev=75)
    ax[2].imshow(g(x, y), extent=[-150, 150, -150, 150])
    ax[2].set_xlabel("X (mm)")
    plt.savefig("/home/robertsoncl/s1_paper_plots/2d_generic_e.png")
    plt.savefig("/home/robertsoncl/s1_paper_plots/2d_generic_e.pdf")
    # ax[2].set_ylabel("Y (mm)")
    # ax[2].set_xlim([-100, 100])
    # ax[2].set_ylim([-100, 100])
    # ax[2].set_title("Moliere Approximation Prediction, $\sigma$=75 mm")


def plot_energy_variations():

    energies = np.arange(50, 250, 25)
    lines = []
    for i in energies:
        lines.append(read_stats(energy=i))
    stats = pd.concat(lines)

    mean_E_unc = 0.02
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.scatter(
        energies,
        stats["mol_sigma"],
        marker="x",
        label="Theoretical Electron $\sigma$",
        color="k",
        s=5,
    )
    # ax.scatter(energies, sigmas, color="red", label="Electron $\sigma$", s=3)
    ax.errorbar(
        energies,
        stats["e_sigma"],
        yerr=stats["e_sigma_unc"],
        color="r",
        ecolor="r",
        ls="none",
        capsize=5,
        markersize=1,
        linewidth=1,
        label="Electron $\sigma$",
    )
    ax.errorbar(
        energies,
        np.abs(stats["y_rms"]),
        yerr=stats["y_rms_unc"],
        color="b",
        ecolor="b",
        ls="none",
        capsize=5,
        markersize=1,
        linewidth=1,
        label="Photon fwhm",
    )
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_xlabel("Energy (MeV)")
    ax.set_ylabel("Radial Distance (mm)")
    ax.legend(loc="upper right")
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    ax[0].plot(
        energies,
        stats["mean_e"],
        color="r",
        linewidth=1,
        label="Mean Final Electron Energy",
    )
    ax[0].plot(
        energies,
        stats["mean_e_y"],
        color="b",
        linewidth=1,
        label="Mean Final Photon Energy",
    )
    ax[0].set_axisbelow(True)
    ax[0].grid(True)
    ax[0].set_xlabel("Initial Energy (MeV)")
    ax[0].set_ylabel("Finial Energy (MeV)")
    ax[0].legend(loc="upper left")
    ax[1].plot(
        energies, stats["e_N"], color="r", linewidth=1, label="Electron Component"
    )
    ax[1].plot(energies, stats["y_N"], color="b", linewidth=1, label="Photon Component")
    ax[1].set_axisbelow(True)
    ax[1].grid(True)
    ax[1].set_xlabel("Initial Energy (MeV)")
    ax[1].set_ylabel("Final Beam Proportion (%)")
    ax[1].legend(loc="upper left")


def plot_beam_radius_variations():

    r = [0.25, 0.5, 0.75, 1, 2]
    lines = []
    for i in r:
        lines.append(read_stats(xy_rad=i))
    stats = pd.concat(lines)
    mean_E_unc = 0.02
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.scatter(
        r,
        stats["mol_sigma"],
        marker="x",
        label="Theoretical Electron $\sigma$",
        color="k",
        s=5,
    )
    # ax.scatter(energies, sigmas, color="red", label="Electron $\sigma$", s=3)
    ax.errorbar(
        r,
        stats["e_sigma"],
        yerr=stats["e_sigma_unc"],
        color="r",
        ecolor="r",
        ls="none",
        capsize=5,
        markersize=1,
        linewidth=1,
        label="Electron $\sigma$",
    )
    ax.errorbar(
        r,
        stats["y_rms"],
        yerr=stats["y_rms_unc"],
        color="b",
        ecolor="b",
        ls="none",
        capsize=5,
        markersize=1,
        linewidth=1,
        label="Photon fwhm",
    )
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_xlabel("Initial Beam Radius (mm)")
    ax.set_ylabel("Radial Distance (mm)")
    ax.legend(loc="upper right")
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    ax[0].plot(
        r, stats["mean_e"], color="r", linewidth=1, label="Mean Final Electron Energy"
    )
    ax[0].plot(
        r, stats["mean_e_y"], color="b", linewidth=1, label="Mean Final Photon Energy"
    )
    ax[0].set_axisbelow(True)
    ax[0].grid(True)
    ax[0].set_xlabel("Initial Beam Radius (mm)")
    ax[0].set_ylabel("Finial Energy (MeV)")
    ax[0].legend(loc="upper left")
    ax[1].plot(r, stats["e_N"], color="r", linewidth=1, label="Electron Component")
    ax[1].plot(r, stats["y_N"], color="b", linewidth=1, label="Photon Component")
    ax[1].set_axisbelow(True)
    ax[1].grid(True)
    ax[1].set_xlabel("Initial Radius (mm)")
    ax[1].set_ylabel("Final Beam Proportion (%)")
    ax[1].legend(loc="upper left")


def plot_beam_pradius_variations():

    pr = [0.25, 0.5, 0.75, 1, 2]
    lines = []
    for i in pr:
        lines.append(read_stats(xy_prad=i))
    stats = pd.concat(lines)
    mean_E_unc = 0.02
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.scatter(
        pr,
        stats["mol_sigma"],
        marker="x",
        label="Theoretical Electron $\sigma$",
        color="k",
        s=5,
    )
    # ax.scatter(energies, sigmas, color="red", label="Electron $\sigma$", s=3)
    ax.errorbar(
        pr,
        stats["e_sigma"],
        yerr=stats["e_sigma_unc"],
        color="r",
        ecolor="r",
        ls="none",
        capsize=5,
        markersize=1,
        linewidth=1,
        label="Electron $\sigma$",
    )
    ax.errorbar(
        pr,
        stats["y_rms"],
        yerr=stats["y_rms_unc"],
        color="b",
        ecolor="b",
        ls="none",
        capsize=5,
        markersize=1,
        linewidth=1,
        label="Photon fwhm",
    )
    ax.set_axisbelow(True)
    ax.grid(True)
    ax.set_xlabel("Initial Beam Radius (mm)")
    ax.set_ylabel("Radial Distance (mm)")
    ax.legend(loc="upper right")
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    ax[0].plot(
        pr, stats["mean_e"], color="r", linewidth=1, label="Mean Final Electron Energy"
    )
    ax[0].plot(
        pr, stats["mean_e_y"], color="b", linewidth=1, label="Mean Final Photon Energy"
    )
    ax[0].set_axisbelow(True)
    ax[0].grid(True)
    ax[0].set_xlabel("Initial Beam Radius (mm)")
    ax[0].set_ylabel("Finial Energy (MeV)")
    ax[0].legend(loc="upper left")
    ax[1].plot(pr, stats["e_N"], color="r", linewidth=1, label="Electron Component")
    ax[1].plot(pr, stats["y_N"], color="b", linewidth=1, label="Photon Component")
    ax[1].set_axisbelow(True)
    ax[1].grid(True)
    ax[1].set_xlabel("Initial Radius (mm)")
    ax[1].set_ylabel("Final Beam Proportion (%)")
    ax[1].legend(loc="upper left")


# plot_generic_2d_and_fits(rerun=False)
plot_energy_variations()
