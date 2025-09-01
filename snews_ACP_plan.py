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
pla=open("2025-08-22T00_00_14_priority_candidates.txt", "w")
pla.write("""#dir F:\CCD\SNEWS_2025-08-22T00_00_14_priority_candidates
#subframe 0.5
#posang 0
#sets 1
#count 1,1,1,1
#filter V,R,I,B
#interval 10,10,10,10
#binning 1,1,1,1\n""")

rows=candidates.readlines()
n=0
for row in rows:
#    print(row.split("\t"))
    l=row.split("\t")[0]
    r=float(row.split("\t")[1])/15.0
    d=float(row.split("\t")[2])
    n=n+1
    nimi="SNEWS_target_"+str(n)
    pla.write(";{}\n".format(l))
    pla.write("{}\t{}\t{}\n".format(nimi,r,d))
            
candidates.close()
pla.close()