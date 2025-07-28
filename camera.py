import os
import time
import array
from alpaca.camera import *     # Sorry Python purists, this has multiple required Classes
import numpy as np
import astropy.io.fits as fits

def take_image(exposure_time,ra,de,pixel_scale):
#
# Set up the camera
#
    c = Camera('192.168.8.103:11111', 0)    # Connect to the ALpaca Omni Simulator
    c.Connected = True
    c.BinX = 1
    c.BinY = 1
# Assure full frame after binning change
    c.StartX = 0
    c.StartY = 0
    c.NumX = c.CameraXSize // c.BinX    # Watch it, this needs to be an int (typ)
    c.NumY = c.CameraYSize // c.BinY
#
# Acquire a light image, wait while printing % complete
#
    c.StartExposure(exposure_time, True)
    while not c.ImageReady:
        time.sleep(1.0)
        print(f'{c.PercentCompleted}% complete')
    print('finished')
#
# OK image acquired, grab the image array and the metadata
#
    img = c.ImageArray
    imginfo = c.ImageArrayInfo
    if imginfo.ImageElementType == ImageArrayElementTypes.Int32:
        if c.MaxADU <= 65535:
            imgDataType = np.uint16 # Required for BZERO & BSCALE to be written
        else:
            imgDataType = np.int32
    elif imginfo.ImageElementType == ImageArrayElementTypes.Double:
        imgDataType = np.float64
#
# Make a numpy array of he correct shape for astropy.io.fits
#
    if imginfo.Rank == 2:
        nda = np.array(img, dtype=imgDataType).transpose()
    else:
        nda = np.array(img, dtype=imgDataType).transpose(2,1,0)
#
# Create the FITS header and common FITS fields
#
    hdr = fits.Header()
    hdr['COMMENT'] = 'FITS (Flexible Image Transport System) format defined in Astronomy and'
    hdr['COMMENT'] = 'Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365.'
    hdr['COMMENT'] = 'Contact the NASA Science Office of Standards and Technology for the'
    hdr['COMMENT'] = 'FITS Definition document #100 and other FITS information.'
    if imgDataType ==  np.uint16:
        hdr['BZERO'] = 32768.0
        hdr['BSCALE'] = 1.0
    hdr['EXPOSURE'] = c.LastExposureDuration
    hdr['EXPTIME'] = c.LastExposureDuration
    #hdr['DATE-OBS'] = c.LastExposureStartTime
    hdr['TIMESYS'] = 'UTC'
    hdr['XBINNING'] = c.BinX
    hdr['YBINNING'] = c.BinY
    hdr['INSTRUME'] = c.SensorName
    hdr['OBJCTRA'] = ra*15.0   # degrees
    hdr['OBJCTDEC'] = de
    
    
# CRVALn #coordinate value at reference point
# CRPIXn #array location of the reference point in pixels
# CDELTn #coordinate increment at reference point
# CTYPEn #axis type (8 characters)
# CROTAn #rotation from stated coordinate type.

    hdr['CRVAL1'] = ra*15.0   # degrees
    hdr['CRVAL2'] = de   # degrees
    hdr['CRPIX1'] = c.CameraXSize/2.0
    hdr['CRPIX2'] = c.CameraYSize/2.0
    hdr['CDELT1'] = pixel_scale/3600.0   # degrees
    hdr['CDELT2'] = pixel_scale/3600.0   # degrees
    hdr['CTYPE1'] = 'RA--TAN'
    hdr['CTYPE2'] = 'DEC-TAN'
    hdr['CROTA1'] = 0.0 # degrees
    hdr['CROTA2'] = 0.0 # degrees

# CD1_1 = CDELT1 * cos (CROTA2)
# CD1_2 = -CDELT2 * sin (CROTA2)
# CD2_1 = CDELT1 * sin (CROTA2)
# CD2_2 = CDELT2 * cos (CROTA2)

    hdr['CD1_1'] = pixel_scale/3600.0 # degrees
    hdr['CD1_2'] = 0.0 # degrees
    hdr['CD2_1'] = 0.0 # degrees
    hdr['CD2_2'] = pixel_scale/3600.0 # degrees



    try:
        hdr['GAIN'] = c.Gain
    except:
        pass
    try:
        hdr['OFFSET'] = c.Offset
        if type(c.Offset == int):
            hdr['PEDESTAL'] = c.Offset
    except:
        pass
    hdr['HISTORY'] = 'Created using Python alpyca-client library'
#
# Create the final FITS from the numpy array and FITS info
#
    hdu = fits.PrimaryHDU(nda, header=hdr)

    img_file = 'test.fts'
    hdu.writeto(img_file, overwrite=True)
    c.Connected = False

    print("Booyah! Your FITS image is ready.", img_file)
    return img_file
