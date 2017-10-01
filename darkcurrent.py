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

# BIAS LEVEL MEASUREMENT
bias = construct_data_array('bias_200ms_', 5)
for i in range(5):
    print "Bias: ", np.median(bias[i]), rms(bias[i])

# 1000 ms
dc1000ms = np.ndarray.flatten(construct_data_array('dc_1000ms_', 1)[0])
print dc1000ms

fig, ax1 = plt.subplots(1, 1, figsize=(12, 12))
n, bins, patches = ax1.hist(dc1000ms, 75)
bincenters = 0.5*(bins[1:]+bins[:-1])

g_init = models.Gaussian1D(amplitude=36200, mean=980, stddev=17.6)
fit_g = fitting.LevMarLSQFitter()
g = fit_g(g_init, bincenters, n)
mean1, stddev1 = g.mean[0], g.stddev[0]
print 'i = 1'
print "Mean: ", mean1
print "Stddev: ", stddev1
ax1.plot(bincenters, g(bincenters), 'r--', linewidth=3)
ax1.set_xlabel('Pixel-wise Dark Current')
ax1.set_ylabel('N')
ax1.set_xlim(900, 1100)
# ax1.set_ylim(0, 20000)
ax1.grid(True)
ax1.set_title('100ms Dark')
plt.show()