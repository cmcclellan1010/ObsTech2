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
        
# make a list of flat images:
exptime = raw_input('Input the exposure time identifier for this flat frame: ')
filter = raw_input('Input the filter identifier for this flat frame: ')
print "Searching for '.fit' files with '"+exptime+"' and '"+filter+"' in the filename..."

flat_list = []
for file in glob.glob('*.fit'):
    if exptime in file and "{}".format(filter) in file:
        flat_list.append(file)

print 'Total images found: '+str(len(flat_list))
print flat_list # for troubleshooting

raw_image_data = {}
for image_name in flat_list: raw_image_data[image_name] = fits.getdata(image_name)

print '\nFile dimension check:'
for image in flat_list: print raw_image_data[image].shape #for troubleshooting
# (check to make sure they're all the same size)

# create an array of flat images
flatcube = np.stack([raw_image_data[flat_frame] for flat_frame in flat_list],axis=0)

# PREVIEW FLATCUBE
#plot_grid(flatcube,flat_list)
#plt.show()


hdu_list = fits.open('master_dark_'+str(exptime)+'.fit')
master_dark = hdu_list[0].data

# filneames of flats that have not yet been dark-subtracted: 
dedark_list_in = flat_list
#print dedarklist_in # for troubleshooting

# filenames for the corresponding dark-subtracted images:
dedark_list_out = ['dedarked_' + im for im in dedark_list_in]

# subtract the master dark from each of the flat frames: 
dedark_data_out = {} # dictionary for the dedarked images

for i in range(len(dedark_list_in)):  
    dedark_data_out[dedark_list_out[i]] = raw_image_data[dedark_list_in[i]] - master_dark

# create an array of dedarked images
dedarkcube = np.stack([dedark_data_out[image] for image in dedark_list_out],axis=0)

# show the images: 
#plot_grid(dedarkcube,dedark_list_out)
#plt.show()

# first we need a list of JUST the dedarked flat images to work with: 
dedark_flat_list = ['dedarked_' + image for image in flat_list] 

# create an array of dedarked flat images 
flatcube = np.stack([dedark_data_out[flat_frame] for flat_frame in dedark_flat_list],axis=0)

# average the images in the stack
master_flat = np.average(flatcube, axis=0)

# PREVIEW MASTER FLAT
plt.figure(figsize=(15,15))
plt.imshow((master_flat), origin='lower', cmap='gray', vmin=5250, vmax=6000)
plt.title('Master Flat')
plt.show()

print '\nmaster flat median: ' + str(np.median(master_flat)) + " counts"
print 'master flat mean: ' + str(np.mean(master_flat)) + " counts"
print 'master flat max value: ' + str(np.max(master_flat)) + " counts"
print 'master flat min value: ' + str(np.min(master_flat)) + " counts"

normalized_master_flat = master_flat/np.mean(master_flat)

# common sense statistics check: 

print '\nnormalized master flat median: ' + str(np.median(normalized_master_flat))
print 'normalized master flat mean: ' + str(np.mean(normalized_master_flat))
print 'normalized master flat max value: ' + str(np.max(normalized_master_flat))
print 'normalized master flat min value: ' + str(np.min(normalized_master_flat))

#save master dark to fits file
hdu = fits.PrimaryHDU(normalized_master_flat)
hdu.writeto('master_flat_'+filter+'.fit')

print "\nNormalized master flat image saved as 'master_flat_"+filter+".fit'."


