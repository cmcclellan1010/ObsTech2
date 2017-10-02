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
    shape = np.shape(da)
    n_pixels = shape[1] * shape[2]
    return da, n_pixels


# READ NOISE 1, 2: Calculate RMS array

data_100ms = construct_data_array('dark_100ms_', 18)
data_1000ms = construct_data_array('dark_1000ms_', 6)
data_1e4ms = construct_data_array('dark_1e4ms_', 6)
data_1e5ms = construct_data_array('dark_1e5ms_', 3)

data_list = [data_100ms, data_1000ms, data_1e4ms, data_1e5ms]
final_RMS_array = []
for i in range(4):
    average_of_square = np.mean(data_list[i][0]**2, axis=0)
    square_of_average = (np.mean(data_list[i][0], axis=0))**2
    variance = average_of_square - square_of_average
    RMS = np.absolute(variance)**0.5

    # READ NOISE 3: Find mean, median, and RMS of RMS array
    npix = data_list[i][1]
    print npix
    print "i = ", i
    print "Mean: ", np.mean(RMS)
    print "Median: ", np.median(RMS)
    print "RMS: ", rms(RMS)
    print "Read noise uncertainty: ", rms(RMS)/np.sqrt(npix), " per pixel"

    # READ NOISE 4: Make a histogram of RMS array values
    final_RMS_array.append(np.ndarray.flatten(RMS))


print "\nGauss Fit measurements:"
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))

# PLOT #1
n, bins, patches = ax1.hist(final_RMS_array[0], 100, range=[0, 30])
bincenters = 0.5*(bins[1:]+bins[:-1])

g_init = models.Gaussian1D(amplitude=18000, mean=12, stddev=2.5)
fit_g = fitting.LevMarLSQFitter()
g = fit_g(g_init, bincenters, n)

mean1, stddev1 = g.mean[0], g.stddev[0]
print 'i = 1'
print "Mean: ", mean1
print "Stddev: ", stddev1

ax1.plot(bincenters, g(bincenters), 'r--', linewidth=3)
ax1.set_xlabel('Pixel-wise RMS of DNs')
ax1.set_ylabel('N')
ax1.set_xlim(0, 30)
ax1.set_ylim(0, 20000)
ax1.grid(True)
ax1.set_title('100ms Dark')


# PLOT #2
n, bins, patches = ax2.hist(final_RMS_array[1], 100, range=[0, 30])
bincenters = 0.5*(bins[1:]+bins[:-1])

g_init = models.Gaussian1D(amplitude=12500, mean=10.6, stddev=4)
fit_g = fitting.LevMarLSQFitter()
g = fit_g(g_init, bincenters, n)

mean2, stddev2 = g.mean[0], g.stddev[0]
print 'i = 2'
print "Mean: ", mean2
print "Stddev: ", stddev2

ax2.plot(bincenters, g(bincenters), 'r--', linewidth=3)
ax2.set_xlabel('Pixel-wise RMS of DNs')
ax2.set_ylabel('N')
ax2.set_xlim(0, 30)
ax2.set_ylim(0, 20000)
ax2.grid(True)
ax2.set_title('1s Dark')


# PLOT 3
n, bins, patches = ax3.hist(final_RMS_array[2], 100, range=[0, 30])
bincenters = 0.5*(bins[1:]+bins[:-1])

g_init = models.Gaussian1D(amplitude=12500, mean=10.6, stddev=4)
fit_g = fitting.LevMarLSQFitter()
g = fit_g(g_init, bincenters, n)

mean3, stddev3 = g.mean[0], g.stddev[0]
print 'i = 3'
print "Mean: ", mean3
print "Stddev: ", stddev3

ax3.plot(bincenters, g(bincenters), 'r--', linewidth=3)
ax3.set_xlabel('Pixel-wise RMS of DNs')
ax3.set_ylabel('N')
ax3.set_xlim(0, 30)
ax3.set_ylim(0, 20000)
ax3.grid(True)
ax3.set_title('10s Dark')


# PLOT 4
n, bins, patches = ax4.hist(final_RMS_array[3], 100, range=[0, 30])
bincenters = 0.5*(bins[1:]+bins[:-1])

g_init = models.Gaussian1D(amplitude=10000, mean=8.9, stddev=5.6)
fit_g = fitting.LevMarLSQFitter()
g = fit_g(g_init, bincenters, n)

mean4, stddev4 = g.mean[0], g.stddev[0]
print 'i = 4'
print "Mean: ", mean4
print "Stddev: ", stddev4

ax4.plot(bincenters, g(bincenters), 'r--', linewidth=3)
ax4.set_xlabel('Pixel-wise RMS of DNs')
ax4.set_ylabel('N')
ax4.set_xlim(0, 30)
ax4.set_ylim(0, 20000)
ax4.grid(True)
ax4.set_title('100s Dark')

plt.tight_layout()
plt.show()

exptime = [0.1, 1, 10, 100]
means = [mean1, mean2, mean3, mean4]
stddevs = [stddev1, stddev2, stddev3, stddev4]

err = []
for item in stddevs:
    err.append(stddevs[stddevs.index(item)]/390150.**0.5)
print err

l_init = models.Linear1D(slope=0, intercept=956)
fit_l = fitting.LinearLSQFitter()
l = fit_l(l_init, exptime, means)
slope, intercept = l.slope[0], l.intercept[0]
print "Slope, Intercept: ", slope, intercept

fig = plt.figure()
ax = fig.add_subplot(111)
ax.annotate('Slope: '+str("%.2E" % slope+' DN/s'), xy=(20, 11))
ax.annotate('Y-Intercept: '+str("%.2f" % intercept)+' DN', xy=(20, 10.5))
plt.errorbar(exptime, means, yerr=err, fmt='ko', ecolor='k', label='Mean Read Noise')
plt.plot(exptime, l(exptime), 'limegreen', label='Linear fit')
plt.xlabel('Exposure time (s)')
plt.ylabel('Mean Read Noise (DN)')
plt.xlim(-10, 110)
plt.tight_layout()
plt.legend(loc=3)
plt.grid(True)
plt.show()