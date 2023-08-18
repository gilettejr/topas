import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
import matplotlib.text as text
import numpy as np
from scipy.stats import norm

# p and t - p placement, t placement, t length
# E_sigma array is [E, sigma]
# s1 array is [material,thickness,placement]
# s2 array is [material, thickness, placement, N_slices]
def show_scattering_setup(E_sigma, s1_array, s2_array, patient_and_tank_array):
    sc = scattering_setup_drawer([E_sigma, s1_array, s2_array, patient_and_tank_array])
    sc.add_patient()
    sc.add_s1()
    sc.add_s2()


class scattering_setup_drawer:
    def __init__(self, master_array):
        fig, ax = plt.subplots(1)
        ax.set_ylim([-500, 500])
        self.ax = ax
        self.master_array = master_array
        self.E = master_array[0][0]

    def add_patient(self):
        ax = self.ax
        patient_and_tank_array = self.master_array[3]
        ax.set_xlim([-200, patient_and_tank_array[0] + 200])
        patient = lines.Line2D(
            [patient_and_tank_array[0], patient_and_tank_array[0]],
            [-100, 100],
            lw=2,
            color="black",
            axes=ax,
        )
        ax.add_line(patient)

    def add_s1(self):
        ax = self.ax
        s1_thickness = self.master_array[1][1]
        s1_placement = self.master_array[1][2]
        s1 = patches.Rectangle([s1_placement, -10], s1_thickness, 20, fc="k")
        ax.add_patch(s1)

    def add_s2(self):
        # E in MeV, X in mm, d in mm, theta in mrad
        def moliere_angle(E, X, d, init_theta=0):
            final_theta = (
                (14.1 / (E / 1000)) * np.sqrt(d / X) * (1 + (1 / 9) * np.log10(d / X))
            )
            return np.sqrt(init_theta ** 2 + final_theta ** 2)

        def get_s2_sigma(theta, s1_to_s2):
            print(s1_to_s2)
            final_sigma = s1_to_s2 / 1000 * np.tan(theta / 1000)
            return final_sigma * 1000

        ax = self.ax
        s2_thickness = self.master_array[2][1]
        s2_placement = self.master_array[2][2]
        sigma_px = self.master_array[0][1]
        X_dict = {"Aluminum": 88.97, "Nylon": 355.2, "Tantalum": 4.094}
        X = X_dict[self.master_array[1][0]]
        s1_scattered_angle = moliere_angle(self.E, X, self.master_array[1][1], sigma_px)
        sigma_at_s2 = get_s2_sigma(
            s1_scattered_angle,
            self.master_array[2][2] - self.master_array[1][2] - self.master_array[1][1],
        )
        s2_sigma = sigma_at_s2
        # define spread of gaussian shape
        # and precision (number of slices in shape) with step argument
        # x = np.arange(-half_width, half_width, step=1)
        x = np.arange(-s2_sigma * 2, 0, step=s2_sigma * 2 / self.master_array[2][3])

        # construct gaussian profile from method argument sigma
        y = norm.pdf(x, 0, s2_sigma)
        # scale for input amplitude
        y = y - min(y)
        y_scaling_factor = s2_thickness / max(y)
        y = y * y_scaling_factor
        # plt.plot(x, y)
        x = np.array(x)
        # scale height and normalise base to 0
        # according to method argument max_height
        # define distance in mm from beam source to gaussian foil
        # define half_y for ease, as Topas uses half lengths
        for i in range(1, len(y)):
            # Don't try to create 0 height widths
            # skip relevant rows
            L = y[i] - y[i - 1]
            HL = L / 2

            # define slice as cylinder
            s2_slice = patches.Rectangle(
                [s2_placement + y[i - 1] + L / 2, -abs(x[i])], L, 2 * abs(x[i]), fc="k"
            )
            ax.add_patch(s2_slice)
            # increment to begin next slice until shape completion
            i = i + 1


E_sigma = (200, 1)
s1_array = ["Tantalum", 10, 200]
s2_array = ["Aluminum", 100, 400, 30]
patient_and_tank_array = [1000, 20]
show_scattering_setup(E_sigma, s1_array, s2_array, patient_and_tank_array)
