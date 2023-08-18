def plot_angular_spreads(distances,sigmas,thicknesses):
    two_sigma=two_sigma
    one_sigma=two_sigma/2
    angle = np.arctan(one_sigma / distance)
