"""
B. Connor McClellan
16 November 2017

Loads in a numpy matrix in the format of [x positions, counts].
Within a region specified by two mouse clicks, calculates the
average central pixel position in the region, weighted by the
counts. Intended for identifying the centroids of spectral
emission features.
"""

import numpy as np
import matplotlib.pyplot as plt


def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print 'x = %d, y = %d'%(
        ix, iy)

    global coords
    coords.append((ix, iy))

    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)


def load_matrix(filename):
    data = np.load(filename)
    length = len(data)
    x_positions = np.zeros(length)
    counts = np.zeros(length)
    for i in range(length):
        x_positions[i] = data[i][0]
        counts[i] = data[i][1]
    data = np.asarray([x_positions, counts])
    return data


filename = "neon_06s_data.npy"
data = load_matrix(filename)

fig = plt.figure(figsize=(17, 17))
ax = fig.add_subplot(111)
ax.plot(data[0], data[1])

# Get mouse coordinates for two clicks
coords = []
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show(1)

# Only need x coordinates from mouse clicks
x0, x1 = int(coords[0][0]), int(coords[1][0])

# Relate x coordinates to their index in the full dataset
x0_index = int((x0 - data[0])[0])
x1_index = int((x1 - data[0])[0])

# These are the indices of all selected x points
x_range = range(x0_index, x1_index)

# Assemble x points and counts for each x point in range
x_points = np.arange(x0, x1, 1)
counts_points = np.zeros(len(x_range))
for i in range(len(x_points)):
    counts_points[i] = data[1][x_range[i]]

# Use weighted average to find centroid x position
counts_total = np.sum(counts_points)
sum = 0.
for i in range(len(x_points)):
    weight = counts_points[i]/counts_total
    sum += weight*x_points[i]
x_centroid = sum

# Copy this to the clipboard after running
print "Centroid of feature: ", x_centroid

# PLOTTING
plt.figure()
plt.plot(data[0], data[1])
plt.plot(x_points, counts_points, 'r-', linewidth=2)
plt.axvline(x_centroid, color='k')
plt.show()



