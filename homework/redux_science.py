import sys
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
    no_A = len(datacube) # number of individual images in the cube
    xplots = int(np.around(np.sqrt(no_A))) # number of image grid columns
    yplots = xplots + 1 # number of image grid rows--sometimes there are one fewer, but that's okay

#     print no_A, xplots, yplots # this line is for troubleshooting
    
    gs = gridspec.GridSpec(yplots, xplots) # define the image grid
    plt.figure(figsize=(15,15)) # set the figure size
    for i in range(no_A): 
        # plots each individual image within the image grid: 
        B = datacube[i]
        plt.subplot(gs[i])
        plt.imshow(np.log10(B), origin='lower', cmap='gray')
        plt.title(imagenames[i])

def stop():
    sys.exit("Stop encountered.")
    
# make a list of raw science images:
name = raw_input('Input the object name for the science frames (i.e. "cig" or "NGC2997"): ')
exptime = raw_input('Input the exposure time identifier for the science frames: ')
filter = raw_input('Input the filter identifier for the science frames: ')

science_list = []
for file in glob.glob('*.fit'):
    if name in file and exptime in file and "{}".format(filter) in file:
        science_list.append(file)
        
print 'Total images found: '+str(len(science_list))
print science_list # for troubleshooting

raw_image_data = {}
for image_name in science_list: raw_image_data[image_name] = fits.getdata(image_name)

print '\nFile dimension check:'
for image in science_list: print raw_image_data[image].shape #for troubleshooting
# (check to make sure they're all the same size)

# create an array of raw science images
sciencecube = np.stack([raw_image_data[science_frame] for science_frame in science_list],axis=0)

# PREVIEW SCIENCECUBE
#plot_grid(sciencecube,science_list)
#plt.show()

#load in master dark
hdu_list = fits.open('master_dark_'+exptime+'.fit')
master_dark = hdu_list[0].data
hdu_list.close()
print "\nLoading master dark 'master_dark_"+exptime+".fit'..."

dedark_list_in = science_list
#print dedark_list_in # for troubleshooting

# filenames for the corresponding dark-subtracted images:
dedark_list_out = ['dedarked_' + im for im in dedark_list_in]

# subtract the master dark from each of the raw science frames: 

dedark_data_out = {} # dictionary for the dark-subtracted images

for i in range(len(dedark_list_in)):  
    dedark_data_out[dedark_list_out[i]] = raw_image_data[dedark_list_in[i]] - master_dark
print "Dark subtraction successful!"
# create an array of dark-subtracted images
dedarkcube = np.stack([dedark_data_out[image] for image in dedark_list_out],axis=0)

# show the images: 
#plot_grid(dedarkcube,dedark_list_out)
#plt.show()

#load in master flat
hdu_list = fits.open('master_flat_'+filter+'.fit')
master_flat = hdu_list[0].data
hdu_list.close()
print "\nLoading master flat 'master_flat_"+filter+".fit'..."

# we'll start with a list of the dedarked science images: 
dedark_science_list = ['dedarked_' + im for im in science_list]
# print dedark_science_list ## this line is for troubleshooting

# and we'll make a corresponding list to name the flattened images: 
flat_dedark_science_list = ['flattened_' + im for im in dedark_science_list]
# print flat_dedark_science_list ## this line is for troubleshooting

# create an empty dictionary to populate with the completely corrected science frames: 
flat_dedark_data_out = {} 

# and populate the dictionary with each corrected image
# where the dictionary keys = the images in flat_dedark_science_list
# we're iterating over an integer here again because the lists match up
for i in range(len(dedark_science_list)): 
    flat_dedark_data_out[flat_dedark_science_list[i]] = \
    dedark_data_out[dedark_science_list[i]]/master_flat
print "Flattening successful!"

# create an array of corrected science images
sciencecube = np.stack([flat_dedark_data_out[science_frame] for science_frame in flat_dedark_science_list],axis=0)
# print sciencecube ## this line is for troubleshooting
# sciencecube.shape ## this line is for troubleshooting

print "\nRecord the number of the reference image to use for alignment, and close the figure."
# show the images: 
plot_grid(sciencecube,science_list)
plt.show()

selection = raw_input('Type the number of the desired reference image for alignment. (1-'+str(len(flat_dedark_science_list))+'): ')
zero_shift_image = flat_dedark_science_list[int(selection)-1]

print "\nShifting and stacking images..."
# find all shifts for other images: 
imshifts = {} # dictionary to hold the x and y shift pairs for each image
for image in flat_dedark_science_list: 
    # register_translation is a function that calculates shifts by comparing 2-D arrays
    result, error, diffphase = register_translation(
        flat_dedark_data_out[zero_shift_image], 
        flat_dedark_data_out[image], 750)
    imshifts[image] = result
    
# print imshifts ## for troubleshooting

# new list for shifted image names: 
shifted_science_list = ['shifted_' + im for im in flat_dedark_science_list]

# new dictionary for shifted image data: 
shifted_science_data = {}
for i in range(len(shifted_science_list)):
    # interp.shift is the function doing the heavy lifting here,
    # it's reinterpolating each array into the new, shifted one
    shifted_science_data[shifted_science_list[i]] = interp.shift(
        flat_dedark_data_out[flat_dedark_science_list[i]], 
        imshifts[flat_dedark_science_list[i]])

# array of aligned arrays: 
sciencecube = np.stack(shifted_science_data.values(),axis=0)

## average combined final image: 
science_stacked = np.average(sciencecube, axis=0)

## show the final image array as an image: 
plt.figure(1)
plt.figure(figsize=(15,15));
plt.title('Aligned and Stacked Science image');
plt.imshow(np.log10(science_stacked), origin='lower', cmap='gray', vmin=1.5, vmax=3)
plt.show()

#save image to fits file
hdu = fits.PrimaryHDU(science_stacked)
hdu.writeto('stacked_'+name+'_'+exptime+'_'+filter+'.fit')

print "\nStacked science image saved as 'stacked_"+name+"_"+exptime+"_"+filter+".fit'."