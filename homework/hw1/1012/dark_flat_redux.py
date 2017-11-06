# B. Connor McClellan
# 6 November 2017

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import glob
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


dark_list = []
flat_list = []
for file in glob.glob('*.FIT'):
    if 'dark' in file:
        dark_list.append(file)
    elif 'flat' in file:
        flat_list.append(file)

print "\nTotal dark images found: ", len(dark_list)
print "\nTotal flat images found: ", len(flat_list)

dark_image_data = {}
for image_name in dark_list:
    dark_image_data[image_name] = fits.getdata(image_name)

darkcube = np.stack([dark_image_data[dark_frame] for dark_frame in dark_list],axis=0)

master_dark = np.median(darkcube, axis=0)

hdu = fits.PrimaryHDU(master_dark)
hdu.writeto('master_dark_2s_1012.fit')

print "\nMaster dark image saved as 'master_dark_2s_1012.fit'."

flat_image_data = {}
for image_name in flat_list:
    flat_image_data[image_name] = fits.getdata(image_name)

hdu_list = fits.open('master_dark_2s_1012.fit')
master_dark = hdu_list[0].data

dark_subtracted_list_in = flat_list
dark_subtracted_list_out = ['dark_subtracted_' + im for im in dark_subtracted_list_in]

dark_subtracted_data_out = {}
for i in range(len(dark_subtracted_list_in)):
    dark_subtracted_data_out[dark_subtracted_list_out[i]] = flat_image_data[dark_subtracted_list_in[i]] - master_dark

dark_subtracted_cube = np.stack([dark_subtracted_data_out[image] for image in dark_subtracted_list_out], axis=0)

master_flat = np.median(dark_subtracted_cube, axis=0)

print '\nmaster flat median:    ' + str(np.median(master_flat))
print 'master flat mean:      ' + str(np.mean(master_flat))
print 'master flat max value: ' + str(np.max(master_flat))
print 'master flat min value: ' + str(np.min(master_flat))

normalized_master_flat = master_flat/np.median(master_flat)

print '\nnormalized master flat median:    ' + str(np.median(normalized_master_flat))
print 'normalized master flat mean:      ' + str(np.mean(normalized_master_flat))
print 'normalized master flat max value: ' + str(np.max(normalized_master_flat))
print 'normalized master flat min value: ' + str(np.min(normalized_master_flat))

hdu = fits.PrimaryHDU(normalized_master_flat)
hdu.writeto('master_flat_r_1012.fit')

print "\nNormalized master flat image saved as 'master_flat_r_1012.fit'."


