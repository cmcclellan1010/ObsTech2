"""
B. Connor McClellan
16 November 2017

Loads in a Pepito spectrum, uses two mouse clicks to designate a line across one fiber.
A counts v. pixel position plot is projected along this line, and a data  matrix is saved
 for later analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from astropy.io import fits
from scipy import ndimage
from os.path import splitext


def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print 'x = %d, y = %d'%(
        ix, iy)

    global coords
    coords.append((ix, iy))

    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)


filename = "neon_06s.fit"
data = fits.open(filename)[0].data

x = np.arange(data.shape[1])
y = np.arange(data.shape[0])

# Show raw image data
fig = plt.figure(figsize=(17,17))
ax = fig.add_subplot(111)
ax.imshow(data)

# Collect mouse location information
coords = []
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show(1)

x0, y0 = int(coords[0][0]), int(coords[0][1])
x1, y1 = int(coords[1][0]), int(coords[1][1])

# Set up x and y space
npoints = x1 - x0
xvalues = np.linspace(x0, x1, npoints)
yvalues = np.linspace(y0, y1, npoints)

# Bin the counts into their appropriate x pixels
sliced_counts = ndimage.map_coordinates(data, np.vstack((yvalues, xvalues)))
x_positions = np.arange(x0, x1, 1)

# Save the matrix
np.save(splitext(filename)[0]+'_data.npy', np.column_stack((x_positions, sliced_counts)))

# Check to make sure the dimensions are the same
print len(sliced_counts)
print len(x_positions)

# PLOTTING
fig = plt.figure(figsize=(22, 8))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
ax1 = plt.subplot(gs[0])
ax1.imshow(data)
ax1.set_xlabel("X pixel position")
ax1.set_ylabel("Y pixel position")
ax1.plot([x0, x1], [y0, y1], 'r-')
ax1.axis('image')

ax2 = plt.subplot(gs[1])
ax2.set_xlabel("X pixel position")
ax2.set_ylabel("Counts")
ax2.plot(x_positions, sliced_counts)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.suptitle(filename)
plt.savefig(splitext(filename)[0]+'_plot.png')