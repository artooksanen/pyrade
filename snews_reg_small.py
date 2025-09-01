import hor
import telescope
import time
import solve
import camera
import hms
import epoch
import math
import epoch
import os

candidates=open("2025-08-22T00_00_14_priority_candidates.tsv", "r")
reg=open("2025-08-22T00_00_14_priority_candidates_small.reg", "w")
reg.write("# Region file format: DS9 version 4.1\n")
reg.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
reg.write("fk5\n")


rows=candidates.readlines()
n=0
for row in rows:
    print(row.split("\t"))
    l=row.split("\t")[0]
    r=float(row.split("\t")[1])
    d=float(row.split("\t")[2])
    reg.write("""circle({},{},30.0\") # text={{{}}}\n""".format(r,d,l))
            
candidates.close()
reg.close()