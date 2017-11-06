import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import glob
from astropy.io import fits
from scipy.ndimage import interpolation as interp

from skimage.feature.register_translation import (register_translation, _upsampled_dft)

import warnings
warnings.filterwarnings('ignore')

def plot_grid(datacube,imagenames):
    no_A = len(datacube) # number of individual images in the cube
    xplots = int(np.around(np.sqrt(no_A))) # number of image grid columns
    yplots = xplots + 1 # number of image grid rows--sometimes there are one fewer, but that's okay
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
    
name = raw_input('Input the object name for the science frames (i.e. "cig" or "NGC2997"): ')

science_list = glob.glob('stacked_'+name+'*.fit')

image_data = {}
for image_name in science_list: image_data[image_name] = fits.getdata(image_name)

#create science cube and plot b, v, and i in grid
sciencecube = np.stack([image_data[frame] for frame in science_list],axis=0)

print "\nRecord the index (first image is 1) of the reference image to use for alignment, and close the figure."
# show the images: 
plot_grid(sciencecube,science_list)
plt.show()


selection = raw_input('Type the number of the desired reference image for alignment. (1-'+str(len(science_list))+'): ')
zero_shift_image = science_list[int(selection)-1]

print "\nShifting images..."
# find all shifts for other images: 
imshifts = {} # dictionary to hold the x and y shift pairs for each image
for image in science_list: 
    # register_translation is a function that calculates shifts by comparing 2-D arrays
    result, error, diffphase = register_translation(
        image_data[zero_shift_image], 
        image_data[image], 1000)
    imshifts[image] = result
    
# print imshifts ## for troubleshooting

# new list for shifted image names: 
shifted_science_list = ['shifted_' + im for im in science_list]

# new dictionary for shifted image data: 
shifted_science_data = {}
for i in range(len(shifted_science_list)):
    # interp.shift is the function doing the heavy lifting here,
    # it's reinterpolating each array into the new, shifted one
    shifted_science_data[shifted_science_list[i]] = interp.shift(
        image_data[science_list[i]], 
        imshifts[science_list[i]])

# array of aligned arrays: 
sciencecube = np.stack(shifted_science_data.values(),axis=0)

#save image to fits file
for filename in shifted_science_list:
    filter = filename[-5:-4]
    print '\nFilter: '+filter
    hdu = fits.PrimaryHDU(shifted_science_data[filename])
    hdu.writeto('aligned_'+name+'_'+filter+'.fit')
    print "Aligned science image saved as 'aligned_"+name+"_"+filter+".fit'."