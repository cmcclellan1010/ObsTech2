from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting


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
    print "Array shape: ", shape
    n_pixels = shape[1] * shape[2]
    print "Number of pixels: ", n_pixels
    return da

### EXPERIMENTAL SECTION ###
flat_1e4 = construct_data_array('flat_1e4ms_', 3)
signal_1e4 = np.mean(np.mean(flat_1e4, axis=0))
master_dark_1e4ms = np.median(construct_data_array('dark_1e4ms_', 3), axis=0)
flat_1e4 -= master_dark_1e4ms
average_of_square = np.mean(flat_1e4 ** 2, axis=0)
square_of_average = (np.mean(flat_1e4, axis=0)) ** 2
variance_1e4 = np.mean(np.absolute(average_of_square - square_of_average))


flat_1e5 = construct_data_array('flat_1e5ms_', 3)
signal_1e5 = np.mean(np.mean(flat_1e5, axis=0))
master_dark_1e5ms = np.median(construct_data_array('dark_1e5ms_', 3), axis=0)
flat_1e5 -= master_dark_1e5ms
average_of_square = np.mean(flat_1e5 ** 2, axis=0)
square_of_average = (np.mean(flat_1e5, axis=0)) ** 2
variance_1e5 = np.mean(np.absolute(average_of_square - square_of_average))

signal = np.asarray([signal_1e4, signal_1e5])
variance = np.asarray([variance_1e4, variance_1e5])

total_signal = np.ndarray.flatten(signal)
total_variance = np.ndarray.flatten(variance)

fig = plt.figure()
ax = fig.add_subplot(111)

l_init = models.Linear1D(slope=1, intercept=1)
fit_l = fitting.LinearLSQFitter()
l = fit_l(l_init, total_signal, total_variance)
slope, intercept = l.slope[0], l.intercept[0]
print "Slope, Intercept: ", slope, intercept


plt.plot(total_signal, total_variance, 'bo')
plt.plot(total_signal, l(total_signal), 'r')
plt.xlabel('Signal (e-)')
plt.ylabel('Variance (RMS^2)')
plt.show()