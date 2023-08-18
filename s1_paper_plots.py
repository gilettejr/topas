import matplotlib.pyplot as plt

import numpy as np
import xarray as xr
from s1_paper_utils import s1_paper_utils


class s1_paper_plots(s1_paper_utils):
    def plot_multi_moliere(self, element, varied_coordinate):
        m_xr = self.import_moliere_table(element=element)
        #        self.nominal_values[varied_coordinate] = self.all_values_Al[varied_coordinate]
        plotting_table = m_xr.loc[
            {"Energy_spread": 0, "Radius": 1, "Angular_radius": 1}
        ]
        plotting_table.plot(label=element)


def scattering_by_material_thickness():
    plotter = s1_paper_plots()
    plotter.plot_multi_moliere("G4NYLON", "s1_thickness")
    plotter.plot_multi_moliere("Aluminum", "s1_thickness")
    plotter.plot_multi_moliere("Steel", "s1_thickness")
    plotter.plot_multi_moliere("Tantalum", "s1_thickness")
    plt.title("Material Scattering Comparison at 200MeV")
    plt.xlabel("Scatterer Thickness")
    plt.ylabel("Moliere Beam $\sigma$")
    plt.legend()


def moliere_energy_variation():
    plotter = s1_paper_plots()
    plotter.plot_multi_moliere("G4NYLON", "energy")
    plotter.plot_multi_moliere("Aluminum", "energy")
    plotter.plot_multi_moliere("Steel", "energy")
    plotter.plot_multi_moliere("Tantalum", "energy")


moliere_energy_variation()
