#!/bin/env python

import numpy as np
import sys

inp = sys.argv[1]
cut = float(sys.argv[2]) 

lines = np.loadtxt(inp, dtype=np.float, comments='#', unpack=False)

if3D = (len(lines[0]) == 4)
if if3D:
  for line in lines:
    x, y, z, d = line
    if d > cut:
      print ("%-10.5f %-10.5f %-10.5f %-10.5f"%(x, y, z, d))
else:
  for line in lines:
    x, y, d = line
    if d > cut:
      print ("%-10.5f %-10.5f %-10.5f"%(x, y, d))


