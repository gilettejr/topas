from ttb_topas_optimiser import (
    optimise_downstream_lattice,
    optimise_downstream_lattice_vary_width,
)
from mlc_topas_optimiser import optimise_downstream_lattice_mlc_vary_width
from topas_ttb_runners import topas_ttb_runners
import sys

sys.path.append("/home/robertsoncl/dphil/rf-track-2.0")
from rf_track_ttb_runner import rf_track_ttb_runner
from rf_optimisers import optimise_upstream_lattice


def do_clear_test(N):
    rf = rf_track_ttb_runner(N=N)
    rf.generate_twiss_beam()


def do_master_optimisation(upstream_opts=10, downstream_opts=1, vary_width=False):
    input_params = optimise_upstream_lattice(upstream_opts, 1000)
    rf = rf_track_ttb_runner(N=10000)
    rf.run_through_upstream_lattice(
        [input_params[0], input_params[1]],
        [input_params[2] / 1000, input_params[3] / 1000, input_params[4] / 1000],
        [input_params[5], input_params[6]],
    )

    rf.export_phsp()
    rf.write_header()
    if vary_width is False:
        optimise_downstream_lattice(downstream_opts, 10000)
    else:
        optimise_downstream_lattice_vary_width(downstream_opts, 10000, 1500)
    print(input_params)


def do_mlc_optimisation(upstream_opts=10, downstream_opts=1):
    input_params = optimise_upstream_lattice(upstream_opts, 1000)
    rf = rf_track_ttb_runner(N=10000)
    rf.run_through_upstream_lattice(
        [input_params[0], input_params[1]],
        [input_params[2] / 1000, input_params[3] / 1000, input_params[4] / 1000],
        [input_params[5], input_params[6]],
    )

    rf.export_phsp()
    rf.write_header()
    s1_runner = topas_ttb_runners()
    s1_runner.run_through_s1(70)
    optimise_downstream_lattice_mlc_vary_width(
        downstream_opts, 10000, 20, set_S1_to_S2=1500, method="DE"
    )
    print(input_params)


def do_mlc_optimisation_topas(upstream_opts=10, downstream_opts=1):
    s1_runner = topas_ttb_runners()
    s1_runner.run_through_s1(70)
    optimise_downstream_lattice_mlc_vary_width(
        downstream_opts, 10000, 20, set_S1_to_S2=1500, method="DE"
    )


# do_mlc_optimisation(1, 1)


def do_topas_optimisation():
    optimise_downstream_lattice(9, 10000)


def do_single_optimisation_with_specific_params(
    N_particles, upstream_input_params, downstream_input_params
):

    rf = rf_track_ttb_runner(N=N_particles)
    rf.run_through_upstream_lattice(
        [upstream_input_params[0], upstream_input_params[1]],
        [
            upstream_input_params[2] / 1000,
            upstream_input_params[3] / 1000,
            upstream_input_params[4] / 1000,
        ],
        [upstream_input_params[5], upstream_input_params[6]],
    )
    rf.export_phsp()
    rf.write_header()
    topas = topas_ttb_runners()
    optimise_downstream_lattice_vary_width(
        1, N_particles, initial_params=downstream_input_params, set_S1_to_S2=2000
    )


# do_master_optimisation(10, 1, vary_width=True)
def view_beam_at_s1(N_particles, upstream_input_params):
    rf = rf_track_ttb_runner(N=N_particles)
    rf.run_through_upstream_lattice(
        [upstream_input_params[0], upstream_input_params[1]],
        [
            upstream_input_params[2] / 1000,
            upstream_input_params[3] / 1000,
            upstream_input_params[4] / 1000,
        ],
        [upstream_input_params[5], upstream_input_params[6]],
    )
    rf.export_phsp()
    rf.write_header()
    plotter = topas_ttb_runners()
    plotter.get_X_Y("ttb_run_data/rf_track_result.phsp")
    plotter.plot_transverse_beam()


def do_specific_run(
    N_particles,
    upstream_input_params,
    downstream_input_params,
    vary_width=False,
    show_shape=False,
):
    rf = rf_track_ttb_runner(N=N_particles)
    rf.run_through_upstream_lattice(
        [upstream_input_params[0], upstream_input_params[1]],
        [
            upstream_input_params[2] / 1000,
            upstream_input_params[3] / 1000,
            upstream_input_params[4] / 1000,
        ],
        [upstream_input_params[5], upstream_input_params[6]],
    )
    rf.export_phsp()
    rf.write_header()
    topas = topas_ttb_runners()
    topas.run_through_s1(downstream_input_params[0])
    if vary_width is False:
        topas.run_through_s2(
            sigma=downstream_input_params[1],
            max_height=downstream_input_params[2],
            s1_to_s2_drift_space=downstream_input_params[3],
            show_shape=show_shape,
        )
    else:
        topas.run_through_s2_vary_width(
            sigma=downstream_input_params[1],
            max_height=downstream_input_params[2],
            s1_to_s2_drift_space=2000,
            width=downstream_input_params[3],
            show_shape=show_shape,
        )


standard_upstream_input_params = [
    -7.51416343e00,
    1.11806199e01,
    5.99999999e03,
    3.00000000e02,
    3.00000000e02,
    2.88117576e-01,
    7.85398163e-01,
]
downstream_input_params = [83.29862412, 6.70220049, 9.73833107, 837.94843254]
# s1 aim
# sigma
# height
# shape radius
downstream_input_params_vary_width = [
    80.39280208,
    10.54646922,
    28.526354667,
    100.09263212,
]
# do_specific_run(
#    1000000,
#    standard_upstream_input_params,
#    downstream_input_params_vary_width,
#    vary_width=True,
#    show_shape=True,
# )


def plot_final_beam():
    topas = topas_ttb_runners()
    topas.get_X_Y("S2_beam.phsp")
    topas.plot_transverse_beam()


plot_final_beam()
# do_single_optimisation_with_specific_params(
#    10000, standard_upstream_input_params, downstream_input_params_vary_width
# )
# plot_final_beam()
# view_beam_at_s1(1000000, standard_upstream_input_params)
# plot_final_beam()
# plot_final_beam()
# view_beam_at_s1(1000000, standard_upstream_input_params)
# plot_final_beam()
# plot_final_beam()
# plot_final_beam()
# plot_final_beam()
