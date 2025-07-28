from photutils.datasets import load_star_image
from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import astropy.io.fits as fits
import hms
from astropy.coordinates import SkyCoord

#hdu = load_star_image()

hdu = fits.open("c:/users/oksanart/sky/new-image.fits")[0]

data, true_wcs = hdu.data, WCS(hdu.header)
mean, median, std = sigma_clipped_stats(data, sigma=3.0)

print("true_wcs:",true_wcs)
x=1000.0
y=750.0
sky=true_wcs.pixel_to_world(x,y)
r0, d0 = sky.ra.deg/15.0, sky.dec.deg
#               r=wcs.wcs.crval[0]/15.0   
#               d=wcs.wcs.crval[1]
print(" ra 2000:",hms.hhmmss(r0))
print(" de 2000:",hms.sddmmss(d0))


from twirl import find_peaks

xy = find_peaks(data)[0:20]

import numpy as np
import matplotlib.pyplot as plt
from photutils.aperture import CircularAperture

plt.imshow(data, vmin=np.median(data), vmax=3 * np.median(data), cmap="Greys_r")
_ = CircularAperture(xy, r=10.0).plot(color="y")

#plt.show()

from astropy.wcs.utils import proj_plane_pixel_scales

fov = (data.shape * proj_plane_pixel_scales(true_wcs))[0]
center = true_wcs.pixel_to_world(*np.array(data.shape) / 2)

from twirl import gaia_radecs
from twirl.geometry import sparsify

all_radecs = gaia_radecs(center, 2.0 * fov)

# we only keep stars 0.01 degree apart from each other
#all_radecs = sparsify(all_radecs, 0.01)

from twirl import compute_wcs

# we only keep the 12 brightest stars from gaia
wcs = compute_wcs(xy, all_radecs[0:10], tolerance=10)

print("wcs:",wcs)
x=1000.0
y=750.0
sky=wcs.pixel_to_world(x,y)

center = SkyCoord(r0*15.0, d0, unit=["deg", "deg"])
print(wcs.world_to_pixel(center))

r, d = sky.ra.deg/15.0, sky.dec.deg
print(" ra 2000:",hms.hhmmss(r))
print(" de 2000:",hms.sddmmss(d))


# plotting to check the WCS
radecs_xy = np.array(wcs.world_to_pixel_values(all_radecs))
plt.imshow(data, vmin=np.median(data), vmax=3 * np.median(data), cmap="Greys_r")
_ = CircularAperture(radecs_xy[0:10], 5).plot(color="y", alpha=0.5)


plt.show()
