import curses
from datetime import datetime, timezone
import time
import hms
import kohdeluettelo
import hor
import planets
import telescope
import epoch
import re
import sexadecimal

screen=curses.initscr()
lwhite=1
blue=2
white=3
yellow=4
red=5
epookki0=2000.0
epookkinyt=2025.5
t=0.0
last_second=0
tf=None

def input():
  global last_second
  input=""
  gotorc(8,3)
  screen.clrtoeol()
  while True:
      now_second=datetime.now().second
      if now_second!=last_second:
        update_time(1)
        update_coord(1)
        last_second=now_second
        if telescope.slewing():
           printrs(3,10,red,blue,"**ajetaan kohteeseen**                            ")
        else:
           printrs(3,10,red,blue,"                                                  ")
   
      printrs(3,8,lwhite,blue,input);
      c = screen.getch()
#      if c == ord('q'):
#        break  # Exit the while loop
      if c>0:
         printrs(3,27,white,blue, "{:d}   ".format(c))
      if c == 10: # return
           break
      if c > 0:
        if(c == 263 or c==330 or c==8 or c==260):
         input=input[:-1]
        else:
          input=input+chr(c)
        printrs(3,8,lwhite,blue,input+"  ");
      time.sleep(0.01)
  return input 

def get_coord():
  r,d,rcounter,dcounter=telescope.get_coordinates()
  return (r,d,rcounter,dcounter)

def aja(r,d):
  printrs(3,10,red,blue,"**ajetaan kohteeseen**                            ")
  telescope.slew(r,d)

def epookki(r,d,e1,e2):
  return epoch.precess(r,d,e1,e2)

def printrs(c,r,col1,col2,s):
  screen.addstr(r, c, s)

def update_time(j):
   global t
   ut=datetime.utcnow()
   lt=datetime.now()
   printrs(56,3,lwhite,blue,lt.strftime('%d.%m.%Y %H:%M:%S'))
   printrs(56,4,lwhite,blue,ut.strftime('%d.%m.%Y %H:%M:%S'))
   y=ut.year
   m=ut.month
   d=ut.day
   hh=ut.hour
   mm=ut.minute
   ss=ut.second
   t=hor.tojd(y,m,d,hh,mm,ss)
   printrs(56,6,lwhite,blue,"{jd:.5f}".format(jd=t))
   ta=hor.taika(t)
   printrs(56,5,yellow,blue,"{:02d}:{:02d}:{:02d}".format(hms.rh(ta),hms.rm(ta),hms.rs(ta)))

def update_screen():
    screen.clear()
    printrs(3,1,lwhite,blue, "Sirius koordinaattori v3.0")
    printrs(42,1,white,blue, "Jyväskylän Sirius ry 2025")
    printrs(3,3,lwhite,blue, "Rekt       Dekl")
    printrs(26,3,lwhite,blue,"Atsim   Kor")
    printrs(42,3,lwhite,blue,"normaaliaika:")
    printrs(42,4,white,blue, "UT:")
    printrs(42,5,white,blue, "tähtiaika:")
    printrs(42,6,white,blue, "Jul.pvm:")
    epookki=2000.0
    buffer="epookki:      {epookki:.1f}"
    printrs(42,7,white,blue,buffer.format(epookki=epookki))
    printrs(3,7,white,blue, "KOMENTO")

def update_coord(i):
  global t
  (ra,de,rcounter,dcounter)=get_coord()                        # luetaan koordinaatit
  (ra1,de1)=epookki(ra,de,epookkinyt,epookki0)
  h=hms.rh(ra1)
  m=hms.rm(ra1)
  s=hms.rs(ra1)
  printrs(3,5,yellow,blue,"{:02d} {:02d} {:02d}".format(h,m,s))
  s=hms.ds(de1)
  d=hms.da(de1)
  m=hms.dm(de1)
  printrs(14,5,yellow,blue,"{}{:02d} {:02d}".format(s,d,m))
  (ats,kor)=hor.atkor(ra,de,t)
  printrs(26,5,yellow,blue,"{:5.1f}  {:4.1f}".format(ats,kor))
  printrs(10,27,yellow,blue,"{:10d}  {:10d}".format(rcounter,dcounter))
  

def tiedot(nimi,r,d,ptr):
   printrs(3,10,red,blue,"tiedot kohteesta                            ")
   printrs(20,10,red,blue,nimi)
   gotorc(12,3)
#   sendrs("\x1bJ")                           # esc J =  clear screen 
#   clear_box(3,12,77,22,white,blue,' ')
   screen.clrtobot()
   printrs(4,12,white,blue,"nimi")
   printrs(4,13,yellow,blue,nimi)
#   epoch(r,d,&r1,&d1,epookki0,epookki1)
   r1=r
   d1=d
   buffer="{hh:02d} {mm:02d} {ss:02d}".format(hh=hms.rh(r1),mm=hms.rm(r1),ss=hms.rs(r1))
   printrs(22,12,white,blue,"rekt")
   printrs(22,13,yellow,blue,buffer)
   buffer="{s:}{d:02d} {m:02d}".format(s=hms.ds(d1),d=hms.da(d1),m=hms.dm(d1))
   printrs(33,12,white,blue,"dekl")
   printrs(33,13,yellow,blue,buffer)
   (atz,alt)=hor.atkor(r1,d1,t)
   buffer="{a:3.0f}  {b:3.0f}".format(a=atz,b=alt)
   printrs(43,12,white,blue,"ats  kor")
   printrs(43,13,yellow,blue,buffer)
   printrs(55,12,white,blue,"nousee  laskee")
   n=hor.nousee(t,r,d)
   if(n<24 and n>0):
     buffer="{hh:02d}:{mm:02d}".format(hh=hms.rh(n),mm=hms.rm(n))
   else:
     buffer="--:--"
   printrs(55,13,white,blue,buffer)
   l=hor.laskee(t,r,d)
   if(l<24 and l>0):
     buffer="{hh:02d}:{mm:02d}".format(hh=hms.rh(l),mm=hms.rm(l))
   else:
     buffer="--:--"
   printrs(63,13,white,blue,buffer)
   printrs(4,14,white,blue,"tiedot:")
   r=15
   while(ptr>0):
      (data,ptr)=kohdeluettelo.readdata(ptr)
      printrs(4,r,white,blue,data)
      r=r+1

def gotorc(r,c):
   screen.move(r,c)

def komennot():
   gotorc(12,3)
#   sendrs("\x1bJ")         #esc J =  clear screen 
   screen.clrtobot()
#   clear_box(3,12,77,20,white,blue,' ')
   printrs(3,12,yellow,blue,"Komennot ovat seuraavat:")
   printrs(3,13,lwhite,blue,"PERUS nimi")
   printrs(17,13,white,blue,"peruskoordinaatin asetus (nimi on kohde tai koordinaatit)")
   printrs(3,14,lwhite,blue,"nimi")
   printrs(17,14,white,blue,"kaukoputken kääntö kohteeseen")
   printrs(3,15,lwhite,blue,"TIEDOT nimi")
   printrs(17,15,white,blue,"tietoja kohteesta")
   printrs(3,16,lwhite,blue,"?nimi")
   printrs(17,16,white,blue,"tietoja kohteesta")
   #printrs(3,17,lwhite,blue,"EPOOKKI vuosi")
   #printrs(17,17,white,blue,"koordinaattiepookin asetus")
   #printrs(3,18,lwhite,blue,"SELAA")
   #printrs(17,18,white,blue,"kohdeluettelon selaus")
   #printrs(3,19,lwhite,blue,"OMAT tiedosto")
   #printrs(17,19,white,blue,"lisäkohdeluettelo")
   printrs(3,17,lwhite,blue,"LOPETUS")
   printrs(17,18,white,blue,"ohjelman lopetus")

def kohde(s):
   ut=datetime.utcnow()
   year=ut.year
   nimi=""
   ra=de=0.0
   l=kohdeluettelo.searchndx(s.upper())
   if l>-1:
      (nimi,ra,de,l)=kohdeluettelo.readndx(l)
      return (nimi,ra,de,l)
   if s=="MERKURIUS":
     nimi="Merkurius"
     ra,de=planets.mercury(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="VENUS":
     nimi="Venus"
     ra,de=planets.venus(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="MARS":
     nimi="MARS"
     ra,de=planets.mars(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="JUPITER":
     nimi="Jupiter"
     ra,de=planets.jupiter(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="SATURNUS":
     nimi="Saturnus"
     ra,de=planets.saturn(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="URANUS":
     nimi="Uranus"
     ra,de=planets.uranus(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="NEPTUNUS":
     nimi="Neptunus"
     ra,de=planets.neptune(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="PLUTO":
     nimi="Pluto"
     ra,de=planets.pluto(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="AURINKO":
     nimi="AURINKO"
     ra,de=planets.sun(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s=="KUU":
     nimi="KUU"
     ra,de=planets.moon(t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s[0:4]=="ETEL" or s=="ET":
     nimi="ETELA"
     ra,de=hor.hortoeq(180.0,0.0,t)
     ra,de=epoch.precess(ra,de,year,2000.0)
   elif s[0:3]=="HOR" and len(s.split(" "))>1:
      nimi=s
      try:
        ats=float(re.split("%*[^0-9.]",s.split()[1])[0])
        kor=float(re.split("%*[^0-9.]",s.split()[1])[1])
        ra,de=hor.hortoeq(ats,kor,t)
      except Exception:
        ra=de=0.0
      ra,de=epoch.precess(ra,de,year,2000.0)
   elif s[0].isnumeric():
      nimi=s
      ra,de=sexadecimal.parse(s)
      if ra == None or de == None:
         ra=0.0
         de=0.0
   return (nimi,ra,de,-1)

def main(stdscr):
    ptr=0
    # Clear screen
    screen=stdscr
    #curses.resize_term(24, 80)
    update_screen()
    telescope.connect()
#    prompt("KOMENTO")
    screen.nodelay(True)
    stdscr.refresh()
    while True:
      komento=input().upper()
      if telescope.slewing():
           telescope.abort()
           printrs(3,10,red,blue,"** ajo keskeytetty **                            ")
      if len(komento)==0:
         komennot()
      else:
        if len(komento.split())>1:
            if komento.split()[0]=="P" or komento.split()[0] == "PERUS":        
              k=komento[len(komento.split()[0])+1:]
              (nimi,ra,de,l) = kohde(k)
              tiedot(nimi,ra,de,l)
              printrs(3,10,red,blue,"** aseteteaan koordinaatit **       "+k)
              (ra_now,de_now)=epookki(ra,de,epookki0,epookkinyt)
              telescope.sync(ra_now,de_now)
              #komento=""
              nimi=""
        if komento=="LO":
           telescope.disconnect()
           break
        if komento=="TPOINT":
           save_tpoint()
        if komento!="":
           l=kohdeluettelo.searchndx(komento)
           if l>-1:
             (nimi,ra,de,ptr)=kohdeluettelo.readndx(l)
             tiedot(nimi,ra,de,ptr)
             (ra_now,de_now)=epookki(ra,de,epookki0,epookkinyt)
             aja(ra_now,de_now)
        if komento[0]=='?' and len(komento)>1:
          k=komento[1:].strip()
          l=-1
          if len(k)>0:
              (nimi,ra,de,l) = kohde(k)
          if l>-1:
             tiedot(nimi,ra,de,l)
          elif nimi!="":
           tiedot(nimi,ra,de,-1)
        if komento != "":
           (nimi,ra,de,l) = kohde(komento)
           if(nimi!=""):
            tiedot(nimi,ra,de,l)
            (ra_now,de_now)=epookki(ra,de,epookki0,epookkinyt)
            aja(ra_now,de_now)
    #telescope.disconnect()

def save_tpoint():
  global t,tf
  if(tf==None): 
    tf=open("pyrade_tpoint.dat","w",buffering=1)
    tf.write("pyrade\n")
    tf.write(":EQUAT\n")
    tf.write(":J2000\n")

    ut=datetime.utcnow()
    pvm=ut.strftime('%Y %m %d')
    #62 13 01.2 2025 4 1 0 1000 100 0.5 0.55
    buffer="{:s}{:02d} {:02d} {:02.1f} {:s} 0 1000 100 0.5 0.55\n".format(hms.ds(hor.leveys),hms.da(hor.leveys),hms.dm(hor.leveys),hms.dssd(hor.leveys),pvm)
    tf.write(buffer)
  (r1,d1)=telescope.get_target_coordinates() 
  (r1_2000,d1_2000)=epoch.precess(r1,d1,epookkinyt,2000.0)
  ta=hor.taika(t)
  (r0,d0)=telescope.uncorrected_coordinates()
  (r0_2000,d0_2000)=epoch.precess(r0,d0,epookkinyt,2000.0)

  buffer="{:02d} {:02d} {:02.1f} {:s}{:02d} {:02d} {:02d}.0 {:02d} {:02d} {:02.1f} {:s}{:02d} {:02d} {:02d}.0 {:02d} {:02d}\n".format(
         hms.rh(r1_2000),hms.rm(r1_2000),hms.rsd(r1_2000),hms.ds(d1_2000),hms.da(d1_2000),hms.dm(d1_2000),hms.dss(1_2000),
         hms.rh(r0_2000),hms.rm(r0_2000),hms.rsd(r0_2000),hms.ds(d0_2000),hms.da(d0_2000),hms.dm(d0_2000),hms.dss(d0_2000),
         hms.rh(ta),hms.rm(ta))
  if(tf):
    tf.write(buffer)
    printrs(3,10,red,blue,"tallettu koordinaatit rade_tpoint.dat tiedostoon                     ");


curses.wrapper(main)
