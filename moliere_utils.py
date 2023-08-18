import numpy as np
from scipy.optimize import minimize_scalar


class moliere_utils:
    def __init__(self):
        rad_lengths_mm = {
            '"Aluminum"': 88.97,
            '"Iron"': 17.57,
            '"Copper"': 14.36,
            '"Nylon"': 355.2,
            '"Tantalum"': 4.094,
            '"Carbon"': 193.2,
            '"Gold"': 3.344,
            '"Lead"': 5.612,
        }
        self.rad_lengths_mm = rad_lengths_mm

        def get_scattered_spatial_sigma(
            init_sigma, init_psigma, init_energy, thickness, material
        ):
            def moliere_angle(E, X, d):
                theta = (
                    (14.1 / (E / 1000))
                    * np.sqrt(d / X)
                    * (1 + (1 / 9) * np.log10(d / X))
                )
                # theta = (14 / (E / 1000)) * np.sqrt(d / X)
                return theta

            def get_final_sigma(init_sigma, init_theta, moliere_theta, d):
                total_theta = np.sqrt(init_theta ** 2 + moliere_theta ** 2)
                final_sigma = d / 1000 * np.tan(total_theta / 1000) + init_sigma / 1000
                return final_sigma * 1000

            X = self.rad_lengths_mm[material]
            moliere_theta = moliere_angle(init_energy, X, thickness)
            final_sigma = get_final_sigma(init_sigma, init_psigma, moliere_theta, 2500)
            return final_sigma

        self.get_scattered_spatial_sigma = get_scattered_spatial_sigma

    def solve_moliere_for_thickness(
        self, init_sigma, init_psigma, init_energy, material, sigma_aim
    ):
        def merit(thickness):
            result = self.get_scattered_spatial_sigma(
                init_sigma, init_psigma, init_energy, thickness, material
            )
            return ((result / sigma_aim) - 1) ** 2

        simp = minimize_scalar(merit)
        return simp.x

    def get_thickness_for_scattered_spatial_sigma(
        self, init_sigma, init_psigma, init_energy, final_sigma, material
    ):
        def get_moliere_angle(init_sigma, init_theta, d):
            total_theta = (
                np.arctan((final_sigma / 1000 - init_sigma / 1000) / (d / 1000)) * 1000
            )
            moliere_theta = np.sqrt(total_theta ** 2 - init_theta ** 2)
            return moliere_theta

        def moliere_scattering_thickness(
            material_X,
            energy,
            theta,
        ):
            thickness = (material_X * theta ** 2) / (14 / (energy / 1000)) ** 2
            return thickness

        theta = get_moliere_angle(init_sigma, init_psigma, 2500)
        X = self.rad_lengths_mm[material]
        thickness = moliere_scattering_thickness(X, init_energy, theta)
        return thickness


# print(mu.get_thickness_for_scattered_spatial_sigma(1, 1, 200, 75, "Aluminum"))

# print(mu.get_thickness_for_scattered_spatial_sigma(1, 1, 200, 75, "Aluminum"))
