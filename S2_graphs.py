import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot_gaussian_shape(filename):
    shape = pd.read_parquet(filename)
    sns.lineplot(data=shape, x="X", y="Y")
    plt.xlabel("R (mm)")
    plt.ylabel("z (mm)")


plot_gaussian_shape("10.21_20.79_740.23")
