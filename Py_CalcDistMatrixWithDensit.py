#!/bin/env python

import numpy as np
import math
import sys

inp = sys.argv[1]

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
    for j in range(i+1, nlines):
      x0, y0, z0, d0 = lines[i]
      x1, y1, z1, d1 = lines[j]
      dist = math.sqrt(DihedDiff(x1,x0)**2 + DihedDiff(y1,y0)**2 + DihedDiff(z1,z0)**2)
      print ("%10d %10d %15.5f %10.5f %10.5f"%(i+1, j+1, dist, d0, d1))
else:
  for i in range(nlines):
    for j in range(i+1, nlines):
      x0, y0, d0 = lines[i]
      x1, y1, d1 = lines[j]
      dist = math.sqrt(DihedDiff(x1,x0)**2 + DihedDiff(y1,y0)**2)
      print ("%10d %10d %15.5f %10.5f %10.5f"%(i+1, j+1, dist, d0, d1))

