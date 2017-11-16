"""
B. Connor McClellan
16 November 2017

Constructs and plots a 2nd order polyfit for a list of x coordinates and
their corresponding known wavelengths, which have been identified using
online references.
"""

import matplotlib.pyplot as plt
import numpy as np

# EMISSION SPECTRA
x = [712.469086748, 804.11082494, 1008.08526837, 1243.67810525, 170.751184558, 1392.43596457, 278.6280747, 1354.78143834, 336.45902757, 650.552477104, 691.713891716]
wavelength = [501, 492, 471, 447, 557.03, 431.96, 546.07, 435.84, 540.06, 508.04, 503.78]
names = ["He 501", "He 492", "He 471", "He 447", "Kr 557.03", "Kr 431.96", "Hg 546.07", "Hg 435.84", "Ne 540.06", "Ne 508.04", "Ne 503.78"]

# Emission fit
coeff = np.polyfit(x, wavelength, 2)
q = np.poly1d(coeff)
emission_xvalues = np.linspace(100, 1800, 1000)

equation = "%.2E*x^2 + %.3f*x + %.3f" % (coeff[0], coeff[1], coeff[2])
print equation

# LASERS
laserx = [1565.24764259, 410.762735969]
laserwave = [405, 532]
lasernames = ["405 nm laser", "532 nm laser"]

# Laser fit
p = np.poly1d(np.polyfit(laserx, laserwave, 1))
laser_xvalues = np.linspace(100, 1800, 1000)


# PLOTTING
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(x, wavelength)
ax.scatter(laserx, laserwave, color='r')

# Plot emission fit
ax.plot(emission_xvalues, q(emission_xvalues), 'b', label = "2nd order polyfit of emission spectra")

# Plot laser fit
ax.plot(laser_xvalues, p(laser_xvalues), 'r--', alpha=0.5, label="Linear fit with two lasers")

# Label the data points
for i, name in enumerate(names):
    ax.annotate(name, (x[i]+5, wavelength[i]+5), fontsize=9)
for i, lasername in enumerate(lasernames):
    ax.annotate(lasernames[i], (laserx[i]+5, laserwave[i]+5), fontsize=9)

ax.set_xlabel("x position (px)")
ax.set_ylabel("Wavelength (nm)")
ax.annotate("Equation of emission fit: "+equation, (100, 360))
plt.title("Wavelength v. Position")
plt.legend()
plt.savefig("wavelength_v_pos.png")
