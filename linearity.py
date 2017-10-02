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


# CLEAR FILTER
flat_100ms = construct_data_array('flat_100ms_', 3)
flat_500ms = construct_data_array('flat_500ms_', 3)
flat_1000ms = construct_data_array('flat_1000ms_', 3)
flat_3000ms = construct_data_array('flat_3000ms_', 3)
flat_1e4ms = construct_data_array('flat_1e4ms_', 3)
flat_3e4ms = construct_data_array('flat_3e4ms_', 3)
flat_6e4ms = construct_data_array('flat_6e4ms_', 3)
flat_1e5ms = construct_data_array('flat_1e5ms_', 3)
flat_2e5ms = construct_data_array('flat_2e5ms_', 3)
flat_12e4ms = construct_data_array('flat_12e4ms_', 3)
flat_15e4ms = construct_data_array('flat_15e4ms_', 1)

data_list = [flat_100ms, flat_500ms, flat_1000ms, flat_3000ms, flat_1e4ms,
             flat_3e4ms, flat_6e4ms, flat_1e5ms, flat_12e4ms, flat_15e4ms, flat_2e5ms]

exptimes = [.1, .5, 1, 3, 10, 30, 60, 100, 120, 150, 200]
signal = []
signal_err = []
for data in data_list:
    mean_signal = np.mean(np.mean(data, axis=0))
    mean_err = rms(np.mean(data, axis=0))/390150.**0.5
    signal.append(mean_signal)
    signal_err.append(mean_err)

print signal
print signal_err


# BLUE FILTER
flat_low_1000ms = construct_data_array('flat_low_1000ms_', 3)
flat_low_3000ms = construct_data_array('flat_low_3000ms_', 3)
flat_low_1e4ms = construct_data_array('flat_low_1e4ms_', 3)
flat_low_3e4ms = construct_data_array('flat_low_3e4ms_', 3)
flat_low_6e4ms = construct_data_array('flat_low_6e4ms_', 3)
flat_low_1e5ms = construct_data_array('flat_low_1e5ms_', 3)
flat_low_12e4ms = construct_data_array('flat_low_12e4ms_', 3)

data_list = [flat_low_1000ms, flat_low_3000ms, flat_low_1e4ms, flat_low_3e4ms,
             flat_low_6e4ms, flat_low_1e5ms, flat_low_12e4ms]

low_exptimes = [1, 3, 10, 30, 60, 100, 120]
low_signal = []
low_signal_err = []
for data in data_list:
    low_mean_signal = np.mean(np.mean(data, axis=0))
    low_mean_err = rms(np.mean(data, axis=0))/390150.**0.5
    low_signal.append(low_mean_signal)
    low_signal_err.append(low_mean_err)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 11))

ax1.plot(exptimes, signal, 'b', linewidth=3)
ax1.set_xlabel('Exposure time (s)')
ax1.set_xlim(-10, 210)
ax1.set_ylabel('Signal (DN)')
ax1.set_ylim(0, 70000)
ax1.set_title('Signal v. Exposure Time for High Light Levels')

ax2.plot(low_exptimes, low_signal, 'limegreen', linewidth=3)
ax2.set_xlabel('Exposure time (s)')
ax2.set_xlim(-10, 210)
ax2.set_ylabel('Signal (DN)')
ax2.set_ylim(0, 70000)
ax2.set_title('Signal v. Exposure Time for Low Light Levels')

plt.tight_layout()
plt.show()
