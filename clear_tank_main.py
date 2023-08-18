from clear_experiment_utils import clear_experiment_utils
from clear_phsp_optimiser import optimise_s2_for_clear
import numpy as np


adjustment = 0
# al setup
# distance from s1 face to patient of 494mm, at robot=300 (tbc)
# s1 to s2 face = 182
# robot_to_s1_to_patient=+194
# s1 face to 0 point of robot=194mm
def simulate_s1_s2_clear_run_al_1(
    s1_thickness=1,
    s1_to_patient=420,
    sigma=18.52898,
    max_height=30.0,
    shape_radius=25,
):
    ceu = clear_experiment_utils()
    ceu.run_through_yag_and_s2_tank_clear(
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
        s1_to_s2=200,
        N_slices=30,
        material='"Aluminum"',
        slice_half_thickness_limit=0.5,
        perspex_pos=11,
    )


def simulate_s1_s2_clear_run_al_2(
    s1_thickness=1,
    s1_to_patient=420,
    sigma=18.52898,
    max_height=35.0,
    shape_radius=20,
):
    ceu = clear_experiment_utils()
    ceu.run_through_yag_and_s2_tank_clear(
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
        s1_to_s2=200,
        N_slices=30,
        material='"Aluminum"',
        slice_half_thickness_limit=0.5,
        perspex_pos=10,
    )


def simulate_s1_s2_clear_run_al_3(
    s1_thickness=1,
    s1_to_patient=420,
    sigma=18.52898,
    max_height=35.0,
    shape_radius=15.3,
    output_filename_ext="",
    jitter_matrix=[[[0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]], [[0, 0], [0, 0, 0]]],
):
    ceu = clear_experiment_utils()
    ceu.run_through_yag_and_s2_tank_clear(
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
        s1_to_s2=200,
        N_slices=30,
        material='"Aluminum"',
        slice_half_thickness_limit=0.5,
        perspex_pos=10,
        output_filename_ext=output_filename_ext,
        jitter_matrix=jitter_matrix,
    )


ceu = clear_experiment_utils()
simulate_s1_s2_clear_run_al_1()
ceu.get_X_Y("S2_beam")
ceu.plot_transverse_beam()
