from math import *


#Jyväskylä
pituus=25.733
leveys=62.217


def set_location(lon,lat):
  pituus=lon
  leveys=lat


def get_location():
  return (pituus,leveys)


def atkor(ra,de,t):	 #t:julian date
  tk=tkulma(t,ra)
  return hor(tk,de)


def hortoeq(ats,kor,t):
  A=rad(ats-180.0)
  h=rad(kor)
  l=rad(leveys)
  H=atan2(sin(A),(cos(A)*sin(l)+tan(h)*cos(l)))
  D=asin(sin(l)*sin(h)-cos(l)*cos(h)*cos(A))
  ta=taika(t);
  r=ta-H*12.0/pi;
  if(r<0):
     r=r+24.0;
  if(r>24.0):
     r=r-24.0;
  return(r,D/pi*180.0)

def rad(x):
   return x*pi/180.0

def deg(x):
   return x/pi*180.0

def tkulma(t,ra):
  ta=taika(t)
  tk=ta-ra
  return(tk)

def tojd(y,m,d,hh,mm,ss):
  jd=367*y-7*(y+(m+9)//12)//4-3*((y+(m-9)//7)/100+1)//4+275*m//9+d+1721028.5+hh/24.0+mm/1440.0+ss/86400.0
  return jd


def ttojd(t):
  return 2440587.5+t/86400.0


def taika(t):
  T=(t-2451545.0)/36525.0
  ta=280.46061837+360.98564736629*(t-2451545.0)+0.000387933*T*T+T*T*T/38710000.0 #asteet 
  ta=ta/15.0 # tunnit 
  ta=ta+(pituus)/15.0
  ta=(ta/24.0-floor(ta/24.0))*24.0
  return ta

def hor(tk,de):
  tkr=rad(tk*15.0)
  rde=rad(de)
  rkor=asin(sin(rad(leveys))*sin(rde)+cos(rad(leveys))*cos(rde)*cos(tkr))
  rats=acos((sin(rde)-sin(rad(leveys))*sin(rkor))/(cos(rad(leveys))*cos(rkor)))
  kor=deg(rkor)
  ats=deg(rats)	 #atsimuutti pohjoisesta
  if(sin(tkr)>0.0):
    ats=360.0-ats
  return (ats,kor)

def nousee(t,r,d):
  cost=-tan(rad(leveys))*tan(rad(d+37.0/60.0)) #refraktio
  if (cost<-1.0):    #ei nouse horisontin yläpuolelle
      return(-99.0)
  elif(cost>1.0):   #sirkumpolaarinen 
      return(99.0)
  else:
      tk=deg(acos(cost))*12.0/180.0
      e=etelassa(t,r)
      n=e-tk*0.997269
      if(n<0):
         n=n+24.0
      if(n>24):
         n=n-24.0
      return(n)


def etelassa(t,r):       # laskee kohteen etelässäoloajan
   ta=taika(t)
   x=(r-ta)
   if(x<0):
      x+=24.0
   te=t+(x/24.0)*0.997269
   he=(te-floor(te))*24.0+14.0
   if(he<0):
      he=he+24.0
   if(he>24):
      he=he-24.0
   return(he)

def laskee(t,r,d):
   cost=-tan(rad(leveys))*tan(rad(d+37/60.0))
   if (cost<-1.0):            #ei nouse horisontin yläpuolelle
      return(-99.0)
   elif(cost>1.0):       #sirkumpolaarinen */
      return(99.0)
   else:
      tk=deg(acos(cost))*12.0/180.0
      e=etelassa(t,r)
      l=e+tk*0.997269
      if(l<0):
          l+=24.0
      if(l>24):
          l-=24.0
      return(l)




if __name__ == '__main__':
  t=tojd(2025,1,25,16,28,00)
  print("t=",t)
  r=6.752500
  d=-16.716667
  print("r=",r,"d=",d)
  (a,k)=atkor(r,d,t)
  print("a=",a,"k=",k)
  e=etelassa(t,r)
  print("etelässä=",e)
  n=nousee(t,r,d)
  l=laskee(t,r,d)
  print("nousee:",n,"laskee:",l)
