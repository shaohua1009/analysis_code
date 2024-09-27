#!/bin/env python

import numpy as np
import math
import sys

centroid=np.loadtxt("centroids",dtype=np.float, unpack=False)

inp = "dihedrals_unclustered.den" #sys.argv[1]

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
  for i in range(nlines):
    belongdist=2
    x0, y0, z0, d0 = lines[i]
    for j in range(len(centroid)):
      x1, y1, z1, c1 = centroid[j]
      dist = math.sqrt(DihedDiff(x1,x0)**2 + DihedDiff(y1,y0)**2 + DihedDiff(z1,z0)**2)
    #print (Avgdist)
      if dist <= belongdist:
          clusterassign = c1
          belongdist = dist
    print (x0,y0,z0,int(clusterassign))
else:
  for i in range(nlines):
    belongdist=2
    x0, y0, d0 = lines[i]
    for j in range(len(centroid)):
      x1, y1, c1 = centroid[j]
      dist = math.sqrt(DihedDiff(x1,x0)**2 + DihedDiff(y1,y0)**2)
    #print (Avgdist)
      if dist <= belongdist:
          clusterassign = c1
          belongdist = dist
    print (x0,y0,int(clusterassign))

