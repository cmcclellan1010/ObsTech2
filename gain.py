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
# testdata = construct_data_array('flat_1e5ms_', 3)
# master_dark_1e5ms = np.median(construct_data_array('dark_1e5ms_', 3), axis=0)
# testdata -= master_dark_1e5ms
# average_of_square = np.mean(testdata ** 2, axis=0)
# print average_of_square
# square_of_average = (np.mean(testdata, axis=0)) ** 2
# print square_of_average
# variance = np.absolute(average_of_square - square_of_average)
# print variance

prefix_list = ['flat_1e4ms_', 'flat_1e5ms_', 'flat_3e4ms_', 'flat_6e4ms_', 'flat_12e4ms_']
y = np.ndarray((len(prefix_list), 390150))
x = np.ndarray((len(prefix_list), 390150))

for prefix in prefix_list:
    i = prefix_list.index(prefix)

    # Calculate mean array
    data = construct_data_array(prefix, 3)
    mean_array = np.mean(data, axis=0)
    print mean_array[1][0]
    # READ NOISE 1, 2: Calculate RMS array
    average_of_square = np.mean(data**2, axis=0)
    print average_of_square[1][0]
    square_of_average = (np.mean(data, axis=0))**2
    print square_of_average[1][0]
    variance = np.absolute(average_of_square - square_of_average)
    print "VARIANCE: ", variance[1][0]

# Plot variance vs signal
    y[i] = np.mean(np.ndarray.flatten(variance))
    x[i] = np.mean(np.ndarray.flatten(mean_array))

#
# fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(17, 11))
#
# ax1.plot(x[0], y[0], 'bo')
# ax1.set_title('1e4 ms')
# ax1.set_xlabel('Signal (e-)')
# ax1.set_ylabel('Variance (RMS^2)')
#
# ax2.plot(x[3], y[3], 'bo')
# ax2.set_title('3e4 ms')
# ax2.set_xlabel('Signal (e-)')
# ax2.set_ylabel('Variance (RMS^2)')
#
# ax3.plot(x[4], y[4], 'bo')
# ax3.set_title('6e4 ms')
# ax3.set_xlabel('Signal (e-)')
# ax3.set_ylabel('Variance (RMS^2)')
#
# ax4.plot(x[1], y[1], 'bo')
# ax4.set_title('1e5 ms')
# ax4.set_xlabel('Signal (e-)')
# ax4.set_ylabel('Variance (RMS^2)')
#
# ax5.plot(x[5], y[5], 'bo')
# ax5.set_title('12e4 ms')
# ax5.set_xlabel('Signal (e-)')
# ax5.set_ylabel('Variance (RMS^2)')
#
# ax6.plot(x[2], y[2], 'bo')
# ax6.set_title('2e5 ms')
# ax6.set_xlabel('Signal (e-)')
# ax6.set_ylabel('Variance (RMS^2)')
#
# plt.tight_layout()
# plt.show()
#
x_total = np.ndarray.flatten(x[0:5])
y_total = np.ndarray.flatten(y[0:5])

l_init = models.Linear1D(slope=1, intercept=1)
fit_l = fitting.LinearLSQFitter()
l = fit_l(l_init, x_total, y_total)
slope, intercept = l.slope[0], l.intercept[0]
print "Slope, Intercept: ", slope, intercept

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(x_total, y_total, 'bo')
plt.plot(x_total, l(x_total), 'r')
plt.xlabel('Signal (e-)')
plt.ylabel('Variance (RMS^2)')
plt.show()