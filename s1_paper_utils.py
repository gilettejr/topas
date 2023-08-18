from thickness_optimiser_utils import thickness_optimiser_utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
from scipy.stats import kurtosis
import xarray as xr


class s1_paper_utils(thickness_optimiser_utils):
    def __init__(self, path_to_data_folder="/home/robertsoncl/topas/s1_paper_data/"):
        def unpacker(param_array):
            (
                title_material,
                energy,
                thickness,
                energy_spread,
                radius,
                angular_radius,
                gauss,
            ) = param_array
            return (
                title_material,
                energy,
                thickness,
                energy_spread,
                radius,
                angular_radius,
                gauss,
            )

        def trim_to_radius(phase_space, radius):
            phase_space = phase_space.copy()
            # create DataFrame containing only electron data at patient
            phase_space = phase_space.drop(
                phase_space[
                    np.sqrt(phase_space["X"] ** 2 + phase_space["Y"] ** 2) > radius
                ].index
            )
            phase_space = phase_space.dropna()
            return phase_space

        def retrieve_phase_space(param_array):
            (
                title_material,
                energy,
                thickness,
                energy_spread,
                radius,
                angular_radius,
                gauss,
            ) = unpacker(param_array)
            title = (
                path_to_data_folder
                + title_material
                + "_"
                + str(energy)
                + "MeV_"
                + str(thickness)
                + "mm_"
                + str(energy_spread)
                + "%_"
                + str(radius)
                + "mm_"
                + str(angular_radius)
                + "mrad_"
                + str(gauss)
                + ".phsp"
            )

            # read Topas ASCII output file
            total_phase_space = pd.read_csv(
                title,
                names=["X", "Y", "Z", "PX", "PY", "E", "Weight", "PDG", "9", "10"],
                delim_whitespace=True,
            )
            # create DataFrame containing only electron data at patient
            electron_phase_space = total_phase_space.drop(
                total_phase_space[total_phase_space["PDG"] != 11].index
            )
            # create DataFrame containing only gamma data at patient
            gamma_phase_space = total_phase_space.drop(
                total_phase_space[total_phase_space["PDG"] != 22].index
            )

            total_phase_space = total_phase_space.dropna()
            electron_phase_space = electron_phase_space.dropna()
            gamma_phase_space = gamma_phase_space.dropna()

            total_phase_space["X"] = total_phase_space["X"] * 10
            total_phase_space["Y"] = total_phase_space["Y"] * 10
            total_phase_space["E"] = total_phase_space["E"]

            electron_phase_space["X"] = electron_phase_space["X"] * 10
            electron_phase_space["Y"] = electron_phase_space["Y"] * 10
            electron_phase_space["E"] = electron_phase_space["E"]

            gamma_phase_space["X"] = gamma_phase_space["X"] * 10
            gamma_phase_space["Y"] = gamma_phase_space["Y"] * 10
            gamma_phase_space["E"] = gamma_phase_space["E"]

            return total_phase_space, electron_phase_space, gamma_phase_space

        def get_two_sigma_fitted(phase_space, max_radius=100):
            phase_space = phase_space.copy()
            # retrieve X data (rotationally symmetric, Y not required)

            # phase_space = trim_to_radius(phase_space, max_radius=)
            X = phase_space["X"]

            hist, bin_edges = np.histogram(X, bins="auto")
            # define X coordinates as bin centres rather than edges
            bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
            # initialise LSQ fitter (fast, more complex fitter not necessary)
            fit_g = fitting.LevMarLSQFitter()
            g_init = models.Gaussian1D()
            # carry out gaussian fit over data
            g = fit_g(g_init, bin_centres, hist)
            # plt.figure()
            # plt.plot(bin_centres, g(bin_centres))
            # plt.plot(bin_centres, hist)

            return 2 * g.stddev.value

        def import_moliere_table(
            path_to_file="/home/robertsoncl/topas/moliere_sigma_table_",
            element="Aluminum",
        ):
            moliere_table = np.load(path_to_file + element + ".npy")
            if element == "G4NYLON":
                i = 0
            elif element == "Aluminum":
                i = 1
            elif element == "Steel":
                i = 2
            else:
                i = 3
            table = xr.DataArray(
                moliere_table,
                coords={
                    "Energy": self.energies,
                    "s1_thickness": self.all_thicknesses[i],
                    "Energy_spread": self.energy_spreads,
                    "Radius": self.radii,
                    "Angular_radius": self.angles,
                },
            )
            return table

        def moliere_to_thickness(energy, theta, X):
            d = X * (energy * theta / 14) ** 2
            return d

        self.trim_to_radius = trim_to_radius

        self.get_two_sigma_fitted = get_two_sigma_fitted

        self.retrieve_phase_space = retrieve_phase_space

        self.import_moliere_table = import_moliere_table

        self.energies = [
            50,
            60,
            70,
            80,
            90,
            100,
            110,
            120,
            130,
            140,
            150,
            160,
            170,
            180,
            190,
            200,
        ]
        self.moliere_radii = np.array([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
        distance = 2500
        theta = np.arctan(self.moliere_radii / distance)

        self.s1_thicknesses_G4 = moliere_to_thickness(200, theta, 355.2)
        self.s1_thicknesses_Al = moliere_to_thickness(200, theta, 88.97)
        self.s1_thicknesses_St = moliere_to_thickness(200, theta, 17.57)
        self.s1_thicknesses_Ta = moliere_to_thickness(200, theta, 4.094)

        self.all_thicknesses = [
            self.s1_thicknesses_G4,
            self.s1_thicknesses_Al,
            self.s1_thicknesses_St,
            self.s1_thicknesses_Ta,
        ]

        self.energy_spreads = [0, 0.25, 0.5, 0.75, 1]
        self.materials = [
            "G4NYLON",
            "Aluminum",
            "Steel",
            "Tantalum",
        ]
        self.material_X = [355.2, 88.97, 17.57, 4.094]
        self.radii = [1, 3]
        self.angles = [1, 3]
        # nominal values kept constant during variation of other parameters
        self.nominal_values_Al = {
            "Material": "Aluminum",
            "Energy": 150,
            "s1_thickness": 5,
            "Energy_spread": 0.5,
            "Radius": 1,
            "Angular_radius": 1,
        }
        self.all_values_Al = {
            "Material": self.materials,
            "Energy": self.energies,
            "s1_thickness": self.s1_thicknesses_Al,
            "Energy_spread": self.energy_spreads,
            "Radius": self.radii,
            "Angular_radius": self.angles,
        }

    def display_single_phsp(self, param_array):
        (
            tps,
            eps,
            gps,
        ) = self.retrieve_phase_space(param_array)
        ps_list = [tps, eps, gps]
        fig, ax = plt.subplots(3, 3, figsize=[15, 15])
        lim = np.std(tps["X"])
        two_sigma = self.get_two_sigma(tps.copy(), lim)
        lim = two_sigma * 2.5
        lim_arr = [-lim, lim]
        tps = self.trim_to_radius(tps, lim)
        for i in range(len(ps_list)):
            ps = ps_list[i]

            ax[i][0].hist2d(ps["X"], ps["Y"], bins=100, range=[lim_arr, lim_arr])
            ax[i][0].set_xlabel("X [mm]")
            ax[i][0].set_ylabel("Y [mm]")
            ax[i][1].hist(ps["X"], bins=100, range=lim_arr)
            ax[i][1].set_xlabel("X [mm]")
            ax[i][1].set_ylabel("Density")
            ax[i][2].hist(ps["Y"], bins=100, range=lim_arr)
            ax[i][2].set_xlabel("Y [mm]")
            ax[i][2].set_ylabel("Density")

    def construct_sigma_table(self):
        def get_stat_params(param_array, moliere_sigma):
            (
                tps,
                eps,
                gps,
            ) = self.retrieve_phase_space(param_array)
            radius = moliere_sigma * 3
            eps = self.trim_to_radius(eps, radius)
            return np.std(eps["X"])

        for i in range(len(self.all_thicknesses)):
            total_lengths = (
                len(self.energies) * len(self.all_thicknesses[i]) * 5 * 2 * 2
            )
            sigma_table = np.zeros(
                [len(self.energies), len(self.all_thicknesses[i]), 5, 2, 2]
            )
            moliere_table = np.load("/home/robertsoncl/topas/moliere_sigma_table.npy")
            count = 1

            for j in range(len(self.energies)):
                for k in range(len(self.all_thicknesses[i])):
                    for l in range(len(self.energy_spreads)):
                        for m in range(len(self.radii)):
                            for n in range(len(self.angles)):
                                moliere_sigma = moliere_table[j][k][l][m][n]
                                sigma_table[j][k][l][m][n] = get_stat_params(
                                    [
                                        self.energies[j],
                                        self.all_thicknesses[i][k],
                                        self.energy_spreads[l],
                                        self.radii[m],
                                        self.angles[n],
                                        False,
                                    ],
                                    moliere_sigma,
                                )
                                print(
                                    str(count) + "/" + str(total_lengths) + " completed"
                                )
                                count = count + 1
            np.save(
                "/home/robertsoncl/topas/sigma_table_" + str(self.materials[i]),
                sigma_table,
            )

    def construct_moliere_table(self):
        def moliere_scattering_sigma(
            material_X, energy, s1_thickness, radius, angular_radius, distance=2500
        ):
            def moliere_angle(E, X, d):
                # theta = (14.1 / E) * np.sqrt(d / X) * (1 + (1 / 9) * np.log10(d / X))
                theta = (14 / (E / 1000)) * np.sqrt(d / X)
                return theta

            def get_final_sigma(init_sigma, init_theta, moliere_theta, d=2500):
                total_theta = np.sqrt(init_theta ** 2 + moliere_theta ** 2)
                final_sigma = d / 1000 * np.tan(total_theta / 1000)
                return final_sigma * 1000

            moliere_theta = moliere_angle(energy, material_X, s1_thickness)
            final_sigma = get_final_sigma(
                radius, angular_radius, moliere_theta, distance
            )
            return final_sigma

        for i in range(len(self.all_thicknesses)):
            total_lengths = (
                len(self.energies) * len(self.all_thicknesses[i]) * 5 * 2 * 2
            )
            sigma_table = np.zeros(
                [len(self.energies), len(self.all_thicknesses[i]), 5, 2, 2]
            )
            moliere_table = np.load("/home/robertsoncl/topas/moliere_sigma_table.npy")
            count = 1

            for j in range(len(self.energies)):
                for k in range(len(self.all_thicknesses[i])):
                    for l in range(len(self.energy_spreads)):
                        for m in range(len(self.radii)):
                            for n in range(len(self.angles)):

                                sigma_table[j][k][l][m][n] = moliere_scattering_sigma(
                                    self.material_X[i],
                                    self.energies[j],
                                    self.all_thicknesses[i][k],
                                    self.radii[m],
                                    self.angles[n],
                                )
                                print(
                                    str(count) + "/" + str(total_lengths) + " completed"
                                )
                                count = count + 1
            np.save(
                "/home/robertsoncl/topas/moliere_sigma_table_" + str(self.materials[i]),
                sigma_table,
            )

    def retrieve_nominal_1D_array(self, filename, varied_coordinate):
        array = np.load(filename)
        table = xr.DataArray(
            array,
            coords={
                "Material": self.materials,
                "Energy": self.energies,
                "s1_thickness": self.s1_thicknesses,
                "Energy_spread": self.energy_spreads,
                "Radius": self.radii,
                "Angular radius": self.angles,
            },
        )
        self.nominal_values[varied_coordinate] = self.all_values[varied_coordinate]
        plotting_table = table.loc[self.nominal_values]
        print(plotting_table)
        return plotting_table

    def retrieve_multi_nominal_1D_array(self, filename, varied_coordinates):
        array = np.load(filename)
        table = xr.DataArray(
            array,
            coords={
                "Material": self.materials,
                "Energy": self.energies,
                "s1_thickness": self.s1_thicknesses,
                "Energy_spread": self.energy_spreads,
                "Radius": self.radii,
                "Angular radius": self.angles,
            },
        )
        self.nominal_values[varied_coordinates[0]] = self.all_values[
            varied_coordinates[0]
        ]
        self.nominal_values[varied_coordinates[1]] = self.all_values[
            varied_coordinates[1]
        ]
        new_dict = {
            varied_coordinates[0]: self.nominal_values[varied_coordinates[0]],
            varied_coordinates[1]: self.nominal_values[varied_coordinates[1]],
        }
        plotting_table = table.loc[self.nominal_values]
        plotting_tables = []
        print(self.all_values[varied_coordinates[1]])
        for i in self.all_values[varied_coordinates[1]]:
            new_dict[varied_coordinates[1]] = i
            plotting_tables.append(plotting_table.loc[new_dict])
        return plotting_tables

    # how many dimensions?
    # create empty numpy array in correct shape

    # loop through and fill everything up
    # convert to xarray and save for further processing
    # convert to xarray and save for further processing

    # how many dimensions?
    # create empty numpy array in correct shape

    # loop through and fill everything up
    # convert to xarray and save for further processing
    # convert to xarray and save for further processing
