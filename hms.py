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
  a=(abs(d)-da(d)-dm(d)/60.0)*3600;
  return int(a)

