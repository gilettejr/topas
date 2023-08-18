from thickness_optimiser_utils import thickness_optimiser_utils
from gaussian_optimiser_utils import gaussian_optimiser_utils
from foil_optimisers import optimise_gaussian_foil


class S2_runner:
    def __init__(
        self, thickness=0.116549, distance=2500, material='"Tantalum"', N=10000
    ):
        def get_tantalum_s1_phasespace():
            beam = thickness_optimiser_utils()
            beam.run_through_uniform_foil(
                thickness=thickness,
                distance=distance,
                material=material,
                N=N,
                score_at_S1=True,
            )

        self.get_tantalum_s1_phasespace = get_tantalum_s1_phasespace

    def run_gaussian_optimisation(self, runs=1):
        self.get_tantalum_s1_phasespace()
        optimise_gaussian_foil(runs)

    def test_setup(self, sigma, height, position):
        self.get_tantalum_s1_phasespace()
        beam = gaussian_optimiser_utils()
        beam.run_through_gaussian_foil(sigma, height, position, save_shape=True)
        beam.get_X_Y("S2_beam.phsp")
        beam.plot_transverse_beam()
