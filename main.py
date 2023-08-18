from S2_optimisation_runner import S2_runner
from thickness_optimiser_utils import thickness_optimiser_utils
from gaussian_optimiser_utils import gaussian_optimiser_utils
from automation_utils import automation_utils
from S1_sweepers import (
    sweep_parameters_and_energy,
    smart_sweep_and_energy,
    sweep_parameters_single_material,
    sweep_parameters,
)


def run_rf_beam_through_topas():
    tou = thickness_optimiser_utils()
    tou.run_through_uniform_foil_from_imported_beam_kapton(
        0.1, 100, '"Kapton"', '"/home/robertsoncl/topas/ttb_run_data/rf_track_result"'
    )


run_rf_beam_through_topas()


def main():
    # runner = S2_runner(N=10000)
    # runner.run_gaussian_optimisation(runs=1)

    benchmarker = thickness_optimiser_utils()
    benchmarker.run_through_uniform_foil_from_generated_beam(
        thickness=0.116549,
        distance=2500,
        material='"Tantalum"',
        N=1000,
        score_at_S1=True,
    )
    # benchmarker.get_X_Y("scattered_beam.phsp")
    # benchmarker.plot_transverse_beam()
    # runner.test_setup(6.698850493926685, 11.033691527726369, 910.7498981259621)
    # sweep_parameters_and_energy(1000, 3000, 1000, 100, 150, 10)
    # smart_sweep_and_energy(1000, 3000, 400, 100, 150, 10)
    # sweep_parameters(1500, 3000, 500)

    # for testing optimisation results
    # beam = thickness_optimiser_utils()
    # beam.run_through_uniform_foil(
    #    thickness=0.116549,
    #    distance=2500,
    #    N=100000,
    #    material='"Tantalum"',
    #    score_at_S1=True,
    # )
    beam = gaussian_optimiser_utils()
    beam.run_through_gaussian_foil(10.207696, 20.78885, 741.2301, save_shape=True)
    beam.get_X_Y("S2_beam.phsp")
    beam.plot_transverse_beam()

    # get_tantalum_s1_phasespace()
    # beam.show_database(
    # "material_classifications/smart_electron_results_E_1", '"Tantalum"', 3000, 110
    # )
    # beam.delete_database_rows(
    # [58], "material_classifications/smart_electron_results_E_1"
    # )
    # optimise_thickness(1, distance=2500, material='"Aluminum"', min_guess=2, max_guess=4)
    # smart_sweep(1500, 3000, 500)
    # sweep_parameters_single_material(1500, 3000, 500)
    # beam = thickness_optimiser_utils()
    # beam.run_through_uniform_foil(
    #    100, 2000, N=1000, material='"Tantalum"', score_at_S1=False, energy=200
    # )
    # beam.get_X_Y("scattered_beam.phsp")
    # beam.save_to_database("collimation_data_1")
    # beam.show_database("collimation_data_1")
    # beam.run_through_uniform_foil(0.116549, 2500, '"Tantalum"', score_at_S1=False)
    # beam.get_X_Y("scattered_beam.phsp")
    # beam.plot_transverse_beam()


# beam.delete_database_rows([5])
# beam.run_through_uniform_foil(2.6230820326844038, 2500, '"Aluminum"')
# beam.get_X_Y("scattered_beam.phsp")
# beam.plot_transverse_beam()
# beam.save_to_database("material_classifications/electron_results")


# main()
