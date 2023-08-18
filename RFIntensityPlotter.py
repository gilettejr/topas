from partrecIntensityPlotter import partrecIntensityPlotter
import pandas as pd
import numpy as np


class RFIntensityPlotter(partrecIntensityPlotter):
    def __init__(self, phsp):
        if isinstance(phsp, str):
            phsp = pd.read_parquet(phsp)

        self.phsp = phsp

        def getSlices(phsp, slice_width=1):
            phsp_xslice = phsp[(phsp["Y"] < slice_width)]
            phsp_xslice = phsp_xslice[(phsp_xslice["Y"] > -slice_width)]
            phsp_yslice = phsp[(phsp["X"] < slice_width)]
            phsp_yslice = phsp_yslice[(phsp_yslice["X"] > -slice_width)]
            return phsp_xslice, phsp_yslice
        self.getSlices = getSlices
