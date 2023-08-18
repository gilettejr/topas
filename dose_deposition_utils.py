from automation_utils import automation_utils


class dose_deposition_utils(automation_utils):
    def run_through_dose_scorer(self):
        file = open(self.home_directory + "topas/scattering_foil/gaussian3d.txt", "w")
        # set number of threads depending on computing power available
        file.write("i:Ts/NumberOfThreads=" + self.no_of_threads + "\n")
        # define arbitrarily large world
        file.write("d:Ge/World/HLX = 50.0 m\n")
        file.write("d:Ge/World/HLY = 50.0 m\n")
        file.write("d:Ge/World/HLZ = 5.0 m\n")
        # set world as vacuum for simplicity
        file.write('s:Ge/World/Material = "Vacuum"\n')
        file.write('s:So/S2_source/Type = "PhaseSpace"\n')
        file.write('s:So/S2_source/Component = "World"\n')
        # import from previously run S1beam file to get correct phase space
        file.write('s:So/S2_source/PhaseSpaceFileName = "S2_beam"\n')
        file.write('b:So/S2_source/PhaseSpacePreCheck = "False"\n')
        file.write("u:So/S2_source/PhaseSpaceScaleZPosBy = 0.\n")
        file.write('s:Ge/Phantom/Type = "TsBox"')
        file.write('s:Ge/Phantom/Parent = "World"')
        file.write('s:Ge/Phantom/Material = "G4_WATER"')
        file.write("d:Ge/Phantom/HLX=0.2 m")
        file.write("d:Ge/Phantom/HLY=0.2 m")
        file.write("d:Ge/Phantom/HLZ=0.2 m")

        file.write('s:Ge/PhantomScorer/Quantity = "DoseToMedium"')
        file.write('s:Ge/PhantomScorer/Component = "Phantom"')
