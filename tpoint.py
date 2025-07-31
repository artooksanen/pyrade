from math import *

def sec(x):
    return 1.0/cos(x) 

def read_model(fname):
   """
   reads TPoint pinting model parameters from the given file
   """
   global modelname
   global IH,ID,NP,CH,MA,ME
   IH=ID=NP=CH=MA=ME=0
   f = open(fname, 'r')
   modelname=f.readline()
   refraction=f.readline()
   while f:
       line=f.readline()
#       print 'reading from file: '+line
#       print 'alku:#'+line[0:3]+"#"
       if line[0:3]!="END" and line!="":
#         print "ei loppunut"
         s = line.split()
         if(s[0]=="IH"): IH=float(s[1])
         if(s[0]=="ID"): ID=float(s[1])
         if(s[0]=="NP"): NP=float(s[1])
         if(s[0]=="CH"): CH=float(s[1])
         if(s[0]=="MA"): MA=float(s[1])
         if(s[0]=="ME"): ME=float(s[1])
       else:
         break
   f.close()
   return(1)

def print_model():
   print("Model:",modelname)
   print("IH=",IH)
   print("ID=",ID)
   print("NP=",NP)
   print("CH=",CH)
   print("MA=",MA)
   print("ME=",ME)

def correction(h,d):
      """
      returns tpoint hour angle and declination correction
      parameters are in radians
      """

      dh = 0.0
      dh +=   IH
      dh +=   NP * tan ( d )
      dh +=   CH / sec ( d )
      dh += - MA * cos ( h ) * tan ( d )
      dh +=   ME * sin ( h ) * tan ( d )

      dd = 0.0
      dd +=   ID
      dd +=   MA * sin ( h )
      dd +=   ME * cos ( h )

      return (radians(dh/3600.),radians(dd/3600.))

def uncorrected(h,d):
      """ returns uncorrected raw encoder coordinates from the true coordinates """
      (dh,dd)=correction(h,d)
      ht = h - dh
      dt = d - dd
      return (ht,dt)

def corrected(h,d):
      """ returns true coordinates from raw encoder coordinates """
      (dh,dd)=correction(h,d)
      ht = h + dh
      dt = d + dd
      return (ht,dt)


read_model('tpoint-model.dat')

if __name__=="__main__":

    print_model()
    h=0.0
    d=0.0
    (ac,ec)=corrected(radians(h),radians(d))
    print("target:   ",h,d)
    print("corrected:",degrees(ac),degrees(ec))
    