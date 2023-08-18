import numpy as np
from thickness_optimiser_utils import thickness_optimiser_utils
import pandas as pd
from foil_optimisers import optimise_S1_thickness

# simple function to sweep through distance and material
# for thickness optimisation across the full parameter space
def sweep_parameters(min_dist, max_dist, step):
    # list of predefined topas materials to study
    materials = ['"Aluminum"', '"Tantalum"', '"G4_NYLON-6-6"']
    # create array of distances to patient to be swept
    distances = np.arange(min_dist, max_dist + step, step=step)
    # loop through materials and distances to find appropriate thicknesses
    # for 1000mm radius beam at patient
    for i in distances:
        for j in materials:
            # carry out optimisation and retrieve minimal merit value
            # and corresponding input variables
            M, X = optimise_S1_thickness(1, i, j, 0, 10)
            # initialise topas utility instance
            beam = thickness_optimiser_utils()
            # rerun optimal solution through topas
            beam.run_through_uniform_foil(X, i, j)
            # retrieve phase space distribution and set as class attributes
            beam.get_X_Y("scattered_beam.phsp")
            # save input parameters and final beam data to binary file
            beam.save_to_database("material_classifications/realistic_beam_results_1")


def sweep_parameters_single_material(min_dist, max_dist, step, material='"Tantalum"'):
    # create array of distances to patient to be swept
    distances = np.arange(min_dist, max_dist + step, step=step)
    # loop through materials and distances to find appropriate thicknesses
    # for 1000mm radius beam at patient
    for i in distances:
        # carry out optimisation and retrieve minimal merit value
        # and corresponding input variables
        M, X = optimise_S1_thickness(1, i, material, 0, 1)
        # initialise topas utility instance
        beam = thickness_optimiser_utils()
        # rerun optimal solution through topas
        beam.run_through_uniform_foil(X, i, material)
        # retrieve phase space distribution and set as class attributes
        beam.get_X_Y("scattered_beam.phsp")
        # save input parameters and final beam data to binary file
        beam.save_to_database("material_classifications/tantalum_realistic")


def sweep_parameters_and_energy(min_dist, max_dist, dstep, min_E, max_E, estep):
    # list of predefined topas materials to study
    materials = [
        '"Aluminum"',
        '"Tantalum"',
    ]
    # create array of distances to patient to be swept
    distances = np.arange(min_dist, max_dist + dstep, step=dstep)
    energies = np.arange(min_E, max_E + estep, step=estep)
    # loop through energies, materials and distances to find appropriate thicknesses
    # for 1000mm radius beam at patient
    for e in energies:
        for i in distances:
            for j in materials:
                # carry out optimisation and retrieve minimal merit value
                # and corresponding input variables
                M, X = optimise_S1_thickness(1, i, j, 0, 10, energy=e)
                # initialise topas utility instance
                beam = thickness_optimiser_utils()
                # rerun optimal solution through topas
                beam.run_through_uniform_foil(X, i, j, energy=e)
                # retrieve phase space distribution and set as class attributes
                beam.get_X_Y("scattered_beam.phsp")
                # save input parameters and final beam data to binary file
                beam.save_to_database("material_classifications/electron_results_E")


# optimised sweeping function
# much faster and more accurate than sweep_parameters
# takes existing data table as input
# sets initial guesses to within existing data points
# good for filling in data between points in existing, sparse database
def smart_sweep(
    min_dist,
    max_dist,
    step,
    initial_file="material_classifications/smart_electron_results",
):
    # list of predefined topas materials to study
    materials = ['"Aluminum"', '"Tantalum"', '"G4_NYLON-6-6"']
    # create array of distances to patient to be swept
    distances = np.arange(min_dist, max_dist + step, step=step)
    # load existing database
    initial_data = pd.read_parquet(initial_file)
    # loop through all chosen materials and defined distances to patient
    for i in distances:
        for j in materials:
            # create initial values for upper and lower bounds
            # for randomised initial guess bounds
            upper_bound = 5000
            lower_bound = 0
            # loop through rows in existing database
            for k in initial_data.index:
                # find higher nearest neighbour for corresponding distance
                # for the appropriate material
                # if nearer by distance than previously defined upper bound,
                # then redefine upper bound
                if (
                    initial_data["Material"].at[k] == j
                    and initial_data["Distance"].at[k] > i
                    and initial_data["Distance"].at[k] < upper_bound
                ):  # upper bound redefined
                    upper_bound = initial_data["Distance"].at[k]
                    # nearest higher neighbour by distance
                    # corresponds to nearest lower neighbour by thickness
                    # define/redefine nearest lower neighbour by thickness
                    min_guess = initial_data["Thickness"].at[k]
                # find lower nearest neighbour for corresponding distance
                # for the approprite material
                # if nearer by distance than previously defined lower bound,
                # then redefine lower bound
                elif (
                    initial_data["Material"].at[k] == j
                    and initial_data["Distance"].at[k] < i
                    and initial_data["Distance"].at[k] > lower_bound
                ):  # lower bound redefined
                    lower_bound = initial_data["Distance"].at[k]
                    # nearest higher neighbour by distance
                    # corresponds to nearest lower neighbour by thickness
                    # define/redefine nearest lower neighbour by thickness
                    max_guess = initial_data["Thickness"].at[k]
                    # if datapoint for same material and distance exists
                    # set guesses closely around existing value for speed
                elif (
                    initial_data["Material"].at[k] == j
                    and initial_data["Distance"].at[k] == i
                ):
                    min_guess = initial_data["Thickness"].at[k] - 0.01
                    max_guess = initial_data["Thickness"].at[k] + 0.01
            M, X = optimise_S1_thickness(1, i, j, min_guess, max_guess)
            beam = thickness_optimiser_utils()
            beam.run_through_uniform_foil(X, i, j)
            beam.get_X_Y("scattered_beam.phsp")
            beam.save_to_database("material_classifications/smart_electron_results_1")


# optimised sweeping function
# much faster and more accurate than sweep_parameters
# takes existing data table as input
# sets initial guesses to within existing data points
# good for filling in data between points in existing, sparse database
def smart_sweep_and_energy(
    min_dist,
    max_dist,
    dstep,
    min_E,
    max_E,
    estep,
    initial_file="material_classifications/smart_electron_results_E_1",
):
    # list of predefined topas materials to study
    materials = [
        '"Aluminum"',
        '"Tantalum"',
    ]
    # create array of distances to patient to be swept
    distances = np.arange(min_dist, max_dist + dstep, step=dstep)
    energies = np.arange(min_E, max_E + estep, step=estep)
    # load existing database
    initial_data = pd.read_parquet(initial_file)
    # loop through all chosen materials and defined distances and energies to patient
    for e in energies:
        for i in distances:
            for j in materials:
                # create initial values for upper and lower bounds
                # for randomised initial guess bounds
                upper_bound = 5000
                lower_bound = 0
                # loop through rows in existing database
                for k in initial_data.index:
                    # find higher nearest neighbour for corresponding distance
                    # for the appropriate material
                    # if nearer by distance than previously defined upper bound,
                    # then redefine upper bound
                    if (
                        initial_data["Material"].at[k] == j
                        and initial_data["Initial_Beam_E"].at[k] == e
                        and initial_data["Distance"].at[k] > i
                        and initial_data["Distance"].at[k] < upper_bound
                    ):  # upper bound redefined
                        upper_bound = initial_data["Distance"].at[k]
                        # nearest higher neighbour by distance
                        # corresponds to nearest lower neighbour by thickness
                        # define/redefine nearest lower neighbour by thickness
                        min_guess = initial_data["Thickness"].at[k]
                    # find lower nearest neighbour for corresponding distance
                    # for the approprite material
                    # if nearer by distance than previously defined lower bound,
                    # then redefine lower bound
                    elif (
                        initial_data["Material"].at[k] == j
                        and initial_data["Initial_Beam_E"].at[k] == e
                        and initial_data["Distance"].at[k] < i
                        and initial_data["Distance"].at[k] > lower_bound
                    ):  # lower bound redefined
                        lower_bound = initial_data["Distance"].at[k]
                        # nearest higher neighbour by distance
                        # corresponds to nearest lower neighbour by thickness
                        # define/redefine nearest lower neighbour by thickness
                        max_guess = initial_data["Thickness"].at[k]
                        # if datapoint for same material and distance exists
                        # set guesses closely around existing value for speed
                    elif (
                        initial_data["Material"].at[k] == j
                        and initial_data["Distance"].at[k] == i
                        and initial_data["Initial_Beam_E"].at[k] == e
                    ):
                        min_guess = initial_data["Thickness"].at[k] - 0.01
                        max_guess = initial_data["Thickness"].at[k] + 0.01
                M, X = optimise_S1_thickness(1, i, j, min_guess, max_guess, energy=e)
                beam = thickness_optimiser_utils()
                beam.run_through_uniform_foil(X, i, j, energy=e)
                beam.get_X_Y("scattered_beam.phsp")
                beam.save_to_database(
                    "material_classifications/smart_electron_results_E_1"
                )
