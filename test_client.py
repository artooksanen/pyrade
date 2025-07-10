from alpaca.telescope import *      # Multiple Classes including Enumerations

T = Telescope('192.168.8.102:5555', 0) # Alpyca

T.Connect()                         # New async connect
print(f'Connected to {T.Name}',T.Connected)
print(T.Description)

ra=T.RightAscension
print("RA=",ra)  

de=T.Declination
print("de=",de)  

T.Disconnect()