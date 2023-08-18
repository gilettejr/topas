from thickness_optimiser_utils import thickness_optimiser_utils
import numpy as np

# moliere = thickness_optimiser_utils()
# moliere.run_through_uniform_foil_from_generated_beam(
#    7.514, 575, '"Aluminum"', energy=200, N=100000
# )
# moliere.get_X_Y("scattered_beam")
# two_sigma = moliere.get_two_sigma(max_radius=400, bins=80)
# print(two_sigma / 2)
# moliere.plot_transverse_beam()
X_ny = 355.2
X_al = 88.97
X_st = 17.57
X_pb = 5.612
X_tg = 3.504
X_ka = 285.7

E = 200

# angle aims
# 10 - 11.745
# 20 - 16.610
# 30 - 20.343


def moliere_scattering_angle(material_X, energy, s1_thickness):
    def moliere_angle(E, X, d):
        # theta = (14.1 / E) * np.sqrt(d / X) * (1 + (1 / 9) * np.log10(d / X))
        theta = (14 / (E / 1000)) * np.sqrt(d / X)
        return theta

    moliere_angle = moliere_angle(energy, material_X, s1_thickness)
    return moliere_angle


def moliere_scattering_thickness(
    material_X,
    energy,
    theta,
):
    d = (material_X * theta ** 2) / (14 / (energy / 1000)) ** 2
    return d


# print(moliere_scattering_angle(X_ny, 200, 20))
# print(moliere_scattering_thickness(X_tg, 200, 20.343))
from thickness_optimiser_utils import thickness_optimiser_utils
import numpy as np

# moliere = thickness_optimiser_utils()
# moliere.run_through_uniform_foil_from_generated_beam(
#    7.514, 575, '"Aluminum"', energy=200, N=100000
# )
# moliere.get_X_Y("scattered_beam")
# two_sigma = moliere.get_two_sigma(max_radius=400, bins=80)
# print(two_sigma / 2)
# moliere.plot_transverse_beam()
X_ny = 355.2
X_al = 88.97
X_st = 17.57
X_pb = 5.612
X_tg = 3.504
X_ka = 285.7

E = 200

# angle aims
# 10 - 11.745
# 20 - 16.610
# 30 - 20.343


def moliere_scattering_angle(material_X, energy, s1_thickness):
    def moliere_angle(E, X, d):
        # theta = (14.1 / E) * np.sqrt(d / X) * (1 + (1 / 9) * np.log10(d / X))
        theta = (14 / (E / 1000)) * np.sqrt(d / X)
        return theta

    moliere_angle = moliere_angle(energy, material_X, s1_thickness)
    return moliere_angle


def moliere_scattering_thickness(
    material_X,
    energy,
    theta,
):
    d = (material_X * theta ** 2) / (14 / (energy / 1000)) ** 2
    return d


# print(moliere_scattering_angle(X_ny, 200, 20))
# print(moliere_scattering_thickness(X_tg, 200, 20.343))
