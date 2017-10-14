from astropy import units as u
from astropy.coordinates import Angle as a



def return_properties(f_length, D, f_number, pix_size, array_x, array_y):
    print "Focal length: ", f_length, " m"
    print "Diameter: ", D, " m"
    print "F/#: F/"+str(f_number)
    platescale = 206265 * pix_size * 10**-6 / f_length
    print "Plate scale: ", format(platescale, '.3f'), ' "/px'
    print "Array size: ", array_x, ' x ', array_y, " pixels"
    x_fov = a(array_x*platescale, unit=u.arcsec)
    y_fov = a(array_y*platescale, unit=u.arcsec)
    print "FOV: ", "{0.value:0.03f}".format(x_fov.to(u.arcmin)), ' x ', "{0.value:0.03f}".format(y_fov.to(u.arcmin))


print "DMK 23U274 without focal reducer: "
return_properties(3.556, 0.356, 10, 4.4, 1600, 1200)

print "\nDMK 23U274 with focal reducer: "
return_properties(2.243, 0.356, 6.3, 4.4, 1600, 1200)

print "\nDMK 23U445 without focal reducer: "
return_properties(3.556, 0.356, 10, 3.75, 1280, 960)

print "\nDMK 23U445 without focal reducer: "
return_properties(2.243, 0.356, 6.3, 3.75, 1280, 960)
