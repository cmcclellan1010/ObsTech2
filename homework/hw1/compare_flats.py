# B. Connor McClellan
# 6 November 2017

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.modeling import models, fitting


def plot_hist_gauss(data, bins, amplitude, mean, stddev):
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 12))
    n, bin_locations, patches = ax1.hist(data, bins, range=[0.97, 1.03])
    bincenters = 0.5*(bin_locations[1:]+bin_locations[:-1])
    g_init = models.Gaussian1D(amplitude=amplitude, mean=mean, stddev=stddev)
    fit_g = fitting.LevMarLSQFitter()
    g = fit_g(g_init, bincenters, n)
    mean1, stddev1 = g.mean[0], g.stddev[0]
    print "Mean: ", mean1
    print "Stddev: ", stddev1
    ax1.plot(bincenters, g(bincenters), 'r--', linewidth=3)
    ax1.set_xlabel('Ratio of flat images by pixel')
    ax1.set_ylabel('N')
    ax1.grid(True)
    return mean1, stddev1


flat_1012 = fits.open('./1012/master_flat_r_1012.fit')[0].data
flat_1102 = fits.open('./1102/master_flat_r_1102.fit')[0].data

div = np.divide(flat_1012, flat_1102)
print div

plot_hist_gauss(np.ndarray.flatten(div), 100, 14000, 1, .08)

plt.figure(figsize=(15, 15))
plt.imshow(div, origin='lower')
plt.title('Division of two master flats')
plt.colorbar(fraction=0.026, pad=0.02)
plt.show()
