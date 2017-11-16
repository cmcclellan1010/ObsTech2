"""
B. Connor McClellan
16 November 2017

Uses laser wavelengths to estimate wavelength as a function of pixel position.
Use for rough estimation only.
"""

import numpy as np


def guess():
    while True:
        input = float(raw_input("Input x: "))
        print "Wavelength = ", p(input)


x = [1565.24764259, 410.762735969]
y = [405, 532]

p = np.poly1d(np.polyfit(x, y, 1))
guess()
