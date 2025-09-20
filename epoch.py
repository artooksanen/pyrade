 # epoch.py -- convert coordinates between epochs.
 #
 # transformations are based on equations appearing in
 # "Celestial BASIC" by Eric Burgess (SYBEX 1982)

import math

DEGTORAD = 3.14159265359/180.0

def DSIN(x):
    return math.sin((x)*DEGTORAD)

def DCOS(x):
    return math.cos((x)*DEGTORAD)

def DTAN(x):
    return math.tan((x)*DEGTORAD)

def precess(rin, din, ein, eout):
    t2 = ( (ein+eout)/2.0 - 1900.0 ) / 100.0
    x = 3.07234 + (0.00186 * t2)
    y = 20.0468 - (0.0085 * t2)
    z = y/15.0
    t = eout-ein
    w = 1.008 * t * (x + (z * DSIN(rin*15.0) * DTAN(din)) )
    d = 0.0168 * t * y * DCOS(rin*15.0)
    rout = rin + w/3600.0
    if (rout >= 24.0):
        rout -= 24.0
    if (rout < 0.0):
        rout += 24.0
    dout = din + d/60.0
    return (rout,dout)


if __name__ == '__main__':
    ra_2000=19+50/60.0+48/3600
    de_2000=8+52/60

    print("ra_2000=",ra_2000,"de_2000=",de_2000)
    ra_now,de_now=precess(ra_2000,de_2000,2000.0,2025.5)
    print("ra_date=",ra_now,"de_date=",de_now)
