from new_foil_plotting_utils import new_foil_plotting_utils
from new_gaussian_optimiser_utils import dual_optimiser_utils


#
dou = dual_optimiser_utils()
#dou.generate_phsp_beam(1, 1, 0.0001, 0.0001, 200, 0.0, 1000000)
dou.generate_twiss_beam(20, 20, 0.025, 0.025, 0, 0, 200, 1000000)

# solution 1a: 890 and between quads
# 48% transmission, 15mm radius close, wider further, nice balance and reasonable geometry now
# dou.add_foils(
#    3,
#    8,
#    500,
#    1900,
#    "Nylon",
#    "Nylon",
#    N_slices=10,
#    s2_sigma=2.2,
#    s2_radius=6,
#    sigma_convolution_factor=0.9,
#    view_setup=True,
# )
# 50% transmission, again much more reasonable geometry
# solution 2a
dou.add_foils(
    1.8,
    4.5,
    500,
    2400,
    "PEEK",
    "PEEK",
    N_slices=10,
    s2_sigma=2,
    s2_radius=8,
    sigma_convolution_factor=0.9,
    view_setup=False,
)

# solution NEW
# dou.add_foils(
#    1.5,
#    3,
#    500,
#    2400,
#    "Peek",
#    "Peek",
#    N_slices=10,
#    s2_sigma=2,
#    s2_radius=6,
#    sigma_convolution_factor=0.9,
#    view_setup=False,
# )

# solution 1b: 890 and between quads
# 50% transmission, 15mm radius close, wider further, nice balance and reasonable geometry now
# much thicker - better in terms of geometry
# dou.add_foils(
#    3,
#    8,
#    500,
#    1900,
#    "Nylon",
#    "Nylon",
#    N_slices=10,
#    s2_sigma=2.2,
#    s2_radius=10,
#    sigma_convolution_factor=0.9,
#    view_setup=False,
# )
# solution 3
# 40% transmission
# dou.add_foils(
#    7,
#    6,
#    1100,
#    1400,
#    "Nylon",
#    "Aluminum",
#    N_slices=10,
#    s2_sigma=6,
#    s2_radius=18,
#    sigma_convolution_factor=0.9,
#    view_setup=False,
# )
# RF Track Benchmark
# 46% transmission
# dou.add_foils(
#    1.8,
#    6,
#    500,
#    2400,
#    "G4_WATER",
#    "Vacuum",
#    N_slices=10,
#    s2_sigma=1.8,
#    s2_radius=6,
#    sigma_convolution_factor=0.9,
#    view_setup=False,
# )

# comparison for andrea

# dou.add_foils(
#    1,
#    10,
#    300,
#    1000.0,
#    "Iron",
#    "Vacuum",
#    N_slices=10,
#    s2_sigma=1.8,
#    s2_radius=6,
#    sigma_convolution_factor=0.9,
#    view_setup=False,
# )


# dou.add_tank(100, view_setup=False)
# dou.add_dipole(0.0
# )
#dou.add_stem(1, 'Steel')
dou.topas_run()
nfu = new_foil_plotting_utils("S2_beam.phsp")
nfu.show_transverse_beam("e", fov=50, col=50)
