from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt


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

prefix_list = ['flat_100ms_', 'flat_500ms_', 'flat_1000ms_', 'flat_3000ms_', 'flat_1e4ms_', 'flat_3e4ms_',
               'flat_6e4ms_', 'flat_12e4ms_']
y = []
x = []
yerr = []
xerr = []

for prefix in prefix_list:
    # Calculate mean array
    data = construct_data_array(prefix, 3)
    mean_array = np.mean(data, axis=0)
    mean_err = rms(mean_array)/390150.**0.5

    # READ NOISE 1, 2: Calculate RMS array
    average_of_square = np.mean(data**2, axis=0)
    square_of_average = (np.mean(data, axis=0))**2
    variance = np.absolute(average_of_square - square_of_average)
    variance_err = rms(variance)/390150.**0.5

    y.append(np.mean(variance))
    yerr.append(variance_err)
    x.append(np.mean(mean_array))
    xerr.append(mean_err)

for i in range(len(prefix_list)):
    print i
    print "Variance: ", '%.3f' % y[i]
    print "Variance Error: ", '%.3f' % yerr[i]
    print "Mean Signal: ", '%.3f' % x[i]
    print "Signal error: ", '%.3f' % xerr[i]
    if i == 0:
        pass
    else:
        print "dV/dS: ", '%.3f' % ((y[i]-y[i-1])/(x[i]-x[i-1]))

p, V = np.polyfit(x, y, 1, cov=True)
print "\nSlope: ", p[0]
print "Error in slope: ", np.sqrt(V[0][0])

yfit = []
for item in x:
    y1 = p[0]*item + p[1]
    yfit.append(y1)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='none', ecolor='b')
ax.annotate('Slope: '+str("%.2E" % p[0])+' ADU/e-', xy=(22000, 5000))
ax.annotate("Error in slope: "+str("%.2E" % np.sqrt(V[0][0]))+' ADU/e-', xy=(22000, 4000))
plt.plot(x, yfit, 'r')
plt.xlabel('Signal (e-)')
plt.ylabel('Variance (RMS^2)')
plt.show()
