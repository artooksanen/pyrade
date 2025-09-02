import math

# ra tunnit
def rh(h):
  return int(h)

#ra minuuti
def rm(h):
  return int((h-rh(h))*60)

#ra sekunnit
def rs(h):
  return int((h-rh(h)-rm(h)/60.0)*3600)

#ra sekunnit
def rs(h):
  return int((h-rh(h)-rm(h)/60.0)*3600.0)

#ra sekunnit desimaaleina
def rsd(h):
  return (h-rh(h)-rm(h)/60.0)*3600.0

#de etumerkki +/-
def ds(d):
  if d<0:
     return '-'
  else:
     return '+'

#de asteet
def da(d):
  a=abs(d)
  return int(a)

#de minuutit
def dm(d):
  a=(abs(d)-da(d))*60.0
  return int(a)

#de sekunnit
def dss(d):
  a=(abs(d)-da(d)-dm(d)/60.0)*3600
  return int(a)

#de sekunnit desimaaleina
def dssd(d):
  a=(abs(d)-da(d)-dm(d)/60.0)*3600
  return a


def hhmmss(h):
    hh=math.floor(h)
    mm=math.floor((h-hh)*60.0)
    ss=math.floor((h-hh-mm/60.0)*3600.0)
    hhs=str(hh)
    if(hh<10):
        hhs="0"+hhs
    mms=str(mm)
    if(mm<10):
        mms="0"+mms
    sss=str(ss)
    if(ss<10):
        sss="0"+sss
    return hhs+" "+mms+" "+sss

def sddmmss(d):
    s="+"
    if d<0:
       d=-d
       s="-"
    dd=math.floor(d)
    mm=math.floor((d-dd)*60.0)
    ss=math.floor((d-dd-mm/60.0)*3600.0)
    dds=str(dd)
    if dd<10:
        dds="0"+dds
    mms=str(mm)
    if mm<10:
        mms="0"+mms
    sss=str(ss)
    if ss<10:
        sss="0"+sss
    return s+dds+" "+mms+" "+sss
