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
   print('Starting slew...')
   t=hor.ttojd(time.time())
   ta=hor.taika(t)
   h=(ta-r)*15.0 #degrees
   (h1,d1)=tpoint.uncorrected(radians(h),radians(d))
   r1=ta-degrees(h1)/15.0 #hours
   T.SlewToCoordinatesAsync(r1, degrees(d1))

def slewing():
  return T.Slewing

def tracking():
  return T.Tracking

def abort():
  T.AbortSlew()

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

def sync(r,d):
   T.SyncToCoordinates(r,d)

def disconnect():
   print("Disconnecting...")
   #T.Connected=False