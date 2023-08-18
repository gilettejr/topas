import pandas as pd


def convert_ascii_to_csv(path_to_file):
    data = pd.read_csv(path_to_file, delim_whitespace=True, header=None)
    print(data)
    data.to_csv(path_to_file + ".csv", header=False, index=False)


convert_ascii_to_csv("XPlusPhaseSpace1.phsp")
