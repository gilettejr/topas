from new_gaussian_optimiser_utils import dual_optimiser_utils
from new_foil_plotting_utils import new_foil_plotting_utils
import numpy as np
from scipy.optimize import minimize


def optimise_gat_lattice_flexible(N_runs, N_particles, s1_thickness, col_aim):

    # lattice params should be container of three containers
    # internal containers are quad strengths drift lengths, dipole angles
    # signatures should be lists of element names in string format, in order quads, dip_strengths, drift positions
    # same order required
    def merit(opt, s1_thickness, col_aim):

        dou = dual_optimiser_utils()
        dou.generate_beam(1, 1, 1, 1, 200, 0.05, N_particles)
        s2_thickness = opt[0]
        s2_sigma = opt[1]
        s2_radius = opt[2]
        sigma_convolution_factor = opt[3]
        dou.add_foils(
            s1_thickness,
            s2_thickness,
            400,
            1500,
            "Nylon",
            "Nylon",
            N_slices=10,
            s2_sigma=s2_sigma,
            s2_radius=s2_radius,
            sigma_convolution_factor=sigma_convolution_factor,
            view_setup=False,
        )
        dou.topas_run()
        print(opt)
        nfu = new_foil_plotting_utils("S2_beam.phsp")
        phsp = nfu.phsp_dict["e"]
        X = phsp["X"]
        Y = phsp["Y"]
        Rx = col_aim
        Ry = col_aim
        rad_range = []
        PRC = np.arange(5, 100, step=5)

        PRC_ud_list = [
            -0.805383421768330,
            -0.687040738956703,
            -0.585132833776080,
            -0.491868616246095,
            -0.403971193323003,
            -0.319684872146710,
            -0.237886465050237,
            -0.157742675776924,
            -7.862070319742011e-02,
            0,
            7.862070319742012e-02,
            0.157742675776924,
            0.237886465050237,
            0.319684872146710,
            0.403971193323002,
            0.491868616246095,
            0.585132833776080,
            0.687040738956703,
            0.805383421768329,
        ]
        M = 0
        N = 8
        phid = np.linspace(0, np.pi, N + 1)[:N]
        for i in phid:
            P = X * np.cos(i) + Y * np.sin(i)
            r = col_aim
            for j in range(len(PRC)):
                if PRC[j] == 50:
                    M = M + 2000 * (np.percentile(P, PRC[j]) / r) ** 2
                else:
                    M = (
                        M
                        + 2000
                        * (np.percentile(P, PRC[j]) / (PRC_ud_list[j] * r) - 1) ** 2
                    )
        lim = col_aim ** 2
        outside = []
        for i in X.index:
            if X[i] ** 2 + Y[i] ** 2 > lim:
                outside.append(0)
        num_removed = len(outside)
        M = M + num_removed

        return M

    M_min = np.inf

    bounds = [[5, 20], [1, 5], [3, 20], [1, 4]]

    for i in range(N_runs):
        initial_guesses = []
        for j in bounds:
            initial_guesses.append(np.random.uniform(low=j[0], high=j[1]))
        # initial_guesses = [10, 2, 6, 0.9]
        result = minimize(
            merit,
            x0=initial_guesses,
            bounds=bounds,
            args=(s1_thickness, col_aim),
            method="Nelder-Mead",
        )

        M = result.fun
        x = result.x
        print("Run " + str(i) + " complete")
        print("Value of Merit Function:" + str(M))
        if M < M_min:
            M_min = M
            x_min = x

    print("Best Solution: ")
    print(x_min)
    print("Function Result: ")
    print(M_min)


optimise_gat_lattice_flexible(50, 10000, 5, 15)
