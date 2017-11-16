"""
B. Connor McClellan
16 November 2017

Uses the wavelength solution derived from known emission spectra to check the difference
between the fitted wavelength (a function of pixel position) and the actual known
wavelength.
"""

import matplotlib.pyplot as plt
import numpy as np


def rms(x):
    return (np.absolute(np.mean(x**2) - (np.mean(x))**2))**0.5


# EMISSION SPECTRA
x = [712.469086748, 804.11082494, 1008.08526837, 1243.67810525, 170.751184558, 1392.43596457, 278.6280747, 1354.78143834, 336.45902757, 650.552477104, 691.713891716]
known = [501, 492, 471, 447, 557.03, 431.96, 546.07, 435.84, 540.06, 508.04, 503.78]
names = ["He 501", "He 492", "He 471", "He 447", "Kr 557.03", "Kr 431.96", "Hg 546.07", "Hg 435.84", "Ne 540.06", "Ne 508.04", "Ne 503.78"]

# Emission fit
coeff = np.polyfit(x, known, 2)
q = np.poly1d(coeff)

# Calculate residual
fitted = q(x)
difference = fitted - known
rms_difference = rms(difference)

# Set up values for wavelength solution line
x_val = np.linspace(100, 1800, 1000)
y_val = q(x_val)

# PLOTTING
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(x, difference)
ax.axhline(0, color='k', ls='--')
for i, name in enumerate(names):
    ax.annotate(name, (x[i]+5, difference[i]), fontsize=9)
ax.annotate("RMS = %.4f" % rms_difference, (1100, -0.35))
ax.set_xlabel("x position, in px")
ax.set_ylabel("Residual wavelength (Fit - Known), in nm")
plt.title("Fit Wavelength Minus Known Wavelength v. X Position")
plt.savefig("residuals.png")