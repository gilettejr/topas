from automation_utils import automation_utils
from thickness_optimiser_utils import thickness_optimiser_utils
from gaussian_optimiser_utils import gaussian_optimiser_utils
from mlc_optimiser_utils import mlc_optimiser_utils
import numpy as np


class topas_ttb_runners(automation_utils):
    def __init__(self):
        def convert_twosigma_to_thickness(twosigma, material):
            # only works for Tantalum right noww
            d = np.divide(np.divide(twosigma, 2.5) - 16.14, 203.576)
            return d

        self.convert_twosigma_to_thickness = convert_twosigma_to_thickness
        # code here to write rf optimisation phase space to phsp input file
        # for topas

    def run_through_s1(self, twosigma_at_target, material='"Tantalum"'):
        thickness = self.convert_twosigma_to_thickness(twosigma_at_target, material)
        tou = thickness_optimiser_utils()
        tou.run_through_uniform_foil_from_imported_beam(
            thickness=thickness,
            material=material,
            distance=0,
            input_filename='"ttb_run_data/rf_track_result"',
        )
        # print(thickness[80])
        # tou.get_X_Y("beam_downstream_of_s1")
        # self.X = tou.X
        # self.Y = tou.Y

    def run_through_s2(self, sigma, max_height, s1_to_s2_drift_space):
        gou = gaussian_optimiser_utils()
        gou.run_through_gaussian_foil(
            sigma,
            max_height,
            s1_to_s2_drift_space,
            filename="ttb_run_data/S2_topas_script.txt",
            input_filename='"beam_downstream_of_s1"',
        )
        # gou.get_X_Y("S2_beam")
        # self.X = gou.X
        # self.Y = gou.Y

    def run_through_s2_vary_width(
        self, sigma, max_height, s1_to_s2_drift_space, width, show_shape
    ):
        gou = gaussian_optimiser_utils()
        gou.run_through_gaussian_foil(
            sigma,
            max_height,
            s1_to_s2_drift_space,
            shape_radius=width,
            filename="ttb_run_data/S2_topas_script.txt",
            input_filename='"beam_downstream_of_s1"',
            show_shape=show_shape,
        )

    def run_through_s2_mlc(
        self,
        slice_radii,
        max_height,
        s1_to_s2_drift_space,
        N_slices,
        max_radius,
        show_shape,
    ):
        mlou = mlc_optimiser_utils()
        mlou.run_through_mlc_foil(
            slice_radii,
            max_height,
            s1_to_s2_drift_space,
            N_slices,
            max_radius,
            show_shape=show_shape,
            filename="ttb_run_data/S2_topas_script.txt",
            input_filename='"beam_downstream_of_s1"',
        )
