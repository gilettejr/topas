import numpy as np


def transport_through_material(matrix, t, material):
    def rms(vector):
        rms = np.sqrt(np.divide(1, len(vector)) * np.sum(np.square(vector)))
        return rms

    # units in mrad, mm, MeV
    def scattering_kick(position_vector, t, X_0):
        kick = (
            np.divide(13.6, 100)
            * np.sqrt(t / X_0)
            * position_vector
            * (1 + 0.038 * np.log(t / X_0))
        )
        return kick

    elements = ["x", "x_prime", "y", "y_prime", "t", "P", "m", "Q"]
    # mm
    X_0 = 88.97
    x = matrix[0]
    x_prime = matrix[1]
    y = matrix[2]
    y_prime = matrix[3]
    x_scattering_kick = scattering_kick(x, t, X_0)
    y_scattering_kick = scattering_kick(y, t, X_0)
    x_prime_new = np.sqrt(np.square(x_prime) + np.square(x_scattering_kick))
    y_prime_new = np.sqrt(np.square(y_prime) + np.square(y_scattering_kick))
