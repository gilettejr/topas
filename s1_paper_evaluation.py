import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.modeling import models, fitting
from new_s1_paper_utils import new_s1_paper_utils
from moliere_utils import moliere_utils
from scipy.stats import sem


def fit_2D_gaussian(x, y, fit_radius=150, bins=100):
    data_sim, x_edges, y_edges = np.histogram2d(
        x, y, bins=bins, range=[
            [-fit_radius, fit_radius], [-fit_radius, fit_radius]]
    )
    x_centres = (x_edges[:-1] + x_edges[1:]) / 2
    y_centres = (y_edges[:-1] + y_edges[1:]) / 2
    x, y = np.meshgrid(x_centres, y_centres)
    model = models.Gaussian2D()
    fitter = fitting.LevMarLSQFitter()
    fit_data = fitter(model, x, y, data_sim)
    err_params = np.sqrt(np.diag(fitter.fit_info["param_cov"]))
    return fit_data, x, y, err_params[3], err_params[4]


def fit_1D_lorentzian(x, max_radius=150, bins=100):
    # retrieve X data (rotationally symmetric, Y not required)

    # initiate Astropy Gaussian model with arbitrary initial values

    hist, bin_edges = np.histogram(
        x, bins=bins, range=[-max_radius, max_radius])
    # define X coordinates as bin centres rather than edges
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    # initialise LSQ fitter (fast, more complex fitter not necessary)
    fitter = fitting.LevMarLSQFitter()
    g_init = models.Lorentz1D()
    # carry out gaussian fit over data
    g = fitter(g_init, bin_centres, hist)
    err_params = np.sqrt(np.diag(fitter.fit_info["param_cov"]))
    return g, err_params[2]


def fit_1D_gaussian(x, max_radius=150, bins=100):
    # retrieve X data (rotationally symmetric, Y not required)

    # initiate Astropy Gaussian model with arbitrary initial values

    hist, bin_edges = np.histogram(
        x, bins=bins, range=[-max_radius, max_radius])
    # define X coordinates as bin centres rather than edges
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    # initialise LSQ fitter (fast, more complex fitter not necessary)
    fit_g = fitting.LevMarLSQFitter()
    g_init = models.Gaussian1D()
    # carry out gaussian fit over data
    g = fit_g(g_init, bin_centres, hist)

    return g


def get_slices(phsp, slice_width=1):
    phsp_xslice = phsp[(phsp["Y"] < slice_width)]
    phsp_xslice = phsp_xslice[(phsp_xslice["Y"] > -slice_width)]
    phsp_yslice = phsp[(phsp["X"] < slice_width)]
    phsp_yslice = phsp_yslice[(phsp_yslice["X"] > -slice_width)]
    return phsp_xslice, phsp_yslice


# 18.34567
def evaluate(
    thickness=18.34567,
    material='"Aluminum"',
    distance=2500,
    energy=200,
    delta_E=0,
    beam_dist="Gaussian",
    beam_pdist="Gaussian",
    xy_rad=1,
    pxy_rad=1,
    N=10000000,
    rerun=False,
    evaluate=True,
):
    utils = new_s1_paper_utils()
    mu = moliere_utils()
    e_moliere_sigma = mu.get_scattered_spatial_sigma(
        xy_rad, pxy_rad, energy, thickness, material
    )
    if rerun is True:
        utils.run_through_uniform_foil_from_generated_beam(
            thickness,
            material,
            distance,
            energy,
            delta_E,
            beam_dist,
            beam_pdist,
            xy_rad,
            pxy_rad,
            N,
        )

        phsp_dict = utils.get_X_Y()
        print("done")
        e = phsp_dict["e"]
        phot = phsp_dict["y"]
        ps = phsp_dict["p"]
        e.to_parquet(
            "/home/robertsoncl/s1_paper_data/e"
            + str(thickness)
            + material
            + str(energy)
            + str(delta_E)
            + beam_dist
            + beam_pdist
            + str(xy_rad)
            + str(pxy_rad)
        )
        phot.to_parquet(
            "/home/robertsoncl/s1_paper_data/y"
            + str(thickness)
            + material
            + str(energy)
            + str(delta_E)
            + beam_dist
            + beam_pdist
            + str(xy_rad)
            + str(pxy_rad)
        )
        ps.to_parquet(
            "/home/robertsoncl/s1_paper_data/p"
            + str(thickness)
            + material
            + str(energy)
            + str(delta_E)
            + beam_dist
            + beam_pdist
            + str(xy_rad)
            + str(pxy_rad)
        )
    else:
        e = pd.read_parquet(
            "/home/robertsoncl/s1_paper_data/e"
            + str(thickness)
            + material
            + str(energy)
            + str(delta_E)
            + beam_dist
            + beam_pdist
            + str(xy_rad)
            + str(pxy_rad)
        )
        phot = pd.read_parquet(
            "/home/robertsoncl/s1_paper_data/y"
            + str(thickness)
            + material
            + str(energy)
            + str(delta_E)
            + beam_dist
            + beam_pdist
            + str(xy_rad)
            + str(pxy_rad)
        )
        ps = pd.read_parquet(
            "/home/robertsoncl/s1_paper_data/p"
            + str(thickness)
            + material
            + str(energy)
            + str(delta_E)
            + beam_dist
            + beam_pdist
            + str(xy_rad)
            + str(pxy_rad)
        )
    if evaluate is True:
        y_slice_x, y_slice_y = get_slices(phot)
        p, x, y, unc_x, unc_y = fit_2D_gaussian(
            e["X"], e["Y"], e_moliere_sigma)
        e_sig = np.mean([p.x_stddev.value, p.y_stddev.value])
        e_sig_unc = max(unc_x, unc_y)
        print("e_sigma=" +
              str(np.mean([p.x_stddev.value, p.y_stddev.value])) + "mm")
        print("e_sigma_err= " + str(max(unc_x, unc_y)) + "mm")
        print("Mean Energy of e: " + str(np.mean(e["E"])) + "MeV")
        print("Error of Energy of e: " + str(sem(e["E"])) + "MeV")

        g, rms_err = fit_1D_lorentzian(y_slice_x["X"], e_moliere_sigma)

        print("y_fwhm=" + str(g.fwhm) + "mm")
        print("y_fwhm_err= " + str(rms_err) + "mm")
        print("Mean Energy of y: " + str(np.mean(phot["E"])) + "MeV")
        print("Error of Energy of y: " + str(sem(phot["E"])) + "MeV")

        # p, x, y, unc_x, unc_y = fit_2D_gaussian(
        #    ps["X"], ps["Y"], e_moliere_sigma * 2, bins=50
        # )

        # print("p_sigma=" + str(np.mean([p.x_stddev.value, p.y_stddev.value])) + "mm")
        # print("p_sigma_err= " + str(max(unc_x, unc_y)) + "mm")
        print("Mean Energy of p: " + str(np.mean(ps["E"])) + "MeV")
        print("Error of Energy of p: " + str(sem(ps["E"])) + "MeV")

        total_part_no = len(e) + len(phot) + len(p)
        e_per = (len(e) / total_part_no) * 100
        y_per = (len(phot) / total_part_no) * 100
        ps_per = (len(ps) / total_part_no) * 100

        print(
            "Final beam composition:"
            + str(e_per)
            + "% electrons,"
            + str(y_per)
            + "% photons,"
            + str(ps_per)
            + "% positrons"
        )
        print("Moliere prediction=" + str(e_moliere_sigma) + "mm")
        paper_stats = pd.DataFrame(
            {
                "e_sigma": e_sig,
                "e_sigma_unc": e_sig_unc,
                "y_rms": g.fwhm.value,
                "y_rms_unc": rms_err,
                "mean_e": np.mean(e["E"]),
                "mean_e_y": np.mean(phot["E"]),
                "mean_p": np.mean(ps["E"]),
                "e_N": e_per,
                "y_N": y_per,
                "p_N": ps_per,
                "mol_sigma": e_moliere_sigma,
            },
            index=[0],
        )
        paper_stats.to_parquet(
            "/home/robertsoncl/s1_paper_stats/"
            + str(round(thickness, 5))
            + material
            + str(energy)
            + str(delta_E)
            + beam_dist
            + beam_pdist
            + str(xy_rad)
            + str(pxy_rad)
        )


energies = [50, 75, 100, 125, 150, 175, 200, 225, 250]
r = [0.25, 0.5, 0.75, 1, 2]
pr = [0.25, 0.5, 0.75, 1, 2, 34, 5]
e_var = [0.25, 0.5, 0.75, 1]
thicknesses = [
    2,
    4,
    6,
    8,
    10,
    12,
    14,
    16,
    18,
    20,
    22,
    24,
    26,
    28,
    30,
    32,
    34,
    36,
    38,
    40,
]
elements = [
    '"Iron"',
    '"Copper"',
    '"Nylon"',
    '"Tantalum"',
    '"Carbon"',
    '"Gold"',
    '"Lead"',
]
# mu = moliere_utils()

# for i in elements:
#    et = mu.solve_moliere_for_thickness(1, 1, 200, i, 75)
#    evaluate(
#        material=i,
#        thickness=et,
#        rerun=True,
#        xy_rad=1,
#        pxy_rad=1,
#        delta_E=0,
#        evaluate=False,
#    )
# evaluate(
#     38,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#     36,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#     34,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#     32,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#     30,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#     28,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#     26,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#     24,
#     '"Aluminum"',
#     rerun=True,
#     xy_rad=1,
#     pxy_rad=1,
#     delta_E=0,
#     evaluate=False,
# )
# evaluate(
#    40,
#    '"Aluminum"',
#    rerun=True,
#    xy_rad=1,
#    pxy_rad=1,
#    delta_E=0,
#    evaluate=False,
# )
#    '"Aluminum"',
#    rerun=True,
#    xy_rad=1,
#    pxy_rad=1,
#    delta_E=0,
#    evaluate=False,
# )
