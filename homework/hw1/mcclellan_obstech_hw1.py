# B. Connor McClellan
# 6 November 2017

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from glob import glob
from astropy.io import fits


def plot_grid(datacube, imagenames):
    no_A = len(datacube)
    xplots = int(np.around(np.sqrt(no_A)))
    yplots = xplots + 1
    gs = gridspec.GridSpec(yplots, xplots)
    plt.figure(figsize=(15, 15))
    for i in range(no_A):
        B = datacube[i]
        plt.subplot(gs[i])
        plt.imshow(np.log10(B), origin='lower', cmap='gray')
        plt.title(imagenames[i])

exptime = raw_input('Input the exposure time identifier for this dark frame: ')
dark_list = []
for file in glob('*.fit'):
    if exptime in file:
        dark_list.append(file)

print "\nTotal images found: ", len(dark_list)

raw_image_data = {}
for image_name in dark_list:
    raw_image_data[image_name] = fits.getdata(image_name)

for dark_frame in dark_list:
    darkcube = np.stack([raw_image_data[dark_frame]], axis=0)

plot_grid(darkcube, dark_list)
plt.show()

master_dark = np.median(darkcube, axis=0)

hdu = fits.PrimaryHDU(master_dark)
hdu.writeto('master_dark_'+str(exptime)+'.fit')

print "\nMaster dark image saved as 'master_dark_"+str(exptime)+".fit'."