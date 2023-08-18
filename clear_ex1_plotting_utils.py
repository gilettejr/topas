from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
from astropy.modeling import models, fitting
from clear_experiment_utils import clear_experiment_utils
from PIL import Image
from scipy.signal import savgol_filter

import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import cv2 as cv


class clear_plotting_utils:
    def __init__(self, filename):

        scale = 10 / (338 - 154)
        image_data = loadmat(filename)
        self.image_data = np.median(image_data["Images_beam"], axis=2)
        self.scale = scale

    def show_image(self):
        plt.imshow(
            self.image_data, cmap="jet", interpolation="nearest", vmin=0, vmax=30
        )
        plt.xlabel("X [pixels]")
        plt.ylabel("Y [pixels]")

    def fit_and_get_sigmas_real_data(self):

        data = self.image_data

        scale = self.scale
        y, x = np.mgrid[: np.shape(data)[0], : np.shape(data)[1]]
        print(y)
        print(x)
        plot_y = y * scale
        plot_x = x * scale
        x_extent = max(np.shape(data[1])) * scale / 2
        y_extent = max(np.shape(data[0])) * scale / 2
        # y = y * scale
        # x = x * scale
        fitter = fitting.LevMarLSQFitter()
        model = models.Gaussian2D()
        fitted = fitter(model, x, y, data)
        norm = clr.Normalize(vmin=0, vmax=50)
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
        # plt.colorbar()

    # x,y for 150=1.83657125mm x 0.99433641
    # px,py for 150=7.80910106 5.78318716
    def fit_and_get_sigmas_simulated(self, s1_thickness, distance_to_patient):
        ceu = clear_experiment_utils()
        ceu.run_through_s1_clear(
            s1_thickness,
            distance_to_patient,
            sigma_x=1.83657125,
            sigma_y=0.99433641,
            sigma_px=7.80910106,
            sigma_py=5.78318716,
            energy=150,
            N=50,
        )
        # ceu.run_through_s1_clear(s1_thickness, distance_to_patient)
        ceu.get_X_Y("clear_beam_after_s1.phsp")
        data_sim, x_edges, y_edges = np.histogram2d(
            ceu.X, ceu.Y, bins=20, range=[[-15, 15], [-15, 15]]
        )
        x_centres = (x_edges[:-1] + x_edges[1:]) / 2
        y_centres = (y_edges[:-1] + y_edges[1:]) / 2
        x, y = np.meshgrid(x_centres, y_centres)
        norm = clr.Normalize()
        model = models.Gaussian2D()
        fitter = fitting.LevMarLSQFitter()
        fit_data = fitter(model, x, y, data_sim)
        plt.figure()
        plt.subplot(1, 3, 1)
        plt.imshow(
            np.transpose(data_sim),
            cmap="jet",
            interpolation="nearest",
            norm=norm,
            extent=[-15, 15, -15, 15],
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
            extent=[-15, 15, -15, 15],
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
            extent=[-15, 15, -15, 15],
        )
        plt.xlabel("x [mm]")
        plt.title("Residuals")
        print(fit_data.x_stddev.value)
        print(fit_data.y_stddev.value)

    def plot_sigma_evolution(self):
        x_sim_30 = [
            13.4560458705721,
            14.725931227006,
            16.6330988484478,
            20.575785723821113,
        ]
        y_sim_30 = [
            13.6177230464886,
            14.9045531817007,
            16.8265098469763,
            20.807629939865098,
        ]
        x_sim_20 = [11.737422101730967,
                    12.926698707856866, 14.571335889431989, np.nan]
        y_sim_20 = [11.898896498664445,
                    13.097421648555345, 14.786777818586451, np.nan]
        x_sim_10 = [9.763927192846639,
                    10.988286543068023, 12.87008901545043, np.nan]
        y_sim_10 = [10.001505284309548,
                    10.988286543068023, 12.653149083847795, np.nan]

        x_expt_30 = [
            14.7176941361006,
            15.5295066921113,
            17.1902246415217,
            17.247570138667893,
        ]
        y_expt_30 = [
            14.33934283336462,
            15.823733971588,
            16.8531406423615,
            17.82208336078307,
        ]
        x_expt_20 = [12.83987290094563,
                     14.368801682499399, 15.71543908803945, np.nan]
        y_expt_20 = [13.231149723304899,
                     13.905475980968108, 15.308877203923743, np.nan]
        x_expt_10 = [10.604432691848915,
                     12.03948589769084, 13.411678436844095, np.nan]
        y_expt_10 = [10.95802416981006,
                     12.3581186620766, 13.746022023364144, np.nan]

        distances = [381, 335, 281, 181]
        plt.figure()
        plt.plot(distances, x_sim_30, label="s1=30mm, simulated")
        plt.plot(distances, x_expt_30, label="s1=30mm, CLEAR")
        plt.plot(distances, x_sim_20, label="s1=20mm, simulated")
        plt.plot(distances, x_expt_20, label="s1=20mm, CLEAR")
        plt.plot(distances, x_sim_10, label="s1=10mm, simulated")

        plt.plot(distances, x_expt_10, label="s1=10mm, CLEAR")
        plt.legend()
        plt.xlabel("z [mm]")
        plt.ylabel("$\sigma_x$ Value from Fit [mm]")
        plt.figure()
        plt.plot(distances, y_sim_30, label="s1=30mm, simulated")
        plt.plot(distances, y_expt_30, label="s1=30mm, CLEAR")
        plt.plot(distances, y_sim_20, label="s1=20mm, simulated")
        plt.plot(distances, y_expt_20, label="s1=20mm, CLEAR")
        plt.plot(distances, y_sim_10, label="s1=10mm, simulated")

        plt.plot(distances, y_expt_10, label="s1=10mm, CLEAR")
        plt.legend()
        plt.xlabel("z [mm]")
        plt.ylabel("$\sigma_y$ from Fit [mm]")


# cpu = clear_plotting_utils("matlab_images/30_500_150.mat")
# cpu.show_image()
# cpu.fit_and_get_sigmas_real_data()
# cpu.fit_and_get_sigmas_simulated(30, 500)
