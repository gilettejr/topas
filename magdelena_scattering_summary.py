import numpy as np
import matplotlib.pyplot as plt
from thickness_optimiser_utils import thickness_optimiser_utils

# 120 for Nylon at 200 for 100mm radius
# 2.2 for Tantalum at 200 for 100mm radius
# 8ish for steel
# 30ish for aluminium
material_X = 355.2
water_X = 360
energy = 200
s1_thicknesses = [10, 20, 30]
radius = 1
angular_radius = 3
s1_placement = np.arange(0, 300, 1)
film_placement = np.arange(400, 700, 1)
water_depth = 300
tank_loc = 400
sigma_array = np.zeros([len(s1_placement), len(film_placement)])


def plot_moliere_predictions():
    def moliere_scattering_sigma_and_angle(
        material_X, energy, s1_thickness, radius, angular_radius, distance
    ):
        def moliere_angle(E, X, d):
            # theta = (14.1 / E) * np.sqrt(d / X) * (1 + (1 / 9) * np.log10(d / X))
            theta = (14 / (E / 1000)) * np.sqrt(d / X)
            return theta

        def get_final_sigma(init_sigma, init_theta, moliere_theta, d):
            total_theta = np.sqrt(init_theta ** 2 + moliere_theta ** 2)
            final_sigma = d / 1000 * np.tan(total_theta / 1000)
            return final_sigma * 1000

        moliere_theta = moliere_angle(energy, material_X, s1_thickness)
        final_sigma = get_final_sigma(radius, angular_radius, moliere_theta, distance)
        return final_sigma, moliere_theta

    for i in range(len(s1_placement)):
        for j in range(len(film_placement)):
            sigma_at_tank, angle_at_tank = moliere_scattering_sigma_and_angle(
                material_X,
                energy,
                30,
                radius,
                angular_radius,
                tank_loc - s1_placement[i],
            )
            sigma_at_film, angle_at_film = moliere_scattering_sigma_and_angle(
                water_X,
                energy,
                (film_placement[j] - 400) / 2,
                sigma_at_tank,
                angle_at_tank,
                (film_placement[j] - 400) / 2,
            )
            sigma_array[i][j] = sigma_at_film + sigma_at_tank

    plt.imshow(sigma_array, interpolation="nearest")
    plt.ylabel("S1 Placement from Beam Pipe Exit [mm]")
    plt.xlabel("Film Placement from Tank Window [mm]")
    cbar = plt.colorbar()
    cbar.set_label("$\sigma$ at film [mm]")
    plt.title("30mm Scatterer")


plot_moliere_predictions()
# tou = thickness_optimiser_utils()
# tou.run_through_uniform_foil_from_generated_beam(
#    10, 1000, '"Aluminum"', N=100000, energy=100
# )
# tou.get_X_Y("scattered_beam")
# tou.plot_transverse_beam()

# plot_moliere_predictions()
