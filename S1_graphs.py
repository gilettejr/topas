import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


class S1_graphs:
    def __init__(self, filename="material_classifications/smart_electron_results"):
        def dist_to_angle(distance):
            angles = np.arctan(100 / distance)
            return angles

        def relabel_legend(position="lower left"):
            plt.legend(
                loc=position,
                labels=["Aluminium", "Lead", "Copper", "Tantalum", "Titanium"],
            )

        def relabel_legend_nylon(position="lower left"):
            plt.legend(loc=position, labels=["Nylon"])

        run_data = pd.read_parquet(filename)
        # sns.set_style("darkgrid")
        self.run_data = run_data
        if filename == "material_classifications/nylon_result":
            self.relabel_legend = relabel_legend_nylon
        else:
            self.relabel_legend = relabel_legend

    def plot_thickness_against_angle(self, initial_beam_energy=100):
        run_data = self.run_data
        run_data["Scattering Angle"] = (np.arctan(100 / run_data["Distance"])) * 1000
        # sm_data = run_data.loc[run_data["Initial_Beam_E"] == initial_beam_energy]
        sns.scatterplot(
            data=run_data,
            y="Scattering Angle",
            x="Thickness",
            hue="Material",
        )
        plt.xlabel("S1 Thickness (mm)")
        plt.ylabel("Scattering Angle (mrad)")
        plt.xlim([0, 25])
        # self.relabel_legend(position="lower right")

    def plot_thickness_against_initial_energy(self, material='"Tantalum"'):
        run_data = self.run_data
        run_data["Scattering Angle"] = round(
            np.arctan(100 / run_data["Distance"]) * 1000, 1
        )
        sm_data = run_data.loc[run_data["Material"] == material]
        sns.scatterplot(
            data=sm_data,
            y="Thickness",
            x="Initial_Beam_E",
            hue="Scattering Angle",
        )
        plt.ylabel("S1 Thickness (mm)")
        plt.xlabel("Initial Beam Energy (MeV)")
        plt.legend(title="Scattering Angle (mrad)")
        plt.ylim([0, 1.5])

    def plot_thickness_against_gamma_no_material(self, initial_beam_energy=100):
        run_data = self.run_data
        run_data["Scattering Angle"] = (
            round(np.arctan(100 / run_data["Distance"]), 3) * 1000
        )
        x = np.arctan(100 / run_data["Distance"]) * 1000
        xnew = np.linspace(x.min(), x.max(), 50)

        y = 10000 / run_data["gamma_number"]
        run_data["ratio"] = y
        sm_data = run_data.loc[run_data["Initial_Beam_E"] == initial_beam_energy]
        sns.scatterplot(
            data=sm_data,
            x="Scattering Angle",
            y="ratio",
            hue="Material",
        )
        # self.relabel_legend(position="upper right")
        plt.xlabel("Scattering Angle (mrad)")
        plt.ylabel("electron/photon ratio at patient")

    def plot_gamma_against_initial_energy(self, material='"Tantalum"'):
        run_data = self.run_data
        run_data["Scattering Angle"] = round(np.arctan(100 / run_data["Distance"]), 3)
        sm_data = run_data.loc[run_data["Material"] == material]
        sns.scatterplot(
            data=sm_data,
            x="Initial_Beam_E",
            y="gamma_number",
            hue="Scattering Angle",
        )

    def plot_angle_against_electron_energy(self):

        run_data = self.run_data
        run_data["Scattering Angle"] = np.arctan(100 / run_data["Distance"]) * 1000
        sns.scatterplot(
            data=run_data,
            x="Scattering Angle",
            y="Mean_E_Collimated",
            hue="Material",
        )
        plt.ylabel("Mean Energy at Patient (MeV)")
        plt.xlabel("Scattering Angle (mrad)")
        # self.relabel_legend()


plotter = S1_graphs()
# plotter.plot_angle_against_electron_energy()
# plotter.plot_thickness_against_angle()
# plotter.plot_thickness_against_initial_energy()
plotter.plot_thickness_against_angle()
