import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#%matplotlib inline

import glob
from astropy.io import fits
from scipy.ndimage import interpolation as interp

from skimage.feature.register_translation import (register_translation, _upsampled_dft)


# This turns off warnings: not a great way to code
# But when we show the images, sometimes we're taking the logarithm of zero and it doesn't like that
# Which would matter if we were doing math, but we're just taking a look at images, so we can ignore it. 
import warnings
warnings.filterwarnings('ignore')

def plot_grid(datacube,imagenames):
    no_A = len(datacube) ## number of individual images in the cube
    xplots = int(np.around(np.sqrt(no_A))) ## number of image grid columns
    yplots = xplots + 1 ## number of image grid rows--sometimes there are one fewer, but that's okay

#     print no_A, xplots, yplots ## this line is for troubleshooting
    
    gs = gridspec.GridSpec(yplots, xplots) ## define the image grid
    plt.figure(figsize=(15,15)) ## set the figure size
    for i in range(no_A): 
        ## plots each individual image within the image grid: 
        B = datacube[i]
        plt.subplot(gs[i])
        plt.imshow(np.log10(B), origin='lower', cmap='gray')
        plt.title(imagenames[i])
        
# make a list of the dark files:
exptime = raw_input('Input the exposure time identifier for this dark frame: ')

dark_list = []
for file in glob.glob('*.fit'):
    if exptime in file:
        dark_list.append(file)

print "\nTotal images found with '"+exptime+"' in the filename: "+str(len(dark_list))
#print dark_list ##this line is for troubleshooting

raw_image_data = {}
for image_name in dark_list: raw_image_data[image_name] = fits.getdata(image_name)

print '\nFile dimension check:'
for image in dark_list: print raw_image_data[image].shape ##for troubleshooting
# (check to make sure they're all the same size)

# create an array of dark images
darkcube = np.stack([raw_image_data[dark_frame] for dark_frame in dark_list],axis=0)
#print darkcube.shape ## this line is for troubleshooting

# PREVIEW DARKCUBE
#plot_grid(darkcube,dark_list)
#plt.show()

# average-combine the darks into a single master image with lower noise

master_dark = np.average(darkcube, axis=0) ## to combine with an average
#master_dark = np.median(darkcube, axis=0) ## to median combine them instead

# PREVIEW MASTER DARK
#plt.figure(figsize=(15,15)) 
#plt.imshow(np.log10(master_dark), origin='lower', cmap='gray');
#plt.title('Master Dark')
#plt.show()

#save master dark to fits file
hdu = fits.PrimaryHDU(master_dark)
hdu.writeto('master_dark_'+str(exptime)+'.fit')

print "\nMaster dark image saved as 'master_dark_"+str(exptime)+".fit'."



