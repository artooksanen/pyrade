import hor
import telescope
import time
import solve
import camera
import hms
import epoch
import math
import epoch
import os

f=open("2025-08-22T00_00_14_priority_candidates.tsv", "r")
rows=f.readlines()
n=0
for row in rows:
    print(row.split("\t"))
    r=float(row.split("\t")[1])/15.0
    d=float(row.split("\t")[2])
    r2025,d2025=epoch.precess(r,d,2000.0,2025.0)
    print(r,d)
    telescope.slew(r2025,d2025)
    while telescope.slewing():
        time.sleep(1)
        print("slewing...")
        while not telescope.tracking():
            time.sleep(1)
        print("tracking...")
        time.sleep(1)
        print("taking image...")
        ra=telescope.rightascension()
        dec=telescope.declination()
        r2000,d2000=epoch.precess(ra,dec,2025.0,2000.0)
        n=n+1
        image_name="snews_"+str(n)
        img_file=camera.take_image(image_name,10,ra,dec,pixel_scale=1.68)
        print("solving...")
        #r2000,d2000=epoch.precess(ra,dec,2025.5,2000.0)
        r2000,d2000=epoch.precess(ra,dec,2025.0,2000.0)
        wcs=solve.solve(img_file,r2000,d2000)
        if wcs != None:
            print("wcs:",wcs)    
            x=1000/2.0
            y=1000/2.0
            sky=wcs.pixel_to_world(x,y)
            r, d = sky.ra.deg/15.0, sky.dec.deg
            print(" ra 2000:",hms.hhmmss(r))
            print(" de 2000:",hms.sddmmss(d))
            
f.close()