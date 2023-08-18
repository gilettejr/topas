from thickness_optimiser_utils import thickness_optimiser_utils
from s1_paper_utils import s1_paper_utils
import numpy as np
import matplotlib.pyplot as plt


def generate_phsps():
    def moliere_to_thickness(energy, theta, X):
        d = X * (energy * theta / 14) ** 2
        return d

    energies = [
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
    moliere_radii = np.array([0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200])
    distance = 2500
    theta = np.arctan(moliere_radii / distance)
    s1_thicknesses_G4 = moliere_to_thickness(200, theta, 355.2)
    s1_thicknesses_Al = moliere_to_thickness(200, theta, 88.97)
    s1_thicknesses_St = moliere_to_thickness(200, theta, 17.57)
    s1_thicknesses_Ta = moliere_to_thickness(200, theta, 4.094)

    all_thicknesses = [
        s1_thicknesses_G4,
        s1_thicknesses_Al,
        s1_thicknesses_St,
        s1_thicknesses_Ta,
    ]
    energy_spreads = [0, 0.25, 0.5, 0.75, 1]
    materials = [
        ['"G4_NYLON-6-6"', "G4NYLON"],
        ['"Aluminum"', "Aluminum"],
        ['"Steel"', "Steel"],
        ['"Tantalum"', "Tantalum"],
    ]
    initial_dists = [(1, 1), (3, 3), (1, 3), (3, 1)]
    tou = thickness_optimiser_utils()
    for a in range(len(all_thicknesses)):
        for i in energy_spreads:
            for k in initial_dists:
                for l in range(len(all_thicknesses[a])):
                    tou.run_through_uniform_foil_for_paper(
                        all_thicknesses[a][l],
                        materials[a][0],
                        materials[a][1],
                        10000,
                        160,
                        i,
                        k[0],
                        k[1],
                        False,
                    )


def plot_single_relationship(filename, varied_coordinate):
    ut = s1_paper_utils()
    ds = ut.retrieve_nominal_1D_array(filename, varied_coordinate)
    ds.plot()


def plot_multi_relationship(filename, varied_coordinates):
    ut = s1_paper_utils()
    ds = ut.retrieve_multi_nominal_1D_array(filename, varied_coordinates)
    for i in ds:
        i.plot()


def main():
    generate_phsps()

    # ut = s1_paper_utils()
    # plot_multi_relationship(
    #    "/home/robertsoncl/topas/sigma_table.npy", ["s1_thickness", "Energy"]
    # )
    # ut.display_single_phsp(["Aluminum", 100, 1, 0, 1, 1, False])
    # ut.construct_moliere_table()


main()
main()
