from pymeeus.Epoch import Epoch
from pymeeus.Mercury import Mercury
from pymeeus.Venus import Venus
from pymeeus.Earth import Earth
from pymeeus.Mars import Mars
from pymeeus.Jupiter import Jupiter
from pymeeus.Saturn import Saturn
from pymeeus.Uranus import Uranus
from pymeeus.Neptune import Neptune
from pymeeus.Pluto import Pluto
from pymeeus.Sun import Sun
from pymeeus.Moon import Moon
from pymeeus.Angle import Angle
import hor

def mercury(t):
  epoch=Epoch(t)
  ra, dec, elon = Mercury.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def venus(t):
  epoch=Epoch(t)
  ra, dec, elon = Venus.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def mars(t):
  epoch=Epoch(t)
  ra, dec, elon = Mars.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def jupiter(t):
  epoch=Epoch(t)
  ra, dec, elon = Jupiter.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def saturn(t):
  epoch=Epoch(t)
  ra, dec, elon = Saturn.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def uranus(t):
  epoch=Epoch(t)
  ra, dec, elon = Uranus.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def neptune(t):
  epoch=Epoch(t)
  ra, dec, elon = Neptune.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def pluto(t):
  epoch=Epoch(t)
  ra, dec, elon = Pluto.geocentric_position(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def sun(t):
  epoch=Epoch(t)
  ra, dec, r = Sun.apparent_rightascension_declination_coarse(epoch)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(ra/15.0,dec)

def moon(t):
  epoch=Epoch(t)
  ra, dec, Delta, ppi = Moon.apparent_equatorial_pos(epoch)
  Lambda, Beta, Delta, ppi = Moon.geocentric_ecliptical_pos(epoch)
  distance = Delta/149597871.0 #in AUs
  long,lat = hor.get_location()
  latitude=Angle(lat)
  ta=hor.taika(t)
  hour_angle = Angle(ta*15.0)
  top_ra, top_dec = Earth.parallax_correction(ra, dec, latitude, distance, hour_angle)
#  print(ra.ra_str(n_dec=1),dec.dms_str(n_dec=1))
  return(top_ra/15.0,top_dec)

if __name__ == '__main__':
  print("Mercury:")
  t=hor.tojd(2025,7,12,16,15,00)
  r,d=mercury(t)
  print("r=",r/15.0,"d=",d)

  right_ascension = Angle(22, 38, 7.25, ra=True)
  declination = Angle(-15, 46, 15.9)
  latitude = Angle(33, 21, 22)
  distance = 0.37276
  hour_angle = Angle(288.7958)
  top_ra, top_dec = Earth.parallax_correction(right_ascension, declination, latitude, distance, hour_angle)

  print("Corrected topocentric right ascension: ", top_ra.ra_str(n_dec=2))
# Corrected topocentric right ascension: : 22h 38' 8.54''
  print("Corrected topocentric declination", top_dec.dms_str(n_dec=1))
# Corrected topocentric declination: -15d 46' 30.0''
