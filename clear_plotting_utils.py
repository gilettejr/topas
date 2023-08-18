from scipy.io import loadmat
from super_g_scipy import super_g
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from astropy.modeling import models, fitting
from Super_Gaussian2D import Super_Gaussian2D
from clear_experiment_utils import clear_experiment_utils
from PIL import Image
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import cv2 as cv

# 0.0637mm/px


class clear_plotting_utils_dual:
    def __init__(self, filename, scale=0.0637):

        image_data = loadmat(filename)
        self.image_data = image_data["image"]
        self.scale = scale

    def show_image(self):
        plt.imshow(
            self.image_data, cmap="jet", interpolation="nearest", vmin=0, vmax=1000
        )
        plt.xlabel("X [pixels]")
        plt.ylabel("Y [pixels]")

    def crop_image(self):
        image = self.image_data
        print(image)
        image = plt.imshow(image)
        print(image)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        plt.imshow(gray)
        circle = cv.HoughCircles()

    def fit_and_get_sigmas_real_data(self):

        data = self.image_data

        scale = self.scale
        y, x = np.mgrid[: np.shape(data)[0], : np.shape(data)[1]]
        plot_y = y * scale
        plot_x = x * scale
        x_extent = max(np.shape(data[1])) * scale / 2
        y_extent = max(np.shape(data[0])) * scale / 2
        # y = y * scale
        # x = x * scale
        fitter = fitting.LevMarLSQFitter()
        model = models.Super_Gaussian2D()
        fitted = fitter(model, x, y, data)
        x_rms = np.sqrt(np.mean(plot_x ** 2))
        y_rms = np.sqrt(np.mean(plot_y ** 2))
        # plt.rc('title', labelsize=20)
        plt.rc("axes", labelsize=20)
        plt.rc("xtick", labelsize=20)
        plt.rc("ytick", labelsize=20)
        norm = clr.Normalize()
        plt.figure(figsize=(20, 8))
        plt.subplot(1, 3, 1)
        plt.imshow(
            data,
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-x_extent, x_extent, -y_extent, y_extent],
        )
        plt.ylabel("y [mm]")
        plt.xlabel("x [mm]")
        plt.title("Experimental Data")
        # plt.colorbar()
        plt.subplot(1, 3, 2)
        plt.imshow(
            fitted(x, y),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-x_extent, x_extent, -y_extent, y_extent],
        )
        plt.xlabel("x [mm]")
        plt.title("Gaussian Fit")
        # plt.colorbar()
        plt.subplot(1, 3, 3)
        plt.imshow(
            data - fitted(x, y),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-x_extent, x_extent, -y_extent, y_extent],
        )
        plt.xlabel("x [mm]")
        plt.title("Residuals")
        print(fitted.x_stddev.value * scale)
        print(fitted.y_stddev.value * scale)
        print(fitted.power)

        # print("X RMS = " + str(x_rms) + "mm")
        # print("Y RMS = " + str(y_rms) + "mm")

        # plt.colorbar()
    def fit_and_get_sigmas_real_superg(self):

        data = self.image_data

        scale = self.scale
        y, x = np.mgrid[: np.shape(data)[0], : np.shape(data)[1]]

        plot_y = y * scale
        plot_x = x * scale
        x_extent = max(np.shape(data[1])) * scale / 2
        y_extent = max(np.shape(data[0])) * scale / 2
        # y = y * scale
        # x = x * scale
        norm = clr.Normalize()
        bounds = np.transpose([[-np.inf, np.inf], [0, 930], [
            0, 901], [0, 450], [0, 450], [0, 10]])
        popt, pcov = curve_fit(
            super_g, (plot_x, plot_y), data.ravel(), bounds=bounds, p0=(100, 0, 0, 14, 14, 2))
        fit_data = super_g((plot_x, plot_y), *popt)
        print(popt)
        perr = np.sqrt(np.diag(pcov))
        print(perr)
        #x_rms = np.sqrt(np.mean(plot_x ** 2))
        #y_rms = np.sqrt(np.mean(plot_y ** 2))
        # plt.rc('title', labelsize=20)
        plt.rc("axes", labelsize=20)
        plt.rc("xtick", labelsize=20)
        plt.rc("ytick", labelsize=20)

        norm = clr.Normalize()
        plt.figure(figsize=(20, 8))
        plt.rc('font', size=20)
        plt.subplot(1, 3, 1)
        plt.imshow(
            data,
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-x_extent, x_extent, -y_extent, y_extent],
        )
        plt.ylabel("y [mm]")
        plt.xlabel("x [mm]")
        plt.title("Experimental Data")
        # plt.colorbar()
        plt.subplot(1, 3, 2)
        plt.imshow(
            fit_data.reshape(np.shape(data)[0], np.shape(data)[1]),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-x_extent, x_extent, -y_extent, y_extent],
        )
        plt.xlabel("x [mm]")
        plt.title("Super Gaussian Fit")
        # plt.colorbar()
        plt.subplot(1, 3, 3)
        plt.imshow(
            data - fit_data.reshape(np.shape(data)[0], np.shape(data)[1]),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-x_extent, x_extent, -y_extent, y_extent],
        )
        plt.xlabel("x [mm]")
        plt.title("Residuals")

    def fit_and_get_sigmas_simulated_superg(self, s1_thickness, s1_to_s2):
        ceu = clear_experiment_utils()
        ceu.run_through_s1_and_s2_clear(
            s1_thickness,
            s1_to_patient=575,
            sigma=19.52898,
            max_height=110.0,
            shape_radius=24.28,
            sigma_x=1.14,
            sigma_y=1.17,
            sigma_px=4.4,
            sigma_py=3.5,
            # show_shape=True,
            N=1000000,
            s1_to_s2=s1_to_s2,
            N_slices=30,
        )
        # ceu.run_through_s1_clear(s1_thickness, distance_to_patient)
        ceu.get_X_Y("S2_beam")
        data_sim, x_edges, y_edges = np.histogram2d(
            ceu.X, ceu.Y, bins=100, range=[[-30, 30], [-30, 30]]
        )
        x_centres = (x_edges[:-1] + x_edges[1:]) / 2
        y_centres = (y_edges[:-1] + y_edges[1:]) / 2
        x, y = np.meshgrid(x_centres, y_centres)
        norm = clr.Normalize()
        popt, pcov = curve_fit(
            super_g, (x, y), data_sim.ravel(), p0=(100, 0, 0, 14, 14, 5))
        print(popt)
        perr = np.sqrt(np.diag(pcov))
        print(perr)
        fit_data = super_g((x, y), *popt)
        plt.rc("axes", labelsize=20)
        plt.rc("xtick", labelsize=20)
        plt.rc("ytick", labelsize=20)
        plt.figure(figsize=(20, 8))
        plt.subplot(1, 3, 1)
        plt.imshow(
            np.transpose(data_sim),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-30, 30, -30, 30],
        )
        plt.xlabel("x [mm]")
        plt.ylabel("y [mm]")
        plt.title("Simulated Data")
        # plt.colorbar()
        plt.subplot(1, 3, 2)
        plt.imshow(
            fit_data.reshape(x_centres.shape[0], y_centres.shape[0]),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-30, 30, -30, 30],
        )
        plt.xlabel("x [mm]")

        plt.title("Super Gaussian Fit")
        # plt.colorbar()
        plt.subplot(1, 3, 3)
        plt.imshow(
            np.transpose(data_sim) -
            fit_data.reshape(x_centres.shape[0], y_centres.shape[0]),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-30, 30, -30, 30],
        )
        plt.xlabel("x [mm]")
        plt.title("Residuals")
        # print(fit_data.x_stddev.value)
        # print(fit_data.y_stddev.value)
        # print(fit_data.power)
        hist, bins = np.histogram(ceu.X, bins=100, range=[-30, 30])
        bins = bins + 30
        plt.figure()
        plt.plot(bins[1:], hist)
        plt.xlabel("X [mm]")
        plt.ylabel("Intensity")
        hist, bins = np.histogram(ceu.Y, bins=100, range=[-30, 30])
        bins = bins + 30
        plt.figure()
        plt.plot(bins[1:], hist)
        plt.xlabel("Y [mm]")
        plt.ylabel("Intensity")

    def fit_and_get_sigmas_simulated(self, s1_thickness, s1_to_s2):
        ceu = clear_experiment_utils()
        # ceu.run_through_s1_and_s2_clear(
        #    s1_thickness,
        #    s1_to_patient=575,
        #    sigma=19.52898,
        #    max_height=110.0,
        #    shape_radius=24.28,
        #    sigma_x=1.14,
        #    sigma_y=1.17,
        #    sigma_px=4.4,
        #    sigma_py=3.5,
        #    # show_shape=True,
        #    N=1000000,
        #    s1_to_s2=s1_to_s2,
        #    N_slices=30,
        # )
        # ceu.run_through_s1_clear(s1_thickness, distance_to_patient)
        ceu.get_X_Y("S2_beam")
        data_sim, x_edges, y_edges = np.histogram2d(
            ceu.gamma_X, ceu.gamma_Y, bins=100, range=[[-30, 30], [-30, 30]]
        )
        x_centres = (x_edges[:-1] + x_edges[1:]) / 2
        y_centres = (y_edges[:-1] + y_edges[1:]) / 2
        x, y = np.meshgrid(x_centres, y_centres)
        norm = clr.Normalize()
        model = models.Gaussian2D()
        fitter = fitting.LevMarLSQFitter()
        fit_data = fitter(model, x, y, data_sim)
        plt.rc("axes", labelsize=20)
        plt.rc("xtick", labelsize=20)
        plt.rc("ytick", labelsize=20)
        plt.figure(figsize=(20, 8))
        plt.rc('font', size=20)
        plt.subplot(1, 3, 1)
        plt.imshow(
            np.transpose(data_sim),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-30, 30, -30, 30],
        )
        plt.xlabel("x [mm]")
        plt.ylabel("y [mm]")
        plt.title("Simulated Data")
        # plt.colorbar()
        plt.subplot(1, 3, 2)
        plt.imshow(
            fit_data(y, x),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-30, 30, -30, 30],
        )
        plt.xlabel("x [mm]")

        plt.title("Gaussian Fit")
        # plt.colorbar()
        plt.subplot(1, 3, 3)
        plt.imshow(
            np.transpose(data_sim) - fit_data(y, x),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-30, 30, -30, 30],
        )
        plt.xlabel("x [mm]")
        plt.title("Residuals")
        # print(fit_data.x_stddev.value)
        # print(fit_data.y_stddev.value)
        # print(fit_data.power)
        hist, bins = np.histogram(ceu.X, bins=100, range=[-30, 30])
        bins = bins + 30
        plt.figure()
        plt.plot(bins[1:], hist)
        plt.xlabel("X [mm]")
        plt.ylabel("Intensity")
        hist, bins = np.histogram(ceu.Y, bins=100, range=[-30, 30])
        bins = bins + 30
        plt.figure()
        plt.plot(bins[1:], hist)
        plt.xlabel("Y [mm]")
        plt.ylabel("Intensity")

    def get_1D_profile_real(self):

        data = self.image_data
        scale = self.scale

        def collapse_along_axis(matrix):
            # initialise list for holding result
            collapsed_matrix = []
            # loop through matrix and add median of each row to 1D array
            # median better than mean here as it smooths out extrema
            for i in matrix:
                collapsed_matrix.append(np.median(i))
            # return 1D array of medians
            return collapsed_matrix

        # collapse matrix to get median x dose distributions along y axis
        collapsed_dose_along_y = collapse_along_axis(data)
        # collapse matrix to get median y dose distributions along x axis
        collapsed_dose_along_x = collapse_along_axis(np.transpose(data))
        x_axis_x = np.arange(len(collapsed_dose_along_x)) * scale
        x_axis_y = np.arange(len(collapsed_dose_along_y)) * scale
        plt.figure()
        plt.plot(x_axis_x, collapsed_dose_along_x)
        plt.xlabel("X [mm]")
        plt.ylabel("Intensity")
        plt.figure()
        plt.plot(x_axis_y, collapsed_dose_along_y)
        plt.xlabel("Y [mm]")
        plt.ylabel("Intensity")

        plt.rc("axes", labelsize=10)
        plt.rc("xtick", labelsize=10)
        plt.rc("ytick", labelsize=10)
        # histograms_along_x_axis(x, y)
        # histograms_along_y_axis(x, y)
        # plt.plot(data[0])

    def plot_energy_spread(self):
        ceu = clear_experiment_utils()
        ceu.get_X_Y("S2_beam.phsp")
        plt.figure()
        plt.hist(ceu.col_E, bins=100)
        plt.xlabel("E")
        plt.ylabel("Intensity")
        plt.rc("axes", labelsize=10)
        plt.rc("xtick", labelsize=10)
        plt.rc("ytick", labelsize=10)
        e_disp = ceu.E - 200
        e_disp_rms = np.sqrt(np.mean(e_disp ** 2))
        print(np.mean(ceu.col_E))


cpud = clear_plotting_utils_dual(
    "/home/robertsoncl/topas/clear_ex2_images/30_335_1.mat"
)
# cpud.show_image()
#cpud.fit_and_get_sigmas_simulated_superg(30, 335)
# cpud.fit_and_get_sigmas_real_superg()

cpud.fit_and_get_sigmas_simulated(30, 335)
# cpud.crop_image()
# cpud.plot_energy_spread()
# cpud.plot_sigma_evolution()
# cpud.plot_sigma_evolution()
