from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting


def rms(x):
    return (np.absolute(np.mean(x**2) - (np.mean(x))**2))**0.5


def construct_data_array(filename_prefix, n_images):
    da = []
    for i in range(n_images):
        if i+1 < 10:
            j = '00'+str(i+1)
        else:
            j = '0'+str(i+1)
        da.append(fits.open(filename_prefix+j+'.FIT')[0].data)
    da = np.array(da, dtype=float)
    return da


def plot_hist_gauss(data, bins, amplitude, mean, stddev, title):
    print title
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 12))
    n, bin_locations, patches = ax1.hist(data, bins, range=[-75, 75])
    bincenters = 0.5*(bin_locations[1:]+bin_locations[:-1])
    g_init = models.Gaussian1D(amplitude=amplitude, mean=mean, stddev=stddev)
    fit_g = fitting.LevMarLSQFitter()
    g = fit_g(g_init, bincenters, n)
    mean1, stddev1 = g.mean[0], g.stddev[0]
    print "Mean: ", mean1
    print "Stddev: ", stddev1
    ax1.plot(bincenters, g(bincenters), 'r--', linewidth=3)
    ax1.set_xlabel('Pixel-wise Dark Current')
    ax1.set_ylabel('N')
    ax1.grid(True)
    ax1.set_title(title)
    #plt.show()
    return mean1, stddev1


# BIAS LEVEL MEASUREMENT
bias = construct_data_array('bias_200ms_', 5)
for i in range(5):
    print "Bias: ", np.median(bias[i]), rms(bias[i])
master_bias = np.median(bias, axis=0)

prefix_list = ['dc_1000ms_', 'dc_5000ms_', 'dc_25000ms_', 'dc_125000ms_', 'dc_6e5_']
final_mean = []
final_stddev = []

for filename in prefix_list:
    i = prefix_list.index(filename)
    data = np.ndarray.flatten(construct_data_array(filename, 1)[0] - master_bias)
    result = plot_hist_gauss(data, 75, 45000, i, 13.6, filename+'001 (Bias-subtracted)')
    final_mean.append(result[0])
    final_stddev.append(result[1]/390150.**0.5)

exptimes = [1, 5, 25, 125, 600]
print final_mean
print final_stddev

p, V = np.polyfit(exptimes, final_mean, 1, cov=True)
slope = p[0]
slope_err = np.sqrt(V[0][0])

print "Slope: ", slope
print "Error in slope: ", slope_err

yfit = []
for item in exptimes:
    y1 = p[0]*item + p[1]
    yfit.append(y1)

fig = plt.figure()
ax = plt.subplot(111)
plt.errorbar(exptimes, final_mean, yerr=final_stddev, fmt='ko', ecolor='k', elinewidth=4)
plt.plot(exptimes, yfit, 'limegreen', linewidth=1)
ax.annotate('Slope: '+str("%.2E" % slope)+' DN/s', xy=(33, 13))
ax.annotate("Error in slope: "+str("%.2E" % slope_err)+' DN/s', xy=(33, 12))
plt.xlabel('Exposure time (s)')
plt.ylabel('DNs')
plt.show()


