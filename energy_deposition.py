import pandas as pd
import numpy as np
import seaborn as sns
import os


def get_delta_E(xbins, ybins, zbins):
    file = open("scattering_foil/S1_energy", "w")
    file.write("i:Ts/NumberOfThreads=6\n")
    file.write("d:Ge/World/HLX = 5.0 m\n")
    file.write("d:Ge/World/HLY = 5.0 m\n")
    file.write("d:Ge/World/HLZ = 5.0 m\n")
    file.write('s:Ge/World/Material = "Vacuum"\n')
    file.write('s:Ge/S1/Type = "TsBox"\n')
    file.write('s:Ge/S1/Parent="World"\n')
    file.write('s:Ge/S1/Material="G4_NYLON-6-6"\n')
    file.write("d:Ge/S1/HLX =  2  mm\n")
    file.write("d:Ge/S1/HLY= 2 mm\n")
    file.write("d:Ge/S1/HLZ = 11 mm\n")
    file.write("d:Ge/S1/TransZ = 0.0582745 mm\n")
    file.write("i:Ge/S1/XBins=" + str(xbins) + "\n")
    file.write("i:Ge/S1/YBins=" + str(ybins) + "\n")
    file.write("i:Ge/S1/ZBins=" + str(zbins) + "\n")

    file.write('s:So/acc_source/Type = "Beam"\n')
    file.write("i:So/acc_source/NumberOfHistoriesInRun = 10000\n")
    file.write('s:So/acc_source/Component = "BeamPosition"\n')
    file.write('s:So/acc_source/BeamParticle="e-"\n')
    file.write("d:So/acc_source/BeamEnergy= 100 MeV\n")
    file.write('s:So/acc_source/BeamPositionDistribution= "Flat"\n')
    file.write("d:So/acc_source/BeamPositionCutoffX = 1 mm\n")
    file.write("d:So/acc_source/BeamPositionCutoffY = 1 mm\n")
    file.write("d:So/acc_source/BeamAngularDistributionX = 0 deg\n")
    file.write("d:So/acc_source/BeamAngularDistributionY = 0 deg\n")
    file.write('s:So/acc_source/BeamAngularDistribution="None"\n')
    file.write("u:So/acc_source/BeamEnergySpread = 0\n")
    file.write('s:So/acc_source/BeamPositionCutoffShape = "Ellipse"\n')
    file.write('s:Sc/MyScorer/Quantity                  = "EnergyDeposit"\n')
    file.write('s:Sc/MyScorer/Component                 = "S1"\n')
    file.write('s:Sc/MyScorer/OutputFile                = "Energy_Test"\n')
    file.write('s:Sc/MyScorer/OutputType                = "csv"\n')
    file.write('b:Sc/MyScorer/OutputToConsole           = "False"\n')
    file.write('s:Sc/MyScorer/IfOutputFileAlreadyExists = "Overwrite"\n')
    file.write('b:Ph/ListProcesses = "False"\n')
    file.write('b:Ge/CheckForOverlaps = "False"\n')
    file.write('b:Ge/QuitIfOverlapDetected = "False"\n')
    file.write('b:Ge/CheckForUnusedComponents = "False"\n')
    file.close()
    # point topas to Geant4 data firectory
    os.system(
        "export TOPAS_G4_DATA_DIR=/home/robertsoncl/G4Data\n./bin/topas scattering_foil/S1_energy"
    )


def get_pedd(xbins, ybins, zbins):
    deposition_frame = pd.read_csv(
        "Energy_Test.csv", skiprows=8, names=["x", "y", "z", "e"]
    )
    xbinlength = 0.2 / xbins
    ybinlength = 0.2 / ybins
    zbinlength = 1.1 / zbins
    voxel_volume = xbinlength * ybinlength * zbinlength
    deltaE = max(deposition_frame["e"])
    density = 16.6
    topas_charge = 1.6e-15
    flash_charge = 600e-9
    e_charge = 1.6e-19

    pedd = (
        np.divide(deltaE, voxel_volume * density)
        * np.divide(flash_charge, topas_charge)
        * 1e6
        * e_charge
    )
    return pedd


def make_pedd_voxel():
    bin_nos = np.arange(1, 40, step=1)
    voxel_nos = bin_nos * bin_nos * 2
    pedds = []
    for i in bin_nos:
        i = int(i)
        get_delta_E(i, i)
        pedd = get_pedd(i, i)
        pedds.append(pedd)
    pedds = np.array(pedds)
    pedd_frame = pd.DataFrame({"Voxel_nos": voxel_nos, "pedds": pedds})
    pedd_frame.to_parquet("pedd_voxel")


# make_pedd_voxel()
def main():
    # data = pd.read_parquet("pedd_voxel")
    # print(data)
    # ns.scatterplot(data=data, x="Voxel_nos", y="pedds")
    print(get_pedd(9, 9, 50))


main()
