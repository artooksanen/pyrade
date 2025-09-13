import time
from alpaca.telescope import *      # Multiple Classes including Enumerations
from alpaca.exceptions import *
import requests     # Or just the exceptions you want to catch
import tpoint
import hor
from math import *

T = Telescope('192.168.8.2:5555', 0) # rihlaperä 
#T = Telescope('192.168.8.102:5555', 0) # Alpyca wifi
#T = Telescope('192.168.8.100:5555', 0) # Alpyca

#192.168.8.103:11111
#T = Telescope('192.168.8.103:11111', 0) # sky_simulator with 5 arc min elevation error

target_ra=0.0
target_de=0.0

ra=0.0
de=0.0

def connect():
   #T.Connect()                         # New async connect
   if not T.Connected:
    T.Connected=True
   while not T.Connected:
     print(f'Not connected to {T.Name}',T.Connected)
     time.sleep(1)
   print(f'Connected to {T.Name}',T.Connected)
   print(T.Description)
   #print("canmoveaxis:",T.CanMoveAxis)


def slew(r,d):
   global target_ra,target_de
   target_ra=r
   target_de=d
   print('Starting slew...')
   t=hor.ttojd(time.time())
   ta=hor.taika(t)
   h=(ta-r)*15.0 #degrees
   (h1,d1)=tpoint.uncorrected(radians(h),radians(d))
   r1=ta-degrees(h1)/15.0 #hours
   T.SlewToCoordinatesAsync(r1, degrees(d1))

def get_target_coordinates():
  return (target_ra,target_de)

def slewing():
  return T.Slewing

def tracking():
  return T.Tracking

def abort():
  T.AbortSlew()

def get_coordinates():
  global ra,de 
  try:
    ds=T.DeviceState
    #print(ds)
    for k in ds:
      #print(k)
      #print(k["Name"])
      #print(k["Value"])
      if k["Name"]=="RightAscension":
        r=k["Value"]      
      if k["Name"]=="Declination":
        d=k["Value"]      
      if k["Name"]=="RACounter":
        ra_counter=k["Value"]      
      if k["Name"]=="DecCounter":
        de_counter=k["Value"]      

    t=hor.ttojd(time.time())
    ta=hor.taika(t)
    h=(ta-r)*15.0 #degrees
    (h1,d1)=tpoint.corrected(radians(h),radians(d))
    ra=ta-degrees(h1)/15.0
    de=degrees(d1)
  except requests.exceptions.Timeout:
    print("Timeout occurred receiving telescipe state")
  finally:
    return ra,de,ra_counter,de_counter  

def rightascension():
  global ra 
  try:
    r=T.RightAscension
    d=T.Declination
    t=hor.ttojd(time.time())
    ta=hor.taika(t)
    h=(ta-r)*15.0 #degrees
    (h1,d1)=tpoint.corrected(radians(h),radians(d))
    ra=ta-degrees(h1)/15.0
    return ra
  except requests.exceptions.Timeout:
    print("Timeout occurred ra")
  finally:
    return ra  

def declination():
  global de 
  try:
    r=T.RightAscension
    d=T.Declination
    t=hor.ttojd(time.time())
    ta=hor.taika(t)
    h=(ta-r)*15.0 #degrees
    (h1,d1)=tpoint.corrected(radians(h),radians(d))
    de=degrees(d1)
    return de
  except requests.exceptions.Timeout:
    print("Timeout occurred de")
  finally:
    return de  

def uncorrected_coordinates():
  return (T.RightAscension,T.Declination)

def sync(r,d):
  t=hor.ttojd(time.time())
  ta=hor.taika(t)
  h=(ta-r)*15.0 #degrees
  (h1,d1)=tpoint.uncorrected(radians(h),radians(d))
  r1=ta-degrees(h1)/15.0 #hours
  T.SlewToCoordinatesAsync(r1, degrees(d1))
  T.SyncToCoordinates(r,degrees(d1))

def disconnect():
   print("Disconnecting...")
   #T.Connected=False

if __name__ == '__main__':

  connect()
  print(get_coordinates())