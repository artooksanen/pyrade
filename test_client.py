import time
from alpaca.telescope import *

T = Telescope('192.168.8.103:11111', 0) 
#T.Connect()                       
#while T.Connecting:
#    time.sleep(1)
ra=T.RightAscension
de=T.Declination
print("ra=",ra,"de=",de)
#T.Disconnect()  