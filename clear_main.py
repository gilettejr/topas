from clear_experiment_utils import clear_experiment_utils
from clear_phsp_optimiser import optimise_s2_for_clear
import numpy as np


def simulate_clear_run(scatterer_thickness, distance_to_screen, sigma_x, sigma_y):
    clear = clear_experiment_utils()
    clear.run_through_s1_clear(
        scatterer_thickness, distance_to_screen, sigma_x, sigma_y, N=100000
    )
    clear.get_X_Y("clear_beam_after_s1.phsp")
    clear.plot_transverse_beam()
    two_sig = clear.get_two_sigma(max_radius=50, bins=500)
    one_sig = two_sig / 2
    print(one_sig)


# optimise_s2_for_clear(
#    runs=1,
#    s1_thickness=10,
#    sigma_x=0.86,
#    sigma_y=1.14,
#    sigma_px=4.17,
#    sigma_py=3.26,
# )
# 330 + scat + 230
# 330+scat+230=330+
# 280+105+190
#
# dual scattering reality:p4.4,3.5
# pos 1.14,1.17
def simulate_s1_s2_clear_run(
    s1_thickness=30,
    s1_to_patient=575,
    sigma=19.52898,
    max_height=110.0,
    shape_radius=24.28,
):
    ceu = clear_experiment_utils()
    ceu.run_through_s1_and_s2_clear(
        s1_thickness,
        s1_to_patient,
        sigma,
        max_height,
        shape_radius,
        sigma_x=1.14,
        sigma_y=1.17,
        sigma_px=4.4,
        sigma_py=3.5,
        show_shape=False,
        N=100000,
        s1_to_s2=335,
        N_slices=30,
        show_setup=True
    )
    ceu.get_X_Y("S2_beam")
    ceu.plot_transverse_beam()

    # simulate_s1_s2_clear_run()
    # GUI limit is 100-300
    # translation between gui and s1_to_s2 is +81
    # s1_to_s2=335, gui=254z


# simulate_s1_s2_clear_run()
adjustment = 0
# al setup
# distance from s1 face to patient of 494mm, at robot=300 (tbc)
# s1 to s2 face = 182
# robot_to_s1_to_patient=+194
# s1 face to 0 point of robot=194mm


def simulate_s1_s2_clear_run_al_1(
    s1_thickness=30,
    s1_to_patient=492,
    sigma=18.52898,
    max_height=30.0,
    shape_radius=25,
):
    ceu = clear_experiment_utils()
    ceu.run_through_s1_and_s2_clear(
        s1_thickness,
        s1_to_patient,
        sigma,
        max_height,
        shape_radius,
        sigma_x=0.86,
        sigma_y=1.14,
        sigma_px=4.17,
        sigma_py=3.26,
        show_shape=True,
        show_setup=True,
        N=1000000,
        s1_to_s2=adjustment + 381,
        N_slices=30,
        material='"Aluminum"',
        slice_half_thickness_limit=0.5,
        perspex_pos=11,
    )


def simulate_s1_s2_clear_run_al_2(
    s1_thickness=30,
    s1_to_patient=492,
    sigma=18.52898,
    max_height=35.0,
    shape_radius=20,
):
    ceu = clear_experiment_utils()
    ceu.run_through_s1_and_s2_clear(
        s1_thickness,
        s1_to_patient,
        sigma,
        max_height,
        shape_radius,
        sigma_x=0.86,
        sigma_y=1.14,
        sigma_px=4.17,
        sigma_py=3.26,
        show_shape=True,
        N=100000,
        s1_to_s2=adjustment + 335,
        N_slices=30,
        material='"Aluminum"',
        slice_half_thickness_limit=0.5,
        perspex_pos=10,
    )


def simulate_s1_s2_clear_run_al_3(
    s1_thickness=30,
    s1_to_patient=200,
    sigma=18.52898,
    max_height=35.0,
    shape_radius=15.3,
    output_filename_ext="",
    jitter_matrix=[[[0, 0], [0, 0, 0]], [
        [0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]]],
):
    ceu = clear_experiment_utils()
    ceu.run_through_s1_and_s2_clear(
        s1_thickness,
        s1_to_patient,
        sigma,
        max_height,
        shape_radius,
        sigma_x=0.86,
        sigma_y=1.14,
        sigma_px=4.17,
        sigma_py=3.26,
        show_shape=True,
        N=1000000,
        s1_to_s2=181,
        N_slices=30,
        material='"Aluminum"',
        slice_half_thickness_limit=0.5,
        perspex_pos=10,
        output_filename_ext=output_filename_ext,
        jitter_matrix=jitter_matrix,
    )


def simulate_s1_s2_clear_run_al_4(
    s1_thickness=15,
    s1_to_patient=300,
    sigma=18.52898,
    max_height=35.0,
    shape_radius=15.3,
    output_filename_ext="",
    jitter_matrix=[[[0, 0], [0, 0, 0]], [
        [0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]]],
):
    ceu = clear_experiment_utils()
    ceu.run_through_s1_and_s2_clear(
        s1_thickness,
        s1_to_patient,
        sigma,
        max_height,
        shape_radius,
        sigma_x=0.86,
        sigma_y=1.14,
        sigma_px=4.17,
        sigma_py=3.26,
        show_shape=True,
        N=1000000,
        s1_to_s2=160,
        N_slices=30,
        material='"Aluminum"',
        slice_half_thickness_limit=0.5,
        perspex_pos=10,
        output_filename_ext=output_filename_ext,
        jitter_matrix=jitter_matrix,
    )


def do_longitudinal_scan(scan_range, step):

    runs = np.arange(scan_range[0], scan_range[1] + step, step=step)
    ceu = clear_experiment_utils()
    for i in runs:
        simulate_s1_s2_clear_run_al_3(
            s1_to_patient=i, output_filename_ext="_" + str(i))


def do_jitter_scan(scan_range, step):
    print("yeet")


simulate_s1_s2_clear_run()


#jitter_matrix = [[[0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]]]
# do_longitudinal_scan([200, 500], 10)
# simulate_s1_s2_clear_run_al_3()
#ceu = clear_experiment_utils()
# simulate_s1_s2_clear_run_al_4(jitter_matrix=jitter_matrix)
# ceu.get_X_Y("S2_beam")
# ceu.plot_transverse_beam()
# do_longitudinal_scan([200, 220], 5)
# scan_range = np.arange(200, 220, 5)
# for i in scan_range:
#    ceu.get_X_Y("S2_beam_" + str(i))
#    ceu.plot_transverse_beam(save=True)
