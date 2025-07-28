import time
from alpaca.telescope import *      # Multiple Classes including Enumerations
from alpaca.exceptions import *
import requests     # Or just the exceptions you want to catch


#T = Telescope('192.168.8.2:5555', 0) # rihlaperä 
#T = Telescope('192.168.8.102:5555', 0) # Alpyca wifi
#T = Telescope('192.168.8.100:5555', 0) # Alpyca

#192.168.8.103:11111
T = Telescope('192.168.8.103:11111', 0) # sky_simulator


ra=0.0
de=0.0

def connect():
   T.Connect()                         # New async connect
   while T.Connecting:
     time.sleep(1)
   print(f'Connected to {T.Name}',T.Connected)
   print(T.Description)
   #print("canmoveaxis:",T.CanMoveAxis)


def slew(r,d):
   print('Starting slew...')
   T.SlewToCoordinatesAsync(r, d)

def slewing():
  return T.Slewing

def tracking():
  return T.Tracking

def abort():
  T.AbortSlew()

def rightascension():
  global ra 
  try:
    ra=T.RightAscension
  except requests.exceptions.Timeout:
    print("Timeout occurred ra")
  finally:
    return ra  

def declination():
  global de 
  try:
    de=T.Declination
  except requests.exceptions.Timeout:
    print("Timeout occurred de")
  finally:
    return de  

def sync(r,d):
   T.SyncToCoordinates(r,d)

def disconnect():
   print("Disconnecting...")
   T.Disconnect()