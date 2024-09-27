#!/bin/env python

import numpy as np
import math
import sys

inp = sys.argv[1] # grep "    N" GRID_ASSIGNATION2

lines = np.loadtxt(inp, dtype=np.float, comments='#', unpack=False)
if3D = (len(lines[0]) == 4)
nlines = len(lines)

def DihedDiff(before,after):
    '''
    Dihedral angle in degree, this function calculates the absoulte dihedral angle changes considering the circulation
    '''
    before = np.radians(before)
    after = np.radians(after)
    return math.sqrt((math.sin(after)-math.sin(before))**2+(math.cos(after)-math.cos(before))**2)

if if3D:
  lowestAvgdist=2
  centroid = "None"
  for i in range(nlines):
    Accdist = 0
    for j in range(nlines):
      x0, y0, z0, c0 = lines[i]
      x1, y1, z1, c1 = lines[j]
      dist = math.sqrt(DihedDiff(x1,x0)**2 + DihedDiff(y1,y0)**2 + DihedDiff(z1,z0)**2)
      Accdist += dist 
    Avgdist = Accdist/(nlines-1)
    if Avgdist <= lowestAvgdist:
        centroid = lines[i]
        lowestAvgdist = Avgdist
  print ('{:10.3f} {:10.3f} {:10.3f} {:5d}'.format(centroid[0],centroid[1],centroid[2],int(centroid[3])))
else:
  lowestAvgdist=2
  centroid = "None"
  for i in range(nlines):
    Accdist = 0
    for j in range(nlines):
      x0, y0, c0 = lines[i]
      x1, y1, c1 = lines[j]
      dist = math.sqrt(DihedDiff(x1,x0)**2 + DihedDiff(y1,y0)**2)
      Accdist += dist 
    Avgdist = Accdist/(nlines-1)
    #print (Avgdist)
    if Avgdist <= lowestAvgdist:
        centroid = lines[i]
        lowestAvgdist = Avgdist
  print ('{:10.3f} {:10.3f} {:5d}'.format(centroid[0],centroid[1],int(centroid[2])))

