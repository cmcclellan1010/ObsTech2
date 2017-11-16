"""
B. Connor McClellan
16 November 2017

Converts a bitmap image into a FIT image.
"""

import numpy as np
from scipy.misc import imread
from astropy.io import fits
from os.path import splitext
import glob


def convert_to_fits(filename):
    image_data = imread(filename).astype(np.float32)
    hdu = fits.PrimaryHDU(image_data)
    hdulist = fits.HDUList([hdu])
    hdulist.writeto(splitext(filename)[0]+'.fit')


for file in glob.glob('*.bmp'):
    convert_to_fits(file)
