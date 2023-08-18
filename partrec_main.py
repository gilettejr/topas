from partrec_gaussian_optimiser_utils import partrec_gaussian_optimiser_utils
from partrecIntensityPlotter import partrecIntensityPlotter
from partrecDosePlotter import partrecDosePlotter
from guiScript import guiScript
from beamScript import beamScript
from scatScript import scatScript
from magnetScript import magnetScript
from additionScript import additionScript
from scorerScript import scorerScript
from mediaScript import mediaScript
import cv2
import os
import matplotlib.pyplot as plt


def design_1():
    # initialise script generator
    setup = partrec_gaussian_optimiser_utils()
    # generate Gaussian unit 90MeV beam with 1 million particles (takes a while to run)
    setup.generate_twiss_beam(20, 20, 0.0258, 0.025, 0, 0, 200, 1000000)
    # add pre-scatterer to magnify beam
    setup.add_flat_scatterer(0.6, 'Peek')
    # define gaussian scatterer (here with 30mm depth, 20mm radius, situated 250mm downstream of first scatterer, composed of 200 slices)
    setup.add_gaussian_scatterer(
        2.6, 2, 0.9, 5, 'Peek', 500, show_shape=False, thickness_limit=False)
    # add patient phase space scorerer at z=500m
    setup.add_patient(2500)
    setup.display_scatterers()
    # run script
    # setup.run_topas(view_setup=False)
    # initialise plotting class
    #plotter = partrec_foil_plotting('patient_beam.phsp')
    # plot transverse distributions and energy spectrum at patient
    #plotter.show_transverse_beam(particle='e', fov=20, col=10)


def design_2():
    # initialise script generator
    setup = partrec_gaussian_optimiser_utils()
    # generate Gaussian unit 90MeV beam with 1 million particles (takes a while to run)
    setup.generate_twiss_beam(100, 100, 0.005, 0.005, 0, 0, 200, 1000000)
    # add pre-scatterer to magnify beam
    setup.add_flat_scatterer(0.35, 'Peek')
    # define gaussian scatterer (here with 30mm depth, 20mm radius, situated 250mm downstream of first scatterer, composed of 200 slices)
    setup.add_gaussian_scatterer(
        2.6, 2, 0.9, 5, 'Peek', 500, show_shape=False, thickness_limit=0.2)
    # add patient phase space scorerer at z=500m
    setup.add_patient(2500)
    setup.display_scatterers()
    # run script
    setup.run_topas(view_setup=False)
    # initialise plotting class
    #plotter = partrec_foil_plotting('patient_beam.phsp')
    # plot transverse distributions and energy spectrum at patient
    #plotter.show_transverse_beam(particle='e', fov=10, col=10)


# design_2()
def design_2_new():
    gs = guiScript()
    bs = beamScript()
    ss = scatScript()
    scors = scorerScript()
    bs.addTwissBeam(30, 30, 0.03, 0.03, 0, 0, 200, 1000000)
    # smaller beam at s1 = larger flat region
    #bs.addPhspBeam(1, 1, 0.001, 0.001, 200, 0, 1000000)
    #ss.addFlatScatterer(0.35, 'Peek')
    # 90 microns Al equivalent
    ss.addFlatScatterer(0.1, 'Sodium')
    ss.addGaussianScatterer(
        2.6, 2, 0.9, 5, 'Peek', 500, show_shape=False, thickness_limit=0.2)
    ss.displayScatterers()
    scors.addPhspScorer(2500)
    #scors.addFilmDoseScorer(2500, xBins=50, yBins=50)
    #scors.setScorerFilter(generation='all', particle='gamma')
    gs.runTopas(view_setup=False)
    print('Initial sigmaX = '+str(round(bs.sigma_x, 2)) + 'mm')
    print('Initial emittX = '+str(round(bs.norm_emitt_x, 2))+'mm.mrad')
    plotter = partrecDosePlotter('DoseAtFilm1.csv', 1000000, 10)
    plotter.setCharge(1)
    # plotter.plotDosemap()
    #
    #plotter = partrec_foil_plotting(scors.scorerName+'.phsp')
    plotter = partrecIntensityPlotter(scors.scorerName+'.phsp')
    # plot transverse distributions and energy spectrum at patient
    plotter.show_transverse_beam(fov=7, col=7)


def makeVideo(image_folder, video_name):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images = sorted(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 10, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def clicAnimationS1():
    gs = guiScript()
    bs = beamScript()
    ss = scatScript()
    scors = scorerScript()
    bs.addTwissBeam(20, 20, 0.01, 0.01, 0, 0, 200, 1000000)

    # bs.addPhspBeam(1, 1, 0.001, 0.001, 200, 0, 1000000)
    #ss.addFlatScatterer(0.35, 'Vacuum')
    ss.addFlatScatterer(10, 'Aluminum')
    # ss.addGaussianScatterer(
    #    2.6, 2, 0.9, 5, 'Peek', 5, show_shape=False, thickness_limit=0.2)
    # ss.displayScatterers()
    scors.addPhspScorer(500)
    #scors.addFilmDoseScorer(2500, xBins=50, yBins=50)
    #scors.setScorerFilter(generation='all', particle='gamma')
    # gs.runTopas(view_setup=False)
    plotter = partrecIntensityPlotter(scors.scorerName+'.phsp')
    image_folder = '/home/robertsoncl/dphil/animations/s1'
    plotter.createAnimateProfile(
        100000, 100, '/home/robertsoncl/dphil/animations/s1/', fov=30, top=3200, etop=50000)

    video_name = 's1.avi'

    # cv2.destroyAllWindows()
    # video.release()

    # plotter.show_transverse_beam(fov=30)


def clicAnimationS2():
    gs = guiScript()
    bs = beamScript()
    ss = scatScript()
    scors = scorerScript()
    bs.addTwissBeam(20, 20, 0.01, 0.01, 0, 0, 200, 1000000)

    # bs.addPhspBeam(1, 1, 0.001, 0.001, 200, 0, 1000000)
    #ss.addFlatScatterer(0.35, 'Vacuum')
    ss.addFlatScatterer(30, 'Aluminum')
    ss.addGaussianScatterer(
        60, 65, 0.9, 20, 'Aluminum', 1000, show_shape=False, thickness_limit=0)
    # ss.displayScatterers()
    scorerNames = []
    for i in range(10, 1511, 10):
        scors.addPhspScorer(i)
        scorerNames.append(scors.scorerName)
    image_folder = '/home/robertsoncl/dphil/animations/s2/'
    #scors.addFilmDoseScorer(2500, xBins=50, yBins=50)
    #scors.setScorerFilter(generation='all', particle='gamma')
    # gs.runTopas(view_setup=False)
#    for i in range(len(scorerNames)):
#        plotter = partrecIntensityPlotter(scorerNames[i]+'.phsp')
#
#        plotter.snap_transverse_beam(fov=200, col=100)
#        # plt.show()
#        name = str(i)+'.png'
#        if len(name) == 5:
#            name = '00'+name
#        elif len(name) == 6:
#            name = '0'+name
#
   #     plt.savefig(
   #         image_folder+name)
   #     plt.close()
    video_name = 's2.avi'
    makeVideo(image_folder, video_name)

    # plotter.createAnimateProfile(
    #    100000, 100, '/home/robertsoncl/dphil/animations/s1/', fov=30, top=3200, etop=50000)


design_2_new()
