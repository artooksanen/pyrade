import hor
import telescope
import time
import solve
import camera
import hms
import epoch
import math
import epoch

for a in range(0,360,30):
    for e in range(10,80,30):
        t=hor.ttojd(time.time())
        r,d=hor.hortoeq(a,e,t)
        print("t=",t,"a=",a,"e=",e,"r=",r,"d=",d)
        if d<60.0:
            telescope.slew(r,d)
            while telescope.slewing():
                time.sleep(1)
                print("slewing...")
            while not telescope.tracking():
                time.sleep(1)
            print("tracking...")
            time.sleep(10)
            print("taking image...")
            ra=telescope.rightascension()
            dec=telescope.declination()
            img_file=camera.take_image(60,ra,dec,pixel_scale=0.52)
            ta=hor.taika(t)
            print("solving...")
            r2000,d2000=epoch.precess(ra,dec,2025.5,2000.0)
            wcs=solve.solve(img_file,r2000,d2000)
            if wcs != None:
                #print("wcs:",wcs)    
                x=2000/2.0
                y=1500/2.0
                sky=wcs.pixel_to_world(x,y)
                r, d = sky.ra.deg/15.0, sky.dec.deg
 #               r=wcs.wcs.crval[0]/15.0   
 #               d=wcs.wcs.crval[1]
                #print(" ra 2000:",hms.hhmmss(r))
                #print(" de 2000:",hms.sddmmss(d))
                r1,d1=epoch.precess(r,d,2000.0,2025.5)    
                print(" r1:",hms.hhmmss(r1))
                print(" d1:",hms.sddmmss(d1))
                
                print("tpoint:",hms.hhmmss(r1),hms.sddmmss(d1),hms.hhmmss(ra),hms.sddmmss(dec),hms.rh(ta),(ta-hms.rh(ta))*60.0)
                print("pointing error (arc sec): {:.1f} {:.1f}".format(((r1-ra)*3600.0)/math.cos(math.radians(dec)),(d1-dec)*3600.0))

