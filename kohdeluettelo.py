import struct
import sys


f = open("index.sor", "rb")
d = open("data.txt", "rb")

def close():
  f.close()
  d.close()

def read_int(f):
    s = f.read(4)
    return struct.unpack('i', s)[0]

def searchndx(nimi):
#   print("Searching...")
   a=-1
   b=15984
   l=-1
   n=0
   while((a!=b) and (n<20)):
     n=n+1
     c=(a+b)//2
     (text,ra,de,ptr)=readndx(c)
#     print(f"tietue {c}: {text}")
     if(text<nimi):
        a=c
     if(text>nimi):
        b=c
     if(text==nimi):
       a=b=c
       l=c
#     print(a,b,c)
#   if(l>-1):
#       print(f"tietue {c}: {text} ra:{ra:.4f} de:{de:.4f} ptr:{ptr}")
#   else:
#       print(f"ei löytynyt: {nimi}")
   return(l)

def readndx(c):
  f.seek(c*22)
  data=f.read(10)
  #print(data)
  nimi=data[0:9].decode("utf-8").rstrip('\x00')
  #print(nimi)
  ra=read_int(f)/3600.0
  #print(ra)
  #print(ra/3600.0)
  de=read_int(f)/60.0
  #print(de)
  #print(de/60.0)
  ptr=read_int(f)
  #print(ptr)
  return (nimi,ra,de,ptr)


def readdata(row):
      offset=69*row
      d.seek(offset)
      data=""
      data=d.read(65)
#      print(data)
      n=0
      while(data[n]>0 or n==65):
         n=n+1
      data=data[0:n].decode("utf-8")
      ptr=read_int(d)
#      print(data)
#      print(ptr)
      return((data,ptr))


if __name__ == '__main__':
  i=searchndx(sys.argv[1].upper())

  if i>0:
    (nimi,ra,de,ptr)=readndx(i)
    print(f"{nimi} ra:{ra:.4f} de:{de:.4f}")
    print("Tiedot:")
    while(ptr>0):
      (data,ptr)=readdata(ptr)
      print(data)
  else:
    print("kohdetta ei löytynyt")

