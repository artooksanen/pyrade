from photutils.datasets import load_star_image
from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import astropy.io.fits as fits
import hms
from astropy.coordinates import SkyCoord

#hdu = load_star_image()
#hdu.writeto('test.fits', overwrite=True)

#hdu = fits.open('test.fts')[0]
#hdu = fits.open('solved_with_astrometrynet.fits')[0]
hdu = fits.open('solved_with_twirl.fits')[0]

data, true_wcs = hdu.data, WCS(hdu.header)
mean, median, std = sigma_clipped_stats(data, sigma=3.0)

print("original wcs:",true_wcs)
#x=1000.0
#y=750.0
#sky=true_wcs.pixel_to_world(x,y)
#r0, d0 = sky.ra.deg/15.0, sky.dec.deg
#               r=wcs.wcs.crval[0]/15.0   
#               d=wcs.wcs.crval[1]
#print(" ra 2000:",hms.hhmmss(r0))
#print(" de 2000:",hms.sddmmss(d0))


from twirl import find_peaks

xy = find_peaks(data)[0:20]

import numpy as np
import matplotlib.pyplot as plt
from photutils.aperture import CircularAperture

plt.imshow(data, vmin=np.median(data), vmax=3 * np.median(data), cmap="Greys_r")
_ = CircularAperture(xy, r=10.0).plot(color="y")

plt.show()

from astropy.wcs.utils import proj_plane_pixel_scales

#fov = (data.shape * proj_plane_pixel_scales(true_wcs))[0]
#center = true_wcs.pixel_to_world(*np.array(data.shape) / 2)


image_width = hdu.header['NAXIS1']
image_height = hdu.header['NAXIS2']
image_center = [image_width / 2, image_height / 2]
print("image center:",image_center)

ra = hdu.header['OBJCTRA']
dec = hdu.header['OBJCTDEC']

center = SkyCoord(ra, dec, unit=["deg", "deg"])
print("solve sky center:",center)

from astropy import units as u

# and the size of its field of view
pixel=0.52
pixel_scale = pixel * u.arcsec  # known pixel scale
#shape = hdu.data.shape
fov = 2000 * pixel_scale.to(u.deg)

from twirl import gaia_radecs
from twirl.geometry import sparsify

print("fov:",fov)
print("center:",center)

all_radecs = gaia_radecs(center, 2.0 * fov,100)

# we only keep stars 0.01 degree apart from each other
all_radecs = sparsify(all_radecs, 0.01)

from twirl import compute_wcs

# we only keep the 12 brightest stars from gaia
wcs = compute_wcs(xy, all_radecs[0:10], tolerance=1,asterism=4,min_match=0.9)

print("\nwcs:",wcs)
#x=1000.0
#y=750.0
#sky=wcs.pixel_to_world(x,y)

image_width = hdu.header['NAXIS1']
image_height = hdu.header['NAXIS2']
image_center = [image_width / 2, image_height / 2]
print("image center:",image_center)

from astropy.wcs import utils

coord_again = utils.pixel_to_skycoord(image_center[0],image_center[1], wcs) #can handle list of objects ([x1,x2],[y1,y2])
print("coord_again r,d (wcs):",coord_again) #,hms.hhmmss(coord_again[0]/15.0),hms.sddmmss(coord_again[1]))


center = true_wcs.pixel_to_world_values([(image_center[0],image_center[1])])
print("center (true_wcs):",center)
center = wcs.pixel_to_world_values([(image_center[0],image_center[1])])
print("center r,d (wcs):",center)
center_w = wcs.world_to_pixel_values([center[0]])
print("center x,y (wcs):",center_w)

#r, d = sky.ra.deg/15.0, sky.dec.deg
#print(" ra 2000:",hms.hhmmss(r))
#print(" de 2000:",hms.sddmmss(d))


# plotting to check the WCS
radecs_xy = np.array(wcs.world_to_pixel_values(all_radecs))
plt.imshow(data, vmin=np.median(data), vmax=3 * np.median(data), cmap="Greys_r")
_ = CircularAperture(radecs_xy[0:10], 5).plot(color="r", alpha=0.5)

#save image

header = wcs.to_header()
hdu.header.update(header)
hdu.writeto('resolved_with_twirl.fits', overwrite=True)

plt.show()
